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
o_key_toggle = False

joystick = None

def get_wheel_input():
    global joystick
    if joystick is None:
        return 0, 0, 0, []
    # Axis 0: Steering wheel (-1 to 1)
    steering = joystick.get_axis(0)

    throttle = (joystick.get_axis(1) + 1) / 2.0  # Normalize to 0 to 1
    throttle = 1 - throttle  # Flip throttle value (0 is at the bottom, 1 is at the top)
    throttle = throttle/2
    brake = (joystick.get_axis(2) + 1) / 2.0  # Normalize to 0 to 1
    brake = 1 - brake  # Flip brake value (0 is at the bottom, 1 is at the top)

    # Buttons
    buttons = []
    for i in range(joystick.get_numbuttons()):
        if joystick.get_button(i):
            buttons.append(i)

    return steering, throttle, brake, buttons

def get_keyboard_control(vehicle):
    # Toggle lane following with Q
    global follow_lane
    global object_avoidance
    global reverse_toggle
    global reverse_gear
    global o_key_toggle
    control = carla.VehicleControl()

    keys = pygame.key.get_pressed()
    control = carla.VehicleControl()

    steering, throttle, brake, buttons = get_wheel_input()

    if brake < 0.01:
        brake = 0



    if not follow_lane:
        control.throttle = throttle
        control.brake = brake
        control.hand_brake = False
        control.steer = steering

        if 5 in buttons and not reverse_toggle:
            reverse_gear = not reverse_gear
            reverse_toggle = True

        if 5 not in buttons:
            reverse_toggle = False

        control.reverse = reverse_gear
    else:
        control.throttle = 0.3

    if 1 in buttons and lane_active:
        follow_lane = not follow_lane

    if 3 in buttons and not o_key_toggle:
        object_avoidance = not object_avoidance
        print("Object avoidance:", object_avoidance)
        o_key_toggle = True

    if 3 not in buttons:
        o_key_toggle = False

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
    # Ensure the output file is in MP4 format
    if not video_filename.endswith(".mp4"):
        video_filename += ".mp4"

    images = [img for img in sorted(os.listdir(output_folder)) if img.endswith(".png")]
    if not images:
        print("No images found in the folder.")
        return

    # Assuming all images have the same resolution
    first_frame = imageio.imread(os.path.join(output_folder, images[0]))
    height, width = first_frame.shape[:2]

    # Create a writer object using imageio for MP4 format
    writer = imageio.get_writer(video_filename, fps=calculated_fps, codec='libx264', pixelformat='yuv420p')

    # Append each frame to the video
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


# Example usage:
def main(pipe):
    global lane_active
    global avoid
    global joystick
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

        for i in range(pygame.joystick.get_count()):
            j = pygame.joystick.Joystick(i)
            j.init()
            print(f"Joystick {i}: {j.get_name()}")
            if "Logitech G HUB G920 Driving Force Racing Wheel USB" in j.get_name():
                joystick = j
                print(f"Found {joystick.get_name()}!")
                break

        if not joystick:
            print("No Logitech G920 found. Exiting...")
            vehicle.destroy()
            sys.exit()

        # Define the camera and LiDAR parameters
        camera_parameters = {
            'x': 0.15, 'y': 0.00, 'z': 1.65, 'roll': 0, 'pitch': -10, 'yaw': 0,
            'width': 800, 'height': 600, 'fov': 90,
            'sensor_label': 'camera', 'sensor_type': 'camera'
        }
        camera_two_parameters = {
            'x': 2.0, 'y': 0.00, 'z': 1, 'roll': 0, 'pitch': -10, 'yaw': 0,
            'width': 800, 'height': 600, 'fov': 60,
            'sensor_label': 'camera', 'sensor_type': 'camera'
        }
        lidar_parameters = {
            'x': 0, 'y': 0, 'z': 2.0, 'roll': 0, 'pitch': 0, 'yaw': 0,
            'channels': 32, 'range': 60, 'lower_fov': -30, 'upper_fov': 30,
            'points_per_second': 56000, 'rotation_frequency': 10,
            'sensor_label': 'lidar', 'sensor_type': 'lidar'
        }

        # Attach sensors to the vehicle
        sensor_list = [camera_parameters, camera_two_parameters, lidar_parameters]
        sensors, sensor_labels = sensor_factory(world, vehicle, sensor_list)
        actor_list.extend(sensors)

        # Variables for capturing and saving data
        frame_number = 0
        output_folder = "output_frames"
        os.makedirs(output_folder, exist_ok=True)

        # Timer for the drive
        start_time = time.time()
        pipestring = pipe
        # If pipestrign contains 'laneUnit', set lane_active to True
        if 'laneUnit' in pipestring:
            lane_active = True
        if 'observerUnit' in pipestring:
            avoid = True

        # Main loop with CarlaSyncMode
        with CarlaSyncMode(world, sensors, fps=30) as sync_mode:
            pipe = bobTheBuilder.build_pipeline(pipestring)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return

                # Get synchronized sensor data
                data = sync_mode.tick(timeout=2.0)
                latest_image, latest_image_two, latest_lidar_data = data

                # Process the image
                image_array = process_image(latest_image)
                image_array_writable = np.copy(image_array)

                image_array_two = process_image(latest_image_two)
                image_array_writable_two = np.copy(image_array_two)
                # processed_image_array, bounding_boxes = run_ai_model(image_array)

                # Process LiDAR data, including intensity
                latest_lidar_data_np = process_lidar_data(latest_lidar_data)
                pipe.dataToken.add_processing_result('velocityUnit',vehicle.get_velocity().x)
                pipe.dataToken.add_sensor_data('camera', image_array_writable)
                pipe.dataToken.add_sensor_data('camera_two', image_array_writable_two)
                pipe.dataToken.add_sensor_data('lidar', latest_lidar_data_np)
                processed_image_array, img_lidar, img_taggr, img_bb, img_la = pipe.process(pipe.dataToken)
                bounding_boxes = pipe.dataToken.get_processing_result('yoloUnit')

                # Integrate LiDAR data with the image and update world data
                # , world_data = integrate_lidar_with_image(processed_image_array,
                # latest_lidar_data_np, bounding_boxes)

                # Get vehicle transform (position and orientation)
                vehicle_transform = vehicle.get_transform()

                # Save frame and data, including the updated world data
                # save_frame_and_data(processed_image_array, bounding_boxes, latest_lidar_data_np, frame_number,
                #                     output_folder, vehicle_transform, image_array)

                # Save the world data to a JSON file
                # world_data_filename = os.path.join(output_folder, f"frame_{frame_number:06d}_world_data.json")
                # with open(world_data_filename, 'w') as world_data_file:
                #     json.dump(world_data, world_data_file, indent=4)

                # Display the processed image
                image_surface = convert_array_to_surface(img_la)
                display.blit(image_surface, (0, 0))

                if pipe.dataToken.get_flag("hasObserverData") and object_avoidance:
                    # Render the text "Object avoidance on"
                    text_surface = font.render("Object avoidance on", True, (0, 255, 0))  # Green text
                    display.blit(text_surface, (10, 10))
                    velocity_text = f"Velocity: {abs(vehicle.get_velocity().x):.2f}"  # Format the velocity to 2 decimal places
                    text_surface = font.render(velocity_text, True, (0, 255, 0))
                    display.blit(text_surface, (10, 30))

                frame_number += 1



                # Apply vehicle control (manual control)
                control = get_keyboard_control(vehicle)
                # print(object_avoidance)
                # print( pipe.dataToken.get_flag("hasObserverData"))
                # print("flag:", pipe.dataToken.get_flag("hasObserverData"))
                # print("avoidance:", object_avoidance)
                if pipe.dataToken.get_flag("hasObserverData") and object_avoidance:
                    print("avoiding")

                    observerToken = pipe.dataToken.get_processing_result('observerUnit')
                    x_text = f"avgX: {observerToken['avgX']:.2f}"
                    print(x_text)
                    text_surface = font.render(x_text, True, (0, 255, 0))  # Green text
                    display.blit(text_surface, (10, 50))
                    breaking = observerToken['breaking']
                    handbreak = observerToken['handBreak']
                    if breaking > 0 or handbreak:
                        control.throttle = 0

                    control.brake = breaking
                    control.hand_brake = handbreak
                    # print(vehicle.get_velocity().x)
                    if (vehicle.get_velocity().x < 2 or vehicle.get_velocity().x > 2) and breaking > 0:
                        control.hand_brake = True
                if (follow_lane):
                    output = pipe.dataToken.get_processing_result('laneUnit')
                    steer = output['steer']
                    control.steer = steer
                    text_surface = font.render(f"Lane Following is on, Steer: {steer}", True, (0, 255, 0))
                    display.blit(text_surface, (10, 10))

                pygame.display.flip()

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

        # video_filename = os.path.join(output_folder, "output_video.avi")
        # stitch_video_from_frames(output_folder, video_filename, calculated_fps)
        # create_directory_and_move_files("output_frames")
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
