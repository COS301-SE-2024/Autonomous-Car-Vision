import carla
import pygame
import numpy as np
import time
import threading
from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import numpy as np
import math
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

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

        # Spawn the vehicle at a random location
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
                # Pass the frame and previous variables to start_following function
                processed_image, steer_value = start_following(frame)

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

model = YOLO('laneTest.pt')

def filter_detections(results, model, image):
    height, width, channels = image.shape
    out_image = np.zeros((height, width, channels), dtype=np.uint8)
    filtered_results = []  # Store filtered results
    
    for result in results[0]:
        # Get the name of the detected class
        class_name = model.names[int(result.boxes.cls)]
        
        if int(result.boxes.cls) != 4 and int(result.boxes.cls) != 3:  # Filter based on specific classes (not lanes)
            mask = result.masks.data.cpu().numpy()  # Get the mask for the detected object
            
            # If there are extra dimensions, squeeze the mask
            mask = np.squeeze(mask)  # This removes extra dimensions like [1, h, w] -> [h, w]
            
            # Check if mask is non-empty before resizing
            if mask.size > 0:
                mask_resized = cv2.resize(mask, (image.shape[1], image.shape[0]))

                # Convert the mask into a binary mask (thresholding)
                binary_mask = (mask_resized > 0.5).astype(np.uint8)  # Thresholding mask

                # Create a colored version of the mask (e.g., green for lanes)
                colored_mask = np.zeros_like(image, dtype=np.uint8)
                colored_mask[binary_mask == 1] = [255, 255, 255]  # White color for lane

                # Add the mask to the output image
                out_image = cv2.addWeighted(out_image, 1, colored_mask, 0.5, 0)
                
                # Add this result to the filtered list
                filtered_results.append(result)
            else:
                print("Empty mask encountered.")
    
    return out_image, filtered_results

def get_lines(filtered_results, image):
    output_image = image.copy()  # Create a copy of the original image to draw on
    lines = []  # Array to store the lines as tuples of (start_point, end_point)
    
    for result in filtered_results:
        # Extract the binary mask from the result
        mask = result.masks.data.cpu().numpy()
        mask = np.squeeze(mask)  # Remove extra dimensions if any
        mask_resized = cv2.resize(mask, (image.shape[1], image.shape[0]))
        binary_mask = (mask_resized > 0.5).astype(np.uint8)  # Convert to binary mask

        # Find contours in the binary mask
        contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            if len(contour) >= 2:  # Ensure there are enough points to fit a line
                # Fit a straight line to the contour points
                [vx, vy, x, y] = cv2.fitLine(contour, cv2.DIST_L2, 0, 0.01, 0.01)
                
                # Get the bounding box of the contour
                x_min, y_min, w, h = cv2.boundingRect(contour)
                x_max = x_min + w
                y_max = y_min + h
                
                # Calculate the intersection points of the fitted line with the bounding box
                def compute_intersection(x_start, y_start, vx, vy, x_min, x_max, y_min, y_max):
                    points = []

                    # Handle vertical lines (vx == 0)
                    if vx == 0:
                        x_bound = x_start
                        # Intersection with horizontal boundaries
                        for y_bound in [y_min, y_max]:
                            if y_min <= y_bound <= y_max:
                                points.append((int(x_bound), int(y_bound)))
                    else:
                        # Intersection with vertical boundaries (x_min and x_max)
                        for x_bound in [x_min, x_max]:
                            y_bound = vy / vx * (x_bound - x_start) + y_start
                            if y_min <= y_bound <= y_max:
                                points.append((int(x_bound), int(y_bound)))

                    # Handle horizontal lines (vy == 0)
                    if vy == 0:
                        y_bound = y_start
                        # Intersection with vertical boundaries
                        for x_bound in [x_min, x_max]:
                            if x_min <= x_bound <= x_max:
                                points.append((int(x_bound), int(y_bound)))
                    else:
                        # Intersection with horizontal boundaries (y_min and y_max)
                        for y_bound in [y_min, y_max]:
                            x_bound = vx / vy * (y_bound - y_start) + x_start
                            if x_min <= x_bound <= x_max:
                                points.append((int(x_bound), int(y_bound)))

                    return points

                # Calculate the intersection points of the fitted line with the bounding box
                intersections = compute_intersection(x, y, vx, vy, x_min, x_max, y_min, y_max)
                
                if len(intersections) >= 2:
                    # Sort intersections to get consistent line endpoints
                    intersections = sorted(intersections, key=lambda pt: (pt[0], pt[1]))
                    pt1, pt2 = intersections[0], intersections[1]
                    
                    # Draw the line within the contour bounding box
                    cv2.line(output_image, pt1, pt2, (0, 255, 0), 2)
                    
                    # Append the line (start and end points) to the array
                    lines.append((pt1, pt2))
        
    return output_image, lines

def get_sides(image, lines, filtered_results, min_length):
    height, width, _ = image.shape
    center_x = width // 2
    center_bottom = (center_x, height - 1)  # Bottom center of the image

    closest_left = None
    closest_right = None
    closest_left_dist = float('inf')
    closest_right_dist = float('inf')

    left_result = None
    right_result = None
    left_line = None
    right_line = None

    # Helper function to calculate the length of a line (Euclidean distance)
    def calculate_line_length(line):
        pt1, pt2 = line
        return math.sqrt((pt2[0] - pt1[0]) ** 2 + (pt2[1] - pt1[1]) ** 2)

    # Iterate over each result to find the closest left and right
    for i, result in enumerate(filtered_results):
        mask = result.masks.data.cpu().numpy()
        mask = np.squeeze(mask)  # Remove extra dimensions if any
        mask_resized = cv2.resize(mask, (image.shape[1], image.shape[0]))
        binary_mask = (mask_resized > 0.5).astype(np.uint8)  # Convert to binary mask

        # Find the contour to get all points
        contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Check if there's an associated line and if its length is greater than the min_length
            if i < len(lines) and calculate_line_length(lines[i]) >= min_length:
                # Iterate through all points to find the closest point to the center bottom
                closest_point = None
                min_distance = float('inf')

                for contour in contours:
                    for point in contour:
                        pt = point[0]  # Get the x, y coordinates from the contour point
                        dist = math.sqrt((pt[0] - center_bottom[0]) ** 2 + (pt[1] - center_bottom[1]) ** 2)

                        if dist < min_distance:
                            min_distance = dist
                            closest_point = pt

                # Now, depending on whether the point is to the left or right of the center
                if closest_point is not None:
                    if closest_point[0] < center_x and min_distance < closest_left_dist:
                        closest_left_dist = min_distance
                        closest_left = result
                        left_result = result
                        left_line = lines[i]  # Line is valid since its length >= min_length
                    elif closest_point[0] > center_x and min_distance < closest_right_dist:
                        closest_right_dist = min_distance
                        closest_right = result
                        right_result = result
                        right_line = lines[i]  # Line is valid since its length >= min_length

    # Create a copy of the image to draw the closest results on
    out_image = image.copy()

    # Draw the closest left and right results in blue
    if closest_left is not None:
        mask = closest_left.masks.data.cpu().numpy()
        mask = np.squeeze(mask)
        mask_resized = cv2.resize(mask, (image.shape[1], image.shape[0]))
        binary_mask = (mask_resized > 0.5).astype(np.uint8)
        colored_mask = np.zeros_like(image, dtype=np.uint8)
        colored_mask[binary_mask == 1] = [255, 0, 0]  # Blue color for left result
        out_image = cv2.addWeighted(out_image, 1, colored_mask, 0.5, 0)

    if closest_right is not None:
        mask = closest_right.masks.data.cpu().numpy()
        mask = np.squeeze(mask)
        mask_resized = cv2.resize(mask, (image.shape[1], image.shape[0]))
        binary_mask = (mask_resized > 0.5).astype(np.uint8)
        colored_mask = np.zeros_like(image, dtype=np.uint8)
        colored_mask[binary_mask == 1] = [255, 0, 0]  # Blue color for right result
        out_image = cv2.addWeighted(out_image, 1, colored_mask, 0.5, 0)

    # Prepare the result object with the left and right results and lines
    sides = {
        'left': {
            'result': left_result,
            'line': left_line
        },
        'right': {
            'result': right_result,
            'line': right_line
        }
    }

    return out_image, sides, filtered_results, lines

def draw_trapezoid_mask(image, bottom_length, top_length):
    # Make a copy of the image to work on, so the original image is not modified
    image_copy = image.copy()
    
    height, width, _ = image_copy.shape
    
    # Calculate the trapezoid's height as 20% of the image height
    trapezoid_height = int(0.25 * height)
    
    # Bottom rectangle
    bottom_y = height - 1
    top_y = bottom_y - trapezoid_height

    # Calculate the left and right positions for both the top and bottom of the trapezoid
    bottom_left = (int((width - bottom_length) / 2), bottom_y)
    bottom_right = (int((width + bottom_length) / 2), bottom_y)
    top_left = (int((width - top_length) / 2), top_y)
    top_right = (int((width + top_length) / 2), top_y)

    # Define the trapezoid points
    points = np.array([bottom_left, bottom_right, top_right, top_left], dtype=np.int32)
    
    # Create an empty mask
    mask = np.zeros_like(image_copy, dtype=np.uint8)
    
    # Draw the filled trapezoid in green (BGR color: 0, 255, 0)
    cv2.fillPoly(mask, [points], (0, 255, 0))  # Green color
    
    # Overlay the green trapezoid mask on the image copy
    masked_image = cv2.addWeighted(image_copy, 1, mask, 0.5, 0)  # Adjust transparency with 0.5 alpha
    
    return masked_image, mask

def calculate_slope(point1, point2):
    """Helper function to calculate the slope of a line given two points."""
    if point1[0] == point2[0]:  # Vertical line, infinite slope
        return float('inf')
    return (point2[1] - point1[1]) / (point2[0] - point1[0])

def calculate_angle(slope1, slope2):
    if slope1 == slope2:  # If the slopes are identical, the angle is zero
        return 0
    
    # Calculate the angle in radians between the two slopes
    angle_rad = math.atan(abs((slope2 - slope1) / (1 + slope1 * slope2)))
    
    # Convert to degrees
    angle_deg = math.degrees(angle_rad)
    
    return angle_deg

def get_values(mask, sides):
    height, width, _ = mask.shape
    
    # Trapezoid dimensions (matching draw_trapezoid_mask)
    bottom_length = 600
    top_length = 220
    trapezoid_height = int(0.25 * height)
    
    # Define trapezoid edges (left and right) using the mask's corners
    bottom_y = height - 1
    top_y = bottom_y - trapezoid_height
    
    # Calculate the positions of the trapezoid's edges
    bottom_left = (int((width - bottom_length) / 2), bottom_y)
    bottom_right = (int((width + bottom_length) / 2), bottom_y)
    top_left = (int((width - top_length) / 2), top_y)
    top_right = (int((width + top_length) / 2), top_y)
    
    # Get the left and right edge slopes of the trapezoid mask
    trapezoid_left_slope = calculate_slope(bottom_left, top_left)
    trapezoid_right_slope = calculate_slope(bottom_right, top_right)
    
    left_object = {'angle': float('inf'), 'distance': float('inf')}
    right_object = {'angle': float('inf'), 'distance': float('inf')}
    
    # Get the left and right lane lines from sides
    left_line = sides['left']['line']
    right_line = sides['right']['line']

    # Process the left side
    if left_line:
        left_slope = calculate_slope(left_line[0], left_line[1])
        left_angle = calculate_angle(trapezoid_left_slope, left_slope)
        
        # Determine sign of the angle
        if left_slope > trapezoid_left_slope:
            left_angle = -left_angle  # Trapezoid edge is more left-leaning
        
        # Calculate horizontal distance difference between bottom of trapezoid and left lane
        if bottom_left[0] > left_line[0][0]:
            left_distance = abs(bottom_left[0] - left_line[0][0])  # Positive if left edge is to the right
        else:
            left_distance = -abs(bottom_left[0] - left_line[0][0])  # Negative if left edge is to the left
        
        # Update left object
        left_object = {'angle': left_angle, 'distance': left_distance}
    
    # Process the right side
    if right_line:
        right_slope = calculate_slope(right_line[0], right_line[1])
        right_angle = calculate_angle(trapezoid_right_slope, right_slope)
        
        # Determine sign of the angle
        if right_slope > trapezoid_right_slope:
            right_angle = -right_angle  # Trapezoid edge is more left-leaning
        
        # Calculate horizontal distance difference between bottom of trapezoid and right lane
        if bottom_right[0] < right_line[0][0]:
            right_distance = abs(bottom_right[0] - right_line[0][0])  # Positive if right edge is to the left
        else:
            right_distance = -abs(bottom_right[0] - right_line[0][0])  # Negative if right edge is to the right
        
        # Update right object
        right_object = {'angle': right_angle, 'distance': right_distance}

    return left_object, right_object

def analise_results(left_object, right_object, bottom_length, top_length):
    steer = 0
    if left_object['angle'] != float('inf') and right_object['angle'] != float('inf'):
        avg_angle = (left_object['angle'] + right_object['angle']) / 2
        
        angle_steer = -avg_angle / 80
        
        steer = angle_steer
    elif right_object['angle'] == float('inf'):
        angle_steer = -left_object['angle'] / 80
        
        steer = angle_steer
    elif left_object['angle'] == float('inf'):
        angle_steer = -right_object['angle'] / 80
        
        steer = angle_steer
        
    if left_object['distance'] != float('inf') and right_object['distance'] != float('inf'):
        distance_steer = 0
        
        if (left_object['distance'] <= 0 and right_object['distance'] <= 0):
            distance_steer = 0
        elif (left_object['distance'] > 0 and right_object['distance'] <= 0):
            distance_steer = -left_object['distance'] / (((bottom_length + top_length) / 2) * 100)
        elif (left_object['distance'] <= 0 and right_object['distance'] > 0):
            distance_steer = right_object['distance'] / (((bottom_length + top_length) / 2) * 100)
        
        steer += distance_steer
    elif right_object['distance'] == float('inf'):
        distance_steer = 0
        
        if left_object['distance'] <= 0:
            distance_steer = left_object['distance'] / (((bottom_length + top_length) / 2) * 100)
        else:
            distance_steer = -left_object['distance'] / (((bottom_length + top_length) / 2) * 100)
        
        steer += distance_steer
    elif left_object['distance'] == float('inf'):
        distance_steer = 0
        
        if right_object['distance'] <= 0:
            distance_steer = -right_object['distance'] / (((bottom_length + top_length) / 2) * 100)
        else:
            distance_steer = right_object['distance'] / (((bottom_length + top_length) / 2) * 100)
        
        steer += distance_steer
    
    return steer

def follow_lane(out_image, filtered_results, original_image):
    bottom_length = 600
    top_length = 220
    
    out_image, lines = get_lines(filtered_results, out_image)
    out_image, sides, filtered_results, lines = get_sides(out_image, lines, filtered_results, 25)
    out_image, mask = draw_trapezoid_mask(out_image, bottom_length, top_length)
    
    left_object, right_object = get_values(mask, sides)
    
    steer = analise_results(left_object, right_object, bottom_length, top_length)
    
    # print(left_object, right_object)
    
    return out_image, steer 

def start_following(frame):
    results = model(frame)
    out_image, filtered_results = filter_detections(results, model, frame)
    res, steer = follow_lane(out_image, filtered_results, frame)
    return res, steer

# cap = cv2.VideoCapture('test_short.mp4')

if __name__ == '__main__':
    main()
