from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
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
from collections import defaultdict

# Load the trained model
model = YOLO('laneTest.pt')  # Replace with the path to your trained model

# Run inference on an image
# img_path = './test_images/solidWhiteRight.jpg'
# img_path = 'Road-Markings.webp'
# img_path = 'frame_000008_raw.png'
img_path = 'img_2.png'
# img_path = 'thirteen.jpg'
results = model(img_path)  # Perform inference

print(model.names)

# Load the original image
image = cv2.imread(img_path)
height, width, channels = image.shape
out_image = np.zeros((height, width, channels), dtype=np.uint8)


def filter_detections(results, model, image):
    height, width, channels = image.shape
    out_image = np.zeros((height, width, channels), dtype=np.uint8)
    filtered_results = []  # Store filtered results

    # Iterate over the results generator
    for result in results:
        # Assuming result.boxes.cls and result.boxes.conf could be tensors with multiple values
        for i in range(len(result.boxes.cls)):
            class_id = int(result.boxes.cls[i].item())  # Extract the scalar value for class ID
            confidence = result.boxes.conf[i].item()  # Extract the scalar value for confidence

            # Check if the detected class is not 0, 3, or 4 and confidence is greater than 0.5
            if class_id not in [0, 3, 4] and confidence > 0.5:
                # Get the mask for the detected object
                mask = result.masks.data[i].cpu().numpy()  # Process the mask for the specific detection

                # If there are extra dimensions, squeeze the mask
                mask = np.squeeze(mask)  # This removes extra dimensions like [1, h, w] -> [h, w]

                # Check if the mask is non-empty before resizing
                if mask.size > 0:
                    # Resize the mask to match the original image size
                    mask_resized = cv2.resize(mask, (image.shape[1], image.shape[0]))

                    # Convert the mask into a binary mask (thresholding)
                    binary_mask = (mask_resized > 0.5).astype(np.uint8)  # Thresholding mask

                    # Create a colored version of the mask (e.g., white for lanes)
                    colored_mask = np.zeros_like(image, dtype=np.uint8)
                    colored_mask[binary_mask == 1] = [255, 255, 255]  # White color for lane

                    # Add the mask to the output image with some transparency
                    out_image = cv2.addWeighted(out_image, 1, colored_mask, 0.5, 0)

                    # Add this result to the filtered list
                    filtered_results.append(result)
                else:
                    print("Empty mask encountered.")

    return out_image, filtered_results


def calculate_best_intersection_and_steering(green_slope, image_center_x, green_intercept, green_midpoint):
    """
    Calculates the steering angle. First checks if the red and green lines intersect.
    If they intersect, calculate the angle between the lines. If not, fall back on
    using the midpoint of the green line and the red line for steering.
    """
    # Red line is vertical, at x = image_center_x
    red_line_x = image_center_x

    # Calculate the y-value where the green line intersects with the red line
    if green_slope is not None:
        # Intersection point is at (red_line_x, y)
        green_y_at_red_x = green_slope * red_line_x + green_intercept

        # Check if this intersection point is within the image bounds (i.e., it's a valid intersection)
        if 0 <= green_y_at_red_x <= 1:  # Assuming normalized y-values, adjust bounds as needed
            # If they intersect, calculate the angle between the red and green lines
            angle_radians = np.arctan(green_slope)  # Angle between green slope and vertical red line

            # Normalize the angle to [-1, 1] for steering
            max_angle = np.pi / 2  # Max steering angle is 90 degrees (in radians)
            steering = angle_radians / max_angle

            # Clip the steering to the range [-1, 1]
            return np.clip(steering, -1, 1)

    # If they don't intersect, fallback to using the midpoint of the green line
    # Red line origin (x = image_center_x, y = 0)
    red_origin = (image_center_x, 0)

    # Extract the midpoint coordinates from the green line
    green_midpoint_x, green_midpoint_y = green_midpoint

    # Calculate the triangle's base and height using the red origin and green midpoint
    base = green_midpoint_x - image_center_x  # Horizontal distance (x-axis)
    height = green_midpoint_y  # Vertical distance (y-axis), since red_origin.y = 0

    if height == 0:
        # If the green midpoint is exactly on the same height as red origin, return 0 steering
        return 0.0

    # Calculate the angle using arctan (inverse tangent)
    angle_radians = np.arctan2(base, height)  # Angle in radians

    # Normalize the angle to [-1, 1] for steering (left is negative, right is positive)
    max_angle = np.pi / 2  # Max steering angle is 90 degrees (in radians)
    steering = angle_radians / max_angle

    # Clip the steering to the range [-1, 1]
    return np.clip(steering, -1, 1)
def field_of_play(filtered_results, image):
    # Copy the original image to draw on it
    output_image = image.copy()
    image_height, image_width = image.shape[:2]
    image_center_x = image_width // 2  # The x-coordinate of the origin line (center)
    image_center = (image_center_x, image_height - 1)  # Bottom center point of the image

    # Draw the red origin line (vertical line at the center of the image)
    red_line_points = [(image_center_x, 0), (image_center_x, image_height)]
    cv2.line(output_image, red_line_points[0], red_line_points[1], (0, 0, 255), 2)  # Red for origin line

    # Initialize lists to store line information
    dotted_lines_left = []
    dotted_lines_right = []
    other_lines = []

    # Iterate over filtered results (segmented lines)
    for result in filtered_results:
        boxes = result.boxes.xyxy
        ids = result.boxes.id
        masks = result.masks.data
        class_ids = result.boxes.cls

        for i in range(len(boxes)):
            class_id = int(class_ids[i].item())  # Extract the class ID
            mask = masks[i].cpu().numpy()
            mask_resized = cv2.resize(mask, (image_width, image_height))
            binary_mask = (mask_resized > 0.5).astype(np.uint8)  # Convert mask to binary

            # Find the coordinates of all points in the mask (for best-fit line)
            mask_points = np.column_stack(np.where(binary_mask == 1))

            if len(mask_points) == 0:
                continue

            # Calculate min and max for x and y of the mask points
            min_x = np.min(mask_points[:, 1])
            max_x = np.max(mask_points[:, 1])
            min_y = np.min(mask_points[:, 0])
            max_y = np.max(mask_points[:, 0])

            # Calculate the mean x-coordinate
            mean_x = np.mean(mask_points[:, 1])

            # Store line info
            line_info = {
                "min_x": min_x,
                "max_x": max_x,
                "min_y": min_y,
                "max_y": max_y,
                "mean_x": mean_x,
                "mask_points": mask_points.tolist(),
                "class_id": class_id
            }

            if class_id == 1:  # Dotted line
                # Group dotted lines based on their side
                if mean_x < image_center_x:
                    dotted_lines_left.append(line_info)
                elif mean_x > image_center_x:
                    dotted_lines_right.append(line_info)
            else:
                other_lines.append(line_info)

    # Function to merge mask points of dotted lines on each side
    def merge_dotted_lines(dotted_lines):
        merged_line = {
            "mask_points": [],
            "mean_x": None
        }
        if dotted_lines:
            # Combine all mask points
            all_points = []
            for line in dotted_lines:
                all_points.extend(line['mask_points'])
            merged_line["mask_points"] = all_points
            # Calculate the mean x-coordinate
            merged_line["mean_x"] = np.mean([p[1] for p in all_points])
        return merged_line

    # Merge dotted lines on each side
    merged_dotted_left = merge_dotted_lines(dotted_lines_left)
    merged_dotted_right = merge_dotted_lines(dotted_lines_right)

    # Combine all lines for selection
    all_lines = []

    # Add merged dotted lines if they exist
    if merged_dotted_left["mask_points"]:
        all_lines.append({
            "mean_x": merged_dotted_left["mean_x"],
            "mask_points": merged_dotted_left["mask_points"],
            "class_id": 1  # Dotted line
        })
    if merged_dotted_right["mask_points"]:
        all_lines.append({
            "mean_x": merged_dotted_right["mean_x"],
            "mask_points": merged_dotted_right["mask_points"],
            "class_id": 1  # Dotted line
        })

    # Add other lines
    all_lines.extend(other_lines)

    # Initialize variables to store the selected left and right lines
    selected_left_line = None
    selected_right_line = None

    # Initialize variables to store the minimum distances
    min_left_distance = float('inf')
    min_right_distance = float('inf')

    # Iterate over all lines to select the closest ones to the center line
    for line in all_lines:
        mean_x = line['mean_x']
        distance = abs(mean_x - image_center_x)

        if mean_x < image_center_x:
            # Line is on the left side
            if distance < min_left_distance:
                min_left_distance = distance
                selected_left_line = line
        elif mean_x > image_center_x:
            # Line is on the right side
            if distance < min_right_distance:
                min_right_distance = distance
                selected_right_line = line

    # Function to calculate best-fit line and draw it
    def draw_best_fit_line(points, color):
        if len(points) > 1:
            # Sort points based on their y-values (top to bottom)
            points = sorted(points, key=lambda p: p[0])

            # Get x and y coordinates separately
            y_coords, x_coords = zip(*points)

            # Calculate the best-fit line (linear fit)
            best_fit = np.polyfit(y_coords, x_coords, 1)
            best_fit_slope = best_fit[0]
            best_fit_intercept = best_fit[1]

            # Draw the best-fit line from top to bottom
            for y in range(image_height):
                x = int(best_fit_slope * y + best_fit_intercept)
                if 0 <= x < image_width:  # Ensure the point is within image bounds
                    output_image[y, x] = color  # Draw the line in the specified color
            return best_fit_slope, best_fit_intercept
        else:
            return None, None

    # Helper function to eliminate outliers based on distance from the best-fit line
    def filter_outliers(points):
        if len(points) < 2:
            return points  # No filtering needed if fewer than 2 points

        # Convert to NumPy array for easier processing
        points = np.array(points)
        y_coords = points[:, 0]
        x_coords = points[:, 1]

        # Fit a line to the points
        best_fit = np.polyfit(y_coords, x_coords, 1)
        best_fit_line = np.poly1d(best_fit)

        # Calculate distances from the points to the best-fit line
        distances = np.abs(x_coords - best_fit_line(y_coords))

        # Calculate threshold for outliers
        threshold = np.mean(distances) + 2 * np.std(distances)

        # Filter out points that are farther than the threshold
        filtered_points = points[distances < threshold]

        return filtered_points.tolist()

    # Process the left field line
    left_slope, left_intercept = None, None
    if selected_left_line:
        # Handle the case where the left field line is selected
        filtered_left_points = filter_outliers(selected_left_line['mask_points'])
        left_slope, left_intercept = draw_best_fit_line(filtered_left_points, (57, 255, 20))  # Neon green for best-fit line

    # Process the right field line
    right_slope, right_intercept = None, None
    if selected_right_line:
        # Handle the case where the right field line is selected
        filtered_right_points = filter_outliers(selected_right_line['mask_points'])
        right_slope, right_intercept = draw_best_fit_line(filtered_right_points, (0, 150, 150))  # Neon green for best-fit line

    # Calculate and draw the follow line (midpoint between left and right field lines)
    follow_line_points = []
    if left_slope is not None and right_slope is not None:
        # Ensure both field lines exist
        for y in range(image_height):
            # Calculate the x-coordinates for left and right best-fit lines at this y
            left_x = int(left_slope * y + left_intercept)
            right_x = int(right_slope * y + right_intercept)

            # Calculate the midpoint (follow line)
            follow_x = (left_x + right_x) // 2  # Midpoint between the two field lines

            # Draw the follow line in bright blue
            if 0 <= follow_x < image_width:
                output_image[y, follow_x] = (255, 0, 0)  # Blue for the follow line
                follow_line_points.append((y, follow_x))  # Note: (y, x) format
    else:
        follow_line_points = []

    # Fit a line to the follow line points to get its slope and intercept
    if len(follow_line_points) > 1:
        # Get y and x coordinates separately
        y_coords, x_coords = zip(*follow_line_points)

        # Fit a line to the points
        follow_fit = np.polyfit(y_coords, x_coords, 1)
        follow_slope = follow_fit[0]
        follow_intercept = follow_fit[1]

        # Calculate the x-coordinate at the bottom of the image (y = image_height - 1)
        follow_x_bottom = int(follow_slope * (image_height - 1) + follow_intercept)
        follow_bottom_point = (follow_x_bottom, image_height - 1)

        # Call the steering function using the calculated follow line
        # Assume the function calculate_best_intersection_and_steering is defined
        steering_angle = calculate_best_intersection_and_steering(
            follow_slope, image_center_x, follow_intercept, follow_bottom_point
        )
        print(f"Steering angle: {steering_angle}")  # Output the steering angle
    else:
        steering_angle = None

    # Save the processed image as test.png
    cv2.imwrite('test.png', output_image)

    return output_image, red_line_points, selected_left_line, selected_right_line, steering_angle

def get_lines(filtered_results, image):
    output_image = image.copy()
    lines = []
    image_height = image.shape[0]
    image_center = (image.shape[1] // 2, image.shape[0] // 2)
    closest_solid_line = None  # Closest solid line from either left or right
    min_distance = float('inf')  # Keep track of minimum distance to the center
    dotted_points = []  # Store points of dotted lines for fitting
    fallback_lines = []  # Store points of solid or double lines as fallback

    purple_lines = []  # Store the purple lines to be plotted first
    solid_line_points = []  # Points for the orange solid line
    divisor_points = []  # Points for the divisor line (dotted or fallback)

    for result in filtered_results:
        boxes = result.boxes.xyxy
        ids = result.boxes.id
        masks = result.masks.data
        class_ids = result.boxes.cls  # Assuming this gives the class IDs

        for i in range(len(boxes)):
            object_id = int(ids[i]) if ids is not None else None
            class_id = int(class_ids[i].item())  # Extract the class ID as an integer
            mask = masks[i].cpu().numpy()
            mask_resized = cv2.resize(mask, (image.shape[1], image.shape[0]))
            binary_mask = (mask_resized > 0.5).astype(np.uint8)
            contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                if len(contour) >= 2:
                    [vx, vy, x, y] = cv2.fitLine(contour, cv2.DIST_L2, 0, 0.01, 0.01)
                    x_min, y_min, w, h = cv2.boundingRect(contour)
                    x_max = x_min + w
                    y_max = y_min + h

                    def compute_intersection(x_start, y_start, vx, vy, x_min, x_max, y_min, y_max):
                        points = []
                        if vx == 0:
                            x_bound = x_start
                            for y_bound in [y_min, y_max]:
                                if y_min <= y_bound <= y_max:
                                    points.append((int(x_bound), int(y_bound)))
                        else:
                            for x_bound in [x_min, x_max]:
                                y_bound = vy / vx * (x_bound - x_start) + y_start
                                if y_min <= y_bound <= y_max:
                                    points.append((int(x_bound), int(y_bound)))

                        if vy == 0:
                            y_bound = y_start
                            for x_bound in [x_min, x_max]:
                                if x_min <= x_bound <= x_max:
                                    points.append((int(x_bound), int(y_bound)))
                        else:
                            for y_bound in [y_min, y_max]:
                                x_bound = vx / vy * (y_bound - y_start) + x_start
                                if x_min <= x_bound <= x_max:
                                    points.append((int(x_bound), int(y_bound)))

                        return points

                    intersections = compute_intersection(x, y, vx, vy, x_min, x_max, y_min, y_max)

                    if len(intersections) >= 2:
                        intersections = sorted(intersections, key=lambda pt: (pt[0], pt[1]))
                        pt1, pt2 = intersections[0], intersections[1]

                        # Collect class ID 2 or 5 (solid or double lines) for plotting in purple
                        if class_id in [2, 5]:
                            purple_lines.append((pt1, pt2))  # Store the purple line data
                            lines.append((pt1, pt2, object_id))
                            fallback_lines.append((pt1, pt2))  # Store solid/double lines for fallback

                            # Calculate distance of the midpoint to the center of the image
                            midpoint = ((pt1[0] + pt2[0]) // 2, (pt1[1] + pt2[1]) // 2)
                            distance_to_center = abs(midpoint[0] - image_center[0])

                            # Update if this is the closest solid or double line found
                            if distance_to_center < min_distance:
                                min_distance = distance_to_center
                                solid_line_points = [pt1, pt2]  # Only store the closest line's points
                                closest_solid_line = (pt1, pt2)

                        # Collect dotted line points for best-fit line calculation (class 1)
                        if class_id == 1:
                            midpoint = ((pt1[0] + pt2[0]) // 2, (pt1[1] + pt2[1]) // 2)
                            dotted_points.append(midpoint)

    # Plot the purple lines first
    for pt1, pt2 in purple_lines:
        cv2.line(output_image, pt1, pt2, (128, 0, 128), 2)  # Purple for solid or double lines

    # Process dotted points for the divisor (preferred)
    best_fit_slope, best_fit_intercept = None, None
    if len(dotted_points) > 1:
        # Filter out outliers based on x and y values
        x_coords, y_coords = zip(*dotted_points)
        median_x = np.median(x_coords)
        median_y = np.median(y_coords)

        # Filter points that are within a threshold from the median (e.g., 20% deviation)
        threshold_x = 0.2 * median_x
        threshold_y = 0.2 * median_y

        filtered_points = [
            (x, y) for x, y in dotted_points
            if abs(x - median_x) < threshold_x and abs(y - median_y) < threshold_y
        ]

        if len(filtered_points) > 1:
            # Separate x and y coordinates after filtering
            filtered_x, filtered_y = zip(*filtered_points)

            # Fit a straight line (linear fit)
            best_fit_slope, best_fit_intercept = np.polyfit(filtered_y, filtered_x, 1)

            # Extend the line from the bottom to the top of the image
            for y in range(image_height):
                x = int(best_fit_slope * y + best_fit_intercept)
                if 0 <= x < image.shape[1]:  # Ensure the point is within image bounds
                    output_image[y, x] = (255, 105, 180)  # Pink for the best-fit line
                divisor_points.append((x, y))  # Store divisor points for midpoint calculation

    # If no dotted lines are found, use solid/double lines for the divisor
    elif len(fallback_lines) > 0:
        pt1, pt2 = fallback_lines[0]  # Take the first solid or double line
        cv2.line(output_image, pt1, pt2, (255, 105, 180), 2)  # Pink for fallback divisor line
        divisor_points.append(pt1)
        divisor_points.append(pt2)

    # If neither dotted nor solid/double lines are found, print an error
    else:
        print("Error: No valid dotted, solid, or double lines found for the divisor.")

    # Draw the red origin line in the center
    red_line_points = [(image_center[0], 0), (image_center[0], image.shape[0])]
    cv2.line(output_image, red_line_points[0], red_line_points[1], (0, 0, 255), 2)  # Red origin line

    # Plot the orange solid line using np.polyfit **LAST**
    solid_slope, solid_intercept = None, None
    if len(solid_line_points) > 1:
        solid_x, solid_y = zip(*solid_line_points)
        solid_slope, solid_intercept = np.polyfit(solid_y, solid_x, 1)

        # Extend the orange line from bottom to top
        for y in range(image_height):
            x = int(solid_slope * y + solid_intercept)
            if 0 <= x < image.shape[1]:  # Ensure the point is within image bounds
                output_image[y, x] = (0, 165, 255)  # Orange for the best-fit solid line

    # Calculate the recommended line (midpoint between orange and best-fit/divisor lines)
    green_line_points = []
    if best_fit_slope is not None and solid_slope is not None:
        # Calculate the green line (recommended) from the bottom of the image
        for y in range(image_height):
            best_fit_x = int(best_fit_slope * y + best_fit_intercept)
            solid_x = int(solid_slope * y + solid_intercept)
            midpoint_x = (best_fit_x + solid_x) // 2

            if 0 <= midpoint_x < image.shape[1]:  # Ensure the midpoint is within image bounds
                output_image[y, midpoint_x] = (0, 255, 0)  # Bright green for recommended line
                green_line_points.append((midpoint_x, y))

        # Call the steering function using the calculated green midpoint
        green_midpoint_x = (green_line_points[0][0] + green_line_points[-1][0]) // 2
        green_midpoint = (green_midpoint_x, image_height - 1)

        # Calculate steering using the midpoint and image center
        steering = calculate_best_intersection_and_steering(
            best_fit_slope, image_center[0], best_fit_intercept, green_midpoint
        )
        print(f"Steering angle: {steering}")  # Output the steering angle

    else:
        steering = None

    return output_image, lines, solid_line_points, red_line_points, green_line_points, steering






def follow_lane(out_image, filtered_results, original, previous_left_id=None, previous_right_id=None):
    bottom_length = 200
    top_length = 50
    output_image, lines, solid_line_points, red_line_points, green_line_points, steering = get_lines(filtered_results, out_image)
    cv2.imwrite('get_lines.jpg', output_image)
    field_of_play(filtered_results, out_image)
    return output_image, lines, solid_line_points, red_line_points, green_line_points, steering


# out_image, mask, steer = follow_lane(out_image, filtered_results, image)

def start_following(frame, previous_left_id=None, previous_right_id=None):
    results = model.track(source=frame, persist=True, stream=True)
    out_image, filtered_results = filter_detections(results, model, frame)
    output_image, lines, solid_line_points, red_line_points, green_line_points, steering = follow_lane(out_image, filtered_results, frame,
                                                                        previous_left_id, previous_right_id)

    return output_image, lines, solid_line_points, red_line_points, green_line_points, steering


output_image, lines, solid_line_points, red_line_points, green_line_points, steering = start_following(image)

