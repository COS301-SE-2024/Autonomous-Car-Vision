import carla
import pygame
import numpy as np
import time
from ultralytics import YOLO
import cv2
import math

# Initialize Pygame
pygame.init()

# Define constants
IM_WIDTH = 640
IM_HEIGHT = 480
FPS = 10

# Global variable to control the mode
manual_mode = True

def main():
    global manual_mode

    # Connect to the CARLA server
    client = carla.Client('localhost', 2000)
    client.set_timeout(5.0)
    world = client.get_world()

    try:
        # Get the blueprint library and choose a vehicle
        blueprint_library = world.get_blueprint_library()
        vehicle_bp = blueprint_library.filter('etron')[0]

        # Spawn the vehicle at a specified location
        spawn_point = world.get_map().get_spawn_points()[5]
        vehicle = world.spawn_actor(vehicle_bp, spawn_point)

        # Add a camera sensor to the vehicle
        camera_bp = blueprint_library.find('sensor.camera.rgb')
        camera_bp.set_attribute('image_size_x', f'{IM_WIDTH}')
        camera_bp.set_attribute('image_size_y', f'{IM_HEIGHT}')
        camera_bp.set_attribute('fov', '110')
        camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
        camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)

        # Set up the display
        display = pygame.display.set_mode((IM_WIDTH, IM_HEIGHT))
        pygame.display.set_caption("CARLA Lane Following")
        clock = pygame.time.Clock()

        # Variables to store the camera image and control
        image_queue = []
        control = carla.VehicleControl()
        steer_value = 0.0

        # Load the lane detection model
        model = YOLO('laneTest.pt')

        # Callback function to process camera images
        def process_image(data):
            array = np.frombuffer(data.raw_data, dtype=np.uint8)
            array = array.reshape((IM_HEIGHT, IM_WIDTH, 4))
            array = array[:, :, :3]  # Remove alpha channel
            image_queue.append(array)

        # Start the camera
        camera.listen(lambda data: process_image(data))

        # Main loop
        while True:
            if len(image_queue) > 0:
                frame = image_queue.pop(0)
            else:
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return  # Exit the script
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        manual_mode = not manual_mode  # Switch modes
                    elif manual_mode:
                        if event.key == pygame.K_w:
                            control.throttle = 0.5
                        elif event.key == pygame.K_s:
                            control.brake = 0.5
                        elif event.key == pygame.K_a:
                            control.steer = -0.5
                        elif event.key == pygame.K_d:
                            control.steer = 0.5
                    else:
                        # In autonomous mode, reset manual controls
                        control.throttle = 0.0
                        control.brake = 0.0
                        control.steer = 0.0
                elif event.type == pygame.KEYUP:
                    if manual_mode:
                        if event.key == pygame.K_w or event.key == pygame.K_s:
                            control.throttle = 0.0
                            control.brake = 0.0
                        elif event.key == pygame.K_a or event.key == pygame.K_d:
                            control.steer = 0.0

            if manual_mode:
                # Manual driving mode
                # Display the camera frame
                surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                display.blit(surface, (0, 0))
            else:
                # Autonomous lane-following mode
                # Process the frame and get steering value
                processed_image, steer_value = start_following(frame, model)

                # Update vehicle control with the steer value
                control.steer = float(steer_value)
                control.throttle = 0.3  # Adjust the throttle value as needed

                # Display the processed image
                surface = pygame.surfarray.make_surface(processed_image.swapaxes(0, 1))
                display.blit(surface, (0, 0))

            # Apply the control to the vehicle
            vehicle.apply_control(control)

            # Update the display
            pygame.display.flip()
            clock.tick(FPS)

    finally:
        # Clean up
        camera.stop()
        vehicle.destroy()
        pygame.quit()

def filter_detections(results, model, image):
    height, width, channels = image.shape
    out_image = np.zeros((height, width, channels), dtype=np.uint8)
    filtered_results = []

    for result in results[0]:
        # Get the class index
        class_idx = int(result.boxes.cls)
        # Only process lane classes (assuming 3 and 4 are lane classes)
        if class_idx in [3, 4]:
            mask = result.masks.data.cpu().numpy()
            mask = np.squeeze(mask)
            if mask.size > 0:
                mask_resized = cv2.resize(mask, (width, height))
                binary_mask = (mask_resized > 0.5).astype(np.uint8)
                colored_mask = np.zeros_like(image, dtype=np.uint8)
                colored_mask[binary_mask == 1] = [255, 255, 255]
                out_image = cv2.addWeighted(out_image, 1, colored_mask, 0.5, 0)
                filtered_results.append(result)
            else:
                print("Empty mask encountered.")

    return out_image, filtered_results

def get_lines(filtered_results, image):
    output_image = image.copy()
    lines = []

    for result in filtered_results:
        mask = result.masks.data.cpu().numpy()
        mask = np.squeeze(mask)
        mask_resized = cv2.resize(mask, (image.shape[1], image.shape[0]))
        binary_mask = (mask_resized > 0.5).astype(np.uint8)

        # Find contours in the binary mask
        contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if len(contour) >= 2:
                # Fit a line to the contour points
                [vx, vy, x, y] = cv2.fitLine(contour, cv2.DIST_L2, 0, 0.01, 0.01)
                lefty = int((-x * vy / vx) + y)
                righty = int(((image.shape[1] - x) * vy / vx) + y)
                pt1 = (image.shape[1] - 1, righty)
                pt2 = (0, lefty)
                cv2.line(output_image, pt1, pt2, (0, 255, 0), 2)
                lines.append((pt1, pt2))

    return output_image, lines

def get_sides(image, lines, filtered_results, min_length):
    height, width, _ = image.shape
    center_x = width // 2

    closest_left_dist = float('inf')
    closest_right_dist = float('inf')
    left_line = None
    right_line = None

    # Helper function to calculate line length
    def calculate_line_length(line):
        pt1, pt2 = line
        return math.hypot(pt2[0] - pt1[0], pt2[1] - pt1[1])

    # Iterate over lines to find the closest left and right lines
    for i, line in enumerate(lines):
        if calculate_line_length(line) < min_length:
            continue

        pt1, pt2 = line
        x_coords = [pt1[0], pt2[0]]
        avg_x = sum(x_coords) / 2
        dist = abs(avg_x - center_x)

        if avg_x < center_x and dist < closest_left_dist:
            closest_left_dist = dist
            left_line = line
        elif avg_x > center_x and dist < closest_right_dist:
            closest_right_dist = dist
            right_line = line

    # Draw the closest left and right lines in blue
    out_image = image.copy()
    if left_line:
        cv2.line(out_image, left_line[0], left_line[1], (255, 0, 0), 2)
    if right_line:
        cv2.line(out_image, right_line[0], right_line[1], (255, 0, 0), 2)

    sides = {
        'left': {'line': left_line},
        'right': {'line': right_line}
    }

    return out_image, sides

def draw_trapezoid_mask(image, bottom_length, top_length):
    image_copy = image.copy()
    height, width, _ = image_copy.shape

    trapezoid_height = int(0.45 * height)
    bottom_y = height - 1
    top_y = bottom_y - trapezoid_height

    bottom_left = (int((width - bottom_length) / 2), bottom_y)
    bottom_right = (int((width + bottom_length) / 2), bottom_y)
    top_left = (int((width - top_length) / 2), top_y)
    top_right = (int((width + top_length) / 2), top_y)

    points = np.array([bottom_left, bottom_right, top_right, top_left], dtype=np.int32)
    mask = np.zeros_like(image_copy, dtype=np.uint8)
    cv2.fillPoly(mask, [points], (0, 255, 0))
    masked_image = cv2.addWeighted(image_copy, 1, mask, 0.5, 0)

    return masked_image, mask

def calculate_slope(point1, point2):
    if point1[0] == point2[0]:
        return float('inf')
    return (point2[1] - point1[1]) / (point2[0] - point1[0])

def calculate_angle_with_vertical(slope):
    if slope == float('inf'):
        return 0
    elif slope == 0:
        return 90
    else:
        angle_rad = math.atan(1 / abs(slope))
        angle_deg = math.degrees(angle_rad)
        return angle_deg

def get_values(sides, image):
    height, width, _ = image.shape
    center_x = width // 2

    left_object = {'angle': float('inf'), 'distance': float('inf')}
    right_object = {'angle': float('inf'), 'distance': float('inf')}

    # Process the left side
    left_line = sides['left']['line']
    if left_line:
        left_slope = calculate_slope(left_line[0], left_line[1])
        left_angle = calculate_angle_with_vertical(left_slope)
        if left_slope < 0:
            left_angle = -left_angle
        left_bottom_point = left_line[0] if left_line[0][1] > left_line[1][1] else left_line[1]
        left_distance = center_x - left_bottom_point[0]
        left_object = {'angle': left_angle, 'distance': left_distance}

    # Process the right side
    right_line = sides['right']['line']
    if right_line:
        right_slope = calculate_slope(right_line[0], right_line[1])
        right_angle = calculate_angle_with_vertical(right_slope)
        if right_slope > 0:
            right_angle = -right_angle
        right_bottom_point = right_line[0] if right_line[0][1] > right_line[1][1] else right_line[1]
        right_distance = right_bottom_point[0] - center_x
        right_object = {'angle': right_angle, 'distance': right_distance}

    return left_object, right_object

def analyze_results(left_object, right_object, bottom_length, top_length):
    steer = 0.0
    angle_steer = 0.0
    distance_steer = 0.0

    ANGLE_COEFFICIENT = 1 / 80
    DISTANCE_COEFFICIENT = 1 / (((bottom_length + top_length) / 2) * 300)

    angles = []
    weights = []

    if left_object['angle'] != float('inf'):
        angles.append(left_object['angle'])
        weights.append(1)
    if right_object['angle'] != float('inf'):
        angles.append(right_object['angle'])
        weights.append(1)

    if angles:
        avg_angle = sum(a * w for a, w in zip(angles, weights)) / sum(weights)
        angle_steer = -avg_angle * ANGLE_COEFFICIENT

    distances = []
    distance_weights = []

    if left_object['distance'] != float('inf'):
        distances.append(-left_object['distance'])
        distance_weights.append(1)
    if right_object['distance'] != float('inf'):
        distances.append(right_object['distance'])
        distance_weights.append(1)

    if distances:
        avg_distance = sum(d * w for d, w in zip(distances, distance_weights)) / sum(distance_weights)
        distance_steer = avg_distance * DISTANCE_COEFFICIENT

    steer = angle_steer + distance_steer
    steer = max(min(steer, 1.0), -1.0)

    return steer

def follow_lane(image, filtered_results):
    bottom_length = 600
    top_length = 70

    out_image, lines = get_lines(filtered_results, image)
    out_image, sides = get_sides(out_image, lines, filtered_results, min_length=25)
    out_image, _ = draw_trapezoid_mask(out_image, bottom_length, top_length)
    left_object, right_object = get_values(sides, image)
    steer = analyze_results(left_object, right_object, bottom_length, top_length)

    return out_image, steer

def start_following(frame, model):
    results = model(frame)
    out_image, filtered_results = filter_detections(results, model, frame)
    res, steer = follow_lane(frame, filtered_results)
    return res, steer

if __name__ == '__main__':
    main()
