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

follow_lane = False
lane_active = False
object_avoidance = False
avoid = False

reverse_toggle = False
reverse_gear = False

def get_wheel_input():
    steering = joystick.get_axis(0)
    
    throttle = (joystick.get_axis(1) + 1) / 2.0
    throttle = 1 - throttle
    
    brake = (joystick.get_axis(2) + 1) / 2.0 
    brake = 1 - brake 
    
    # Buttons
    buttons = []
    for i in range(joystick.get_numbuttons()):
        if joystick.get_button(i):
            buttons.append(i)
    
    return steering, throttle, brake, buttons

def get_wheel_control(vehicle):
    global follow_lane
    global object_avoidance
    global reverse_toggle
    global reverse_gear
    control = carla.VehicleControl()

    # keys = pygame.key.get_pressed()
    control = carla.VehicleControl()
    
    steering, throttle, brake, buttons = get_wheel_input()
    
    control.steer = steering
    control.throttle = throttle
    control.brake = brake

    # if not follow_lane:
    #     control.throttle = 1.0 if keys[pygame.K_w] else 0.0
    #     control.brake = 1.0 if keys[pygame.K_s] else 0.0
    #     control.steer = -1.0 if keys[pygame.K_a] else 1.0 if keys[pygame.K_d] else 0.0
    #     control.hand_brake = keys[pygame.K_SPACE]

    #     if keys[pygame.K_r] and not reverse_toggle:
    #         reverse_gear = not reverse_gear
    #         reverse_toggle = True

    #     if not keys[pygame.K_r]:
    #         reverse_toggle = False

    #     control.reverse = reverse_gear
    # else:
    #     control.throttle = 0.3

    # if keys[pygame.K_q] and lane_active:
    #     follow_lane = not follow_lane

    # if keys[pygame.K_o]:
    #     object_avoidance = not object_avoidance
    #     print("oooioioioioioioioioioioioioioioioioioioioi")

    return control


def process_image(image):
    array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
    array = np.reshape(array, (image.height, image.width, 4))
    array = array[:, :, :3]
    array = array[:, :, ::-1]
    return array


def run_ai_model(image_array):
    results = model(image_array)
    result_image = results[0].plot()
    return result_image, results[0].boxes.data.tolist()


def process_lidar_data(lidar_measurement):
    points = np.frombuffer(lidar_measurement.raw_data, dtype=np.dtype('f4'))
    lidar_data_np = np.reshape(points, (int(points.shape[0] / 4), 4))
    return lidar_data_np


def convert_array_to_surface(image_array):
    surface = pygame.surfarray.make_surface(image_array.swapaxes(0, 1))
    return surface


def stitch_video_from_frames(output_folder, video_filename, calculated_fps):
    if not video_filename.endswith(".mp4"):
        video_filename += ".mp4"

    images = [img for img in sorted(os.listdir(output_folder)) if img.endswith(".png")]
    if not images:
        print("No images found in the folder.")
        return

    first_frame = imageio.imread(os.path.join(output_folder, images[0]))
    height, width = first_frame.shape[:2]

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
            continue

        transform = carla.Transform(carla.Location(x=params['x'], y=params['y'], z=params['z']),
                                    carla.Rotation(roll=params['roll'], pitch=params['pitch'], yaw=params['yaw']))
        sensor = world.spawn_actor(sensor_bp, transform, attach_to=vehicle)
        sensors.append(sensor)
        sensor_labels.append(params['sensor_label'])

    return sensors, sensor_labels


def integrate_lidar_with_image(image, lidar_data, bounding_boxes):
    image_height, image_width, _ = image.shape

    x = lidar_data[:, 0]
    y = lidar_data[:, 1]
    z = lidar_data[:, 2]

    r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    theta = np.arctan2(y, x)
    phi = np.arcsin(z / r)

    horizontal_fov = np.radians(90 / 2)
    vertical_fov = np.radians(60 / 2)

    fov_mask = (np.abs(theta) <= horizontal_fov) & (np.abs(phi) <= vertical_fov)
    filtered_data = lidar_data[fov_mask]
    filtered_r = r[fov_mask]
    
    if filtered_r.size == 0:
        return image, []

    x_filtered = filtered_data[:, 0]
    y_filtered = filtered_data[:, 1]
    z_filtered = filtered_data[:, 2]

    indices_in_fov = np.where(fov_mask)[0]
    world_positions = filtered_data

    focal_length = image_width / (2 * np.tan(horizontal_fov))
    principal_point = np.array([image_width / 2, image_height / 2])

    angle_y = np.radians(-10)
    R = np.array([
        [np.cos(angle_y), 0, np.sin(angle_y)],
        [0, 1, 0],
        [-np.sin(angle_y), 0, np.cos(angle_y)]
    ])

    t = np.array([0.0, 0.0, 0.2])

    points_lidar = np.vstack((x_filtered, y_filtered, z_filtered))
    points_camera = R @ points_lidar + t[:, np.newaxis]

    pixel_x = (focal_length * points_camera[1, :] / points_camera[0, :]) + principal_point[0]
    pixel_y = (focal_length * (-points_camera[2, :] / points_camera[0, :])) + principal_point[1]

    valid_pixels_mask = (pixel_x >= 0) & (pixel_x < image_width) & (pixel_y >= 0) & (pixel_y < image_height)
    pixel_x = pixel_x[valid_pixels_mask].astype(int)
    pixel_y = pixel_y[valid_pixels_mask].astype(int)
    filtered_r = filtered_r[valid_pixels_mask]

    valid_indices = indices_in_fov[valid_pixels_mask]
    valid_world_positions = world_positions[valid_pixels_mask]

    norm = plt.Normalize(vmin=filtered_r.min(), vmax=filtered_r.max())
    cmap = plt.colormaps.get_cmap('plasma')
    colors = cmap(norm(filtered_r))[:, :3]
    colors = (colors * 255).astype(int) 

    for i in range(len(pixel_x)):
        color = (int(colors[i][2]), int(colors[i][1]), int(colors[i][0]))
        cv2.circle(image, (pixel_x[i], pixel_y[i]), radius=2, color=color, thickness=-1)
        
    world_data = []

    for bbox in bounding_boxes:
        x_min, y_min, x_max, y_max, score, class_id = bbox
        x_min, y_min, x_max, y_max = int(x_min), int(y_min), int(x_max), int(y_max)

        inside_bbox_mask = (pixel_x >= x_min) & (pixel_x <= x_max) & (pixel_y >= y_min) & (pixel_y <= y_max)
        if np.any(inside_bbox_mask):
            min_distance_idx = np.argmin(filtered_r[inside_bbox_mask])
            min_distance = filtered_r[inside_bbox_mask][min_distance_idx]
            world_position = valid_world_positions[inside_bbox_mask][min_distance_idx]

            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

            region_points = [world_position]

            local_world_positions = valid_world_positions[inside_bbox_mask]
            local_region_mask = np.zeros(local_world_positions.shape[0], dtype=bool)
            local_region_mask[min_distance_idx] = True

            distance_limit = min_distance / 10

            while True:
                current_region_size = len(region_points)
                for i, wp in enumerate(local_world_positions):
                    if not local_region_mask[i]: 
                        if np.any(np.linalg.norm(np.array(region_points) - wp, axis=1) < distance_limit):
                            region_points.append(wp)
                            local_region_mask[i] = True
                if len(region_points) == current_region_size:
                    break

            region_pixel_x = pixel_x[inside_bbox_mask][local_region_mask]
            region_pixel_y = pixel_y[inside_bbox_mask][local_region_mask]

            for i in range(len(region_pixel_x)):
                cv2.circle(image, (region_pixel_x[i], region_pixel_y[i]), radius=2, color=(0, 255, 0), thickness=-1)

            if len(local_world_positions[local_region_mask]) >= 2:
                pca = PCA(n_components=2)
                pca.fit(local_world_positions[local_region_mask])
                orientation_vector = pca.components_[0]

                orientation_angle = np.arctan2(orientation_vector[1], orientation_vector[0])

                text = f"Object: {min_distance:.2f}m, θ: {np.degrees(orientation_angle):.1f}°"
                cv2.putText(image, text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                world_data.append({
                    "label": "object",
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
                    "label": "object",
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


def save_frame_and_data(image_array, bounding_boxes, lidar_data, frame_number, output_folder, vehicle_transform, raw):
    # Save the processed image
    filename = os.path.join(output_folder, f"frame_{frame_number:06d}_raw.png")
    cv2.imwrite(filename, cv2.cvtColor(raw, cv2.COLOR_RGB2BGR))

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
    
joystick = None
for i in range(pygame.joystick.get_count()):
    j = pygame.joystick.Joystick(i)
    j.init()
    print(f"Joystick {i}: {j.get_name()}")
    if "Logitech G HUB G920 Driving Force Racing Wheel USB" in j.get_name():
        joystick = j
        print(f"Found {joystick.get_name()}!")
        break

def main(pipe):
    global lane_active
    global avoid
    pygame.init()
    display = pygame.display.set_mode((800, 600), pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption("CARLA Manual Control")
    
    pygame.font.init()
    font = pygame.font.Font(None, 36)

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
            'channels': 64, 'range': 60, 'lower_fov': -30, 'upper_fov': 30,
            'points_per_second': 150000, 'rotation_frequency': 50,
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

        start_time = time.time()
        pipestring = pipe
        
        if 'laneUnit' in pipestring:
            lane_active = True
        if 'observerUnit' in pipestring:
            avoid = True

        with CarlaSyncMode(world, sensors, fps=30) as sync_mode:
            pipe = bobTheBuilder.build_pipeline(pipestring)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return

                data = sync_mode.tick(timeout=2.0)
                latest_image, latest_lidar_data = data

                image_array = process_image(latest_image)
                image_array_writable = np.copy(image_array)
  
                latest_lidar_data_np = process_lidar_data(latest_lidar_data)
                pipe.dataToken.add_sensor_data('camera', image_array_writable)
                pipe.dataToken.add_sensor_data('lidar', latest_lidar_data_np)
                processed_image_array, img_lidar, img_taggr, img_bb, img_la = pipe.process(pipe.dataToken)
                bounding_boxes = pipe.dataToken.get_processing_result('yoloUnit')

                vehicle_transform = vehicle.get_transform()

                save_frame_and_data(processed_image_array, bounding_boxes, latest_lidar_data_np, frame_number,
                                    output_folder, vehicle_transform, image_array)

                image_surface = convert_array_to_surface(processed_image_array)
                display.blit(image_surface, (0, 0))
                
                if pipe.dataToken.get_flag("hasObeserverData") and object_avoidance:
                    text_surface = font.render("Object avoidance on", True, (0, 255, 0))  # Green text
                    display.blit(text_surface, (10, 10))
                    
                frame_number += 1

                pygame.display.flip()

                # Apply vehicle control (manual control)
                control = get_wheel_control(vehicle)

                if pipe.dataToken.get_flag("hasObeserverData") and object_avoidance:
                    print("avoiding")
                    observerToken = pipe.dataToken.get_processing_result('observerUnit')
                    breaking = observerToken['breaking']
                    handbreak = observerToken['handBreak']
                    if breaking > 0 or handbreak:
                        control.throttle = 0

                    control.brake = breaking
                    control.hand_brake = handbreak
                    print(vehicle.get_velocity().x)
                    if (vehicle.get_velocity().x < 2 or vehicle.get_velocity().x > 2) and breaking > 0:
                        control.hand_brake = True
                        control.breaking = 1
                if (follow_lane):
                    output = pipe.dataToken.get_processing_result('laneUnit')
                    steer = output['steer']
                    control.steer = steer

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


        video_filename = os.path.join(output_folder, "output_video.avi")
        stitch_video_from_frames(output_folder, video_filename, calculated_fps)
        create_directory_and_move_files("output_frames")
        print('done.')
        pygame.quit()

if __name__ == '__main__':
    try:
        if len(sys.argv) > 1:
            pipe_argument = sys.argv[1]
        else:
            print("No pipe argument provided. Exiting...")
            sys.exit(1)

        main(pipe_argument)
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')