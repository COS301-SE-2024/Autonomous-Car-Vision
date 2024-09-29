import glob
import os
import sys
import time
import random
import pygame
import numpy as np
import cv2
import json
from ultralytics import YOLO
import queue
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import bobTheBuilder
import torch
import os
import shutil
import datetime
import platform
import logging
import imageio

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

# Initialization
actor_list = []
model = YOLO('./models/yolov8n.pt')


def get_keyboard_control(vehicle):
    keys = pygame.key.get_pressed()
    control = carla.VehicleControl()
    control.throttle = 1.0 if keys[pygame.K_w] else 0.0
    control.brake = 1.0 if keys[pygame.K_s] else 0.0
    control.steer = -1.0 if keys[pygame.K_a] else 1.0 if keys[pygame.K_d] else 0.0
    control.hand_brake = keys[pygame.K_SPACE]
    return control


def process_image(image):
    array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
    array = np.reshape(array, (image.height, image.width, 4))
    array = array[:, :, :3]
    array = array[:, :, ::-1]  # Convert BGRA to RGB
    return array


def run_ai_model(image_array):
    results = model(image_array)
    result_image = results[0].plot()
    return result_image, results[0].boxes.data.tolist()


def process_lidar_data(lidar_measurement):
    points = np.frombuffer(lidar_measurement.raw_data, dtype=np.dtype('f4'))
    # Reshape to (N, 4), where N is the number of points, and each point has (x, y, z, intensity)
    lidar_data_np = np.reshape(points, (int(points.shape[0] / 4), 4))  # x, y, z, intensity
    return lidar_data_np


def convert_array_to_surface(image_array):
    surface = pygame.surfarray.make_surface(image_array.swapaxes(0, 1))
    return surface


def stitch_video_from_frames(output_folder, video_filename, calculated_fps):
    images = [img for img in sorted(os.listdir(output_folder)) if img.endswith(".png")]
    if not images:
        return

    # Assuming all images have the same resolution
    first_frame = imageio.imread(os.path.join(output_folder, images[0]))
    height, width = first_frame.shape[:2]

    # Create a writer object using imageio
    writer = imageio.get_writer(video_filename, fps=calculated_fps, codec='libx264', pixelformat='yuv420p')

    for image in images:
        frame = imageio.imread(os.path.join(output_folder, image))
        writer.append_data(frame)

    writer.close()


class CarlaSyncMode:
    def __init__(self, world, sensors, fps=30):
        self.world = world
        self.sensors = sensors
        self.delta_seconds = 1.0 / fps
        self.frame = 0
        self._queues = []
        self._settings = None

    def __enter__(self):
        self._settings = self.world.get_settings()
        self.world.apply_settings(carla.WorldSettings(
            synchronous_mode=True,
            fixed_delta_seconds=self.delta_seconds))

        for sensor in self.sensors:
            q = queue.Queue()
            sensor.listen(q.put)
            self._queues.append(q)
        return self

    def tick(self, timeout):
        self.frame += 1
        self.world.tick()
        data = [self._queues[i].get(timeout=timeout) for i in range(len(self.sensors))]
        return data

    def __exit__(self, *args, **kwargs):
        self.world.apply_settings(self._settings)
        for sensor in self.sensors:
            sensor.stop()


def sensor_factory(world, vehicle, sensor_parameters):
    sensors = []
    sensor_labels = []
    for params in sensor_parameters:
        if params['sensor_type'] == 'camera':
            sensor_bp = world.get_blueprint_library().find('sensor.camera.rgb')
            sensor_bp.set_attribute('image_size_x', str(params['width']))
            sensor_bp.set_attribute('image_size_y', str(params['height']))
            sensor_bp.set_attribute('fov', str(params['fov']))
        elif params['sensor_type'] == 'lidar':
            sensor_bp = world.get_blueprint_library().find('sensor.lidar.ray_cast')
            sensor_bp.set_attribute('channels', str(params['channels']))
            sensor_bp.set_attribute('range', str(params['range']))
            sensor_bp.set_attribute('rotation_frequency', str(params['rotation_frequency']))
            sensor_bp.set_attribute('points_per_second', str(params['points_per_second']))
            sensor_bp.set_attribute('upper_fov', str(params['upper_fov']))
            sensor_bp.set_attribute('lower_fov', str(params['lower_fov']))
        else:
            continue  # Handle other sensor types if needed

        transform = carla.Transform(carla.Location(x=params['x'], y=params['y'], z=params['z']),
                                    carla.Rotation(roll=params['roll'], pitch=params['pitch'], yaw=params['yaw']))
        sensor = world.spawn_actor(sensor_bp, transform, attach_to=vehicle)
        sensors.append(sensor)
        sensor_labels.append(params['sensor_label'])

    return sensors, sensor_labels


def integrate_lidar_with_image(image, lidar_data, bounding_boxes):
    # Get image dimensions
    image_height, image_width, _ = image.shape

    # Extract Cartesian coordinates from LiDAR data
    x = lidar_data[:, 0]
    y = lidar_data[:, 1]
    z = lidar_data[:, 2]

    # Compute r, θ (azimuth), and φ (elevation)
    r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    theta = np.arctan2(y, x)  # Azimuth (horizontal angle)
    phi = np.arcsin(z / r)  # Elevation (vertical angle)

    # Convert the FOV angles from degrees to radians
    horizontal_fov = np.radians(90 / 2)  # 90° horizontal FOV
    vertical_fov = np.radians(60 / 2)  # 60° vertical FOV

    # Apply the initial FOV constraints to limit the LiDAR data to 90° horizontal and 60° vertical FOV
    fov_mask = (np.abs(theta) <= horizontal_fov) & (np.abs(phi) <= vertical_fov)
    filtered_data = lidar_data[fov_mask]
    filtered_r = r[fov_mask]

    # If no points are left after filtering, return the image unchanged
    if filtered_r.size == 0:
        return image, []

    # Extract filtered x, y, z coordinates
    x_filtered = filtered_data[:, 0]
    y_filtered = filtered_data[:, 1]
    z_filtered = filtered_data[:, 2]

    # Store indices and 3D world positions
    indices_in_fov = np.where(fov_mask)[0]
    world_positions = filtered_data  # This keeps the x, y, z of points within FOV

    # Example intrinsic parameters (focal length and principal point)
    focal_length = image_width / (2 * np.tan(horizontal_fov))
    principal_point = np.array([image_width / 2, image_height / 2])

    # Example extrinsic parameters - inverting the rotation to skew outward
    angle_y = np.radians(-10)  # Negative rotation around the y-axis (adjust this as needed)
    R = np.array([
        [np.cos(angle_y), 0, np.sin(angle_y)],
        [0, 1, 0],
        [-np.sin(angle_y), 0, np.cos(angle_y)]
    ])

    t = np.array([0.0, 0.0, 0.2])  # Negative translation along the z-axis (adjust this as needed)

    # Transform filtered LiDAR points from LiDAR to camera coordinates
    points_lidar = np.vstack((x_filtered, y_filtered, z_filtered))  # Create 3xN matrix
    points_camera = R @ points_lidar + t[:, np.newaxis]  # Apply rotation and translation

    # Perspective projection
    pixel_x = (focal_length * points_camera[1, :] / points_camera[0, :]) + principal_point[0]
    pixel_y = (focal_length * (-points_camera[2, :] / points_camera[0, :])) + principal_point[1]

    # Filter based on valid pixel coordinates within the image dimensions
    valid_pixels_mask = (pixel_x >= 0) & (pixel_x < image_width) & (pixel_y >= 0) & (pixel_y < image_height)
    pixel_x = pixel_x[valid_pixels_mask].astype(int)
    pixel_y = pixel_y[valid_pixels_mask].astype(int)
    filtered_r = filtered_r[valid_pixels_mask]  # Update filtered_r to correspond to valid pixels

    # Update indices and world positions based on valid pixels
    valid_indices = indices_in_fov[valid_pixels_mask]
    valid_world_positions = world_positions[valid_pixels_mask]

    # Normalize the distances (r) for color mapping
    norm = plt.Normalize(vmin=filtered_r.min(), vmax=filtered_r.max())
    cmap = plt.colormaps.get_cmap('plasma')  # Updated method for colormap
    colors = cmap(norm(filtered_r))[:, :3]  # Get RGB values from the colormap
    colors = (colors * 255).astype(int)  # Convert to 8-bit values for OpenCV

    # Overlay the points on the image
    for i in range(len(pixel_x)):
        color = (int(colors[i][2]), int(colors[i][1]), int(colors[i][0]))  # Convert RGB to BGR for OpenCV
        cv2.circle(image, (pixel_x[i], pixel_y[i]), radius=2, color=color, thickness=-1)

    # Create a list to store the world position data
    world_data = []

    # Process each bounding box
    for bbox in bounding_boxes:
        x_min, y_min, x_max, y_max, score, class_id = bbox
        x_min, y_min, x_max, y_max = int(x_min), int(y_min), int(x_max), int(y_max)

        # Find LiDAR points within this bounding box
        inside_bbox_mask = (pixel_x >= x_min) & (pixel_x <= x_max) & (pixel_y >= y_min) & (pixel_y <= y_max)
        if np.any(inside_bbox_mask):
            # Get the minimum distance within the bounding box
            min_distance_idx = np.argmin(filtered_r[inside_bbox_mask])
            min_distance = filtered_r[inside_bbox_mask][min_distance_idx]
            world_position = valid_world_positions[inside_bbox_mask][min_distance_idx]

            # Draw the bounding box
            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

            # Start building the region of connected points
            region_points = [world_position]

            # Create a local mask for points inside the bounding box
            local_world_positions = valid_world_positions[inside_bbox_mask]
            local_region_mask = np.zeros(local_world_positions.shape[0], dtype=bool)
            local_region_mask[min_distance_idx] = True

            distance_limit = min_distance / 10

            while True:
                current_region_size = len(region_points)
                for i, wp in enumerate(local_world_positions):
                    if not local_region_mask[i]:  # Only consider points not already in the region
                        if np.any(np.linalg.norm(np.array(region_points) - wp, axis=1) < distance_limit):
                            region_points.append(wp)
                            local_region_mask[i] = True
                # Break if no new points are added
                if len(region_points) == current_region_size:
                    break

            # Get the pixel coordinates for the region points
            region_pixel_x = pixel_x[inside_bbox_mask][local_region_mask]
            region_pixel_y = pixel_y[inside_bbox_mask][local_region_mask]

            # Overlay the region points as green dots
            for i in range(len(region_pixel_x)):
                cv2.circle(image, (region_pixel_x[i], region_pixel_y[i]), radius=2, color=(0, 255, 0), thickness=-1)

            # Only apply PCA if there are at least 2 points
            if len(local_world_positions[local_region_mask]) >= 2:
                # Apply PCA to the region points to determine the orientation
                pca = PCA(n_components=2)
                pca.fit(local_world_positions[local_region_mask])
                orientation_vector = pca.components_[0]  # First principal component (dominant direction)

                # Calculate the angle of the orientation vector relative to the x-axis in radians
                orientation_angle = np.arctan2(orientation_vector[1], orientation_vector[0])

                # Display the orientation and distance inside the bounding box
                text = f"Object: {min_distance:.2f}m, θ: {np.degrees(orientation_angle):.1f}°"
                cv2.putText(image, text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                # Save the world position with label, distance, and orientation in the list
                world_data.append({
                    "label": "object",  # Change "object" to actual detected object class from YOLO if available
                    "world_position": {
                        "x": float(world_position[0]),
                        "y": float(world_position[1]),
                        "z": float(world_position[2])
                    },
                    "distance": float(min_distance),
                    "orientation": {
                        "angle_degrees": float(np.degrees(orientation_angle)),
                        "vector": {
                            "x": float(orientation_vector[0]),
                            "y": float(orientation_vector[1])
                        }
                    }
                })
            else:
                # Handle the case with fewer than 2 points
                text = f"Object: {min_distance:.2f}m"
                cv2.putText(image, text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                # Save the world position without orientation
                world_data.append({
                    "label": "object",  # Change "object" to actual detected object class from YOLO if available
                    "world_position": {
                        "x": float(world_position[0]),
                        "y": float(world_position[1]),
                        "z": float(world_position[2])
                    },
                    "distance": float(min_distance),
                    "orientation": {
                        "angle_degrees": float(np.degrees(0)),
                        "vector": {
                            "x": float(0),
                            "y": float(0)
                        }
                    }
                })

    return image, world_data


def save_frame_and_data(image_array, bounding_boxes, lidar_data, frame_number, output_folder, vehicle_transform):
    # Save the processed image
    filename = os.path.join(output_folder, f"frame_{frame_number:06d}.png")
    cv2.imwrite(filename, cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR))

    # Save the bounding boxes to a JSON fileda
    bbox_filename = os.path.join(output_folder, f"frame_{frame_number:06d}_bboxes.json")
    with open(bbox_filename, 'w') as bbox_file:
        json.dump(bounding_boxes, bbox_file)

    # Save the full LiDAR data including intensity (x, y, z, intensity)
    lidar_filename = os.path.join(output_folder, f"frame_{frame_number:06d}_lidar.npy")
    np.save(lidar_filename, lidar_data)

    # Save the vehicle's position and orientation (weaver JSON file)
    weaver_filename = os.path.join(output_folder, f"frame_{frame_number:06d}_weaver.json")
    weaver_data = {
        'position': {
            'x': vehicle_transform.location.x,
            'y': vehicle_transform.location.y,
            'z': vehicle_transform.location.z
        },
        'orientation': {
            'roll': vehicle_transform.rotation.roll,
            'pitch': vehicle_transform.rotation.pitch,
            'yaw': vehicle_transform.rotation.yaw
        }
    }
    with open(weaver_filename, 'w') as weaver_file:
        json.dump(weaver_data, weaver_file)

def create_directory_and_move_files(output_frames):
    # 1. Generate a timestamp for naming
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # 2. Determine the appropriate save directory based on the OS
    if platform.system() == 'Windows':
        # For Windows, use the AppData directory
        base_directory = os.path.join(os.getenv('APPDATA'), 'HVstore')
    elif platform.system() == 'Linux':
        # For Linux, use ~/.local/share
        base_directory = os.path.join(os.path.expanduser('~'), '.local', 'share', 'HVstore')
    else:
        raise OSError("Unsupported operating system")

    # 3. Create the main directory if it doesn't exist
    os.makedirs(base_directory, exist_ok=True)

    # 4. Create a subdirectory with the naming schema drive_<timestamp>
    subdirectory_name = f"drive_{timestamp}"
    save_directory = os.path.join(base_directory, subdirectory_name)
    os.makedirs(save_directory, exist_ok=True)

    # 5. Move the contents of the output_frames to the new subdirectory
    for filename in os.listdir(output_frames):
        full_file_path = os.path.join(output_frames, filename)
        if os.path.isfile(full_file_path):
            shutil.move(full_file_path, save_directory)

    print(f"Files moved to: {save_directory}")

# Example usage:
def main(pipe_string):
    pygame.init()
    display = pygame.display.set_mode((800, 600), pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption("CARLA Manual Control")

    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.get_world()
    blueprint_library = world.get_blueprint_library()

    try:
        # Vehicle setup
        bd = blueprint_library.filter('vehicle.tesla.model3')[0]
        spawn_point = random.choice(world.get_map().get_spawn_points())
        vehicle = world.spawn_actor(bd, spawn_point)
        actor_list.append(vehicle)

        # Define the camera and LiDAR parameters
        camera_parameters = {
            'x': 0.15, 'y': 0.00, 'z': 1.65, 'roll': 0, 'pitch': -10, 'yaw': 0,
            'width': 800, 'height': 600, 'fov': 90,
            'sensor_label': 'camera', 'sensor_type': 'camera'
        }
        lidar_parameters = {
            'x': 0, 'y': 0, 'z': 2.0, 'roll': 0, 'pitch': 0, 'yaw': 0,
            'channels': 64, 'range': 100.0, 'lower_fov': -30, 'upper_fov': 30,
            'points_per_second': 640000, 'rotation_frequency': 30,
            'sensor_label': 'lidar', 'sensor_type': 'lidar'
        }

        # Attach sensors to the vehicle
        sensor_list = [camera_parameters, lidar_parameters]
        sensors, sensor_labels = sensor_factory(world, vehicle, sensor_list)
        actor_list.extend(sensors)

        # Variables for capturing and saving data
        frame_number = 0
        output_folder = "output_frames"
        os.makedirs(output_folder, exist_ok=True)

        # Timer for the drive
        start_time = time.time()

        # Main loop with CarlaSyncMode
        with CarlaSyncMode(world, sensors, fps=30) as sync_mode:
            pipe = bobTheBuilder.build_pipeline(pipe_string)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return

                # Get synchronized sensor data
                data = sync_mode.tick(timeout=2.0)
                latest_image, latest_lidar_data = data

                # Process the image
                image_array = process_image(latest_image)
                image_array_writable = np.copy(image_array)
                # processed_image_array, bounding_boxes = run_ai_model(image_array)

                # Process LiDAR data, including intensity
                latest_lidar_data_np = process_lidar_data(latest_lidar_data)
                pipe.dataToken.add_sensor_data('camera', image_array_writable)
                pipe.dataToken.add_sensor_data('lidar', latest_lidar_data_np)
                processed_image_array = pipe.process(pipe.dataToken)
                bounding_boxes = pipe.dataToken.get_processing_result('yoloUnit')
                
                # Integrate LiDAR data with the image and update world data
                # , world_data = integrate_lidar_with_image(processed_image_array,
                                                                                # latest_lidar_data_np, bounding_boxes)

                # Get vehicle transform (position and orientation)
                vehicle_transform = vehicle.get_transform()

                # Save frame and data, including the updated world data
                save_frame_and_data(processed_image_array, bounding_boxes, latest_lidar_data_np, frame_number,
                                    output_folder, vehicle_transform)

                # Save the world data to a JSON file
                # world_data_filename = os.path.join(output_folder, f"frame_{frame_number:06d}_world_data.json")
                # with open(world_data_filename, 'w') as world_data_file:
                #     json.dump(world_data, world_data_file, indent=4)

                # Display the processed image
                image_surface = convert_array_to_surface(processed_image_array)
                display.blit(image_surface, (0, 0))
                frame_number += 1

                pygame.display.flip()

                # Apply vehicle control (manual control)
                control = get_keyboard_control(vehicle)
                vehicle.apply_control(control)

                pygame.time.Clock().tick(30)
                

    finally:
        print('destroying actors')
        for actor in actor_list:
            if actor.is_alive:
                actor.destroy()

        # Calculate the actual FPS based on the number of frames and total time
        end_time = time.time()
        total_time = end_time - start_time
        calculated_fps = frame_number / total_time
        print(f"Calculated FPS: {calculated_fps}")

        # Stitch frames into a video
        video_filename = os.path.join(output_folder, "output_video.avi")
        stitch_video_from_frames(output_folder, video_filename, calculated_fps)
        create_directory_and_move_files("output_frames")
        print('done.')
        pygame.quit()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')
