import threading
from units import Unit
import numpy as np
import matplotlib.pyplot as plt
from dataToken import DataToken
from ultralytics import YOLO
import cv2
import torch
import matplotlib.pyplot as plt
import numpy as np
import math
import copy
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from collections import defaultdict

class laneUnit(Unit):
    def __init__(self):
        super().__init__(id="laneUnit", input_type=DataToken, output_type=DataToken)

    def process(self, data_token):
        image = data_token.get_sensor_data('camera')
        output = data_token.get_processing_result('laneUnit')

        image = data_token.get_sensor_data('camera')

            # Apply blue tint to the image before any further processing
        image = image.astype(np.float32)

            # Adjust color channels
        blue_channel_multiplier = 1.3
        red_channel_multiplier = 0.95
        green_channel_multiplier = 0.95

        image[:, :, 0] *= blue_channel_multiplier  # Increase blue channel
        image[:, :, 1] *= green_channel_multiplier  # Slightly decrease green channel
        image[:, :, 2] *= red_channel_multiplier   # Slightly decrease red channel

            # Clip the values to the valid range [0, 255]
        image = np.clip(image, 0, 255)

            # Convert back to uint8
        image = image.astype(np.uint8)


        if (output):
            previous_left_id = output.get('previous_left_id', None)
            previous_right_id = output.get('previous_right_id', None)
        else:
            previous_left_id = None
            previous_right_id = None

        output_image, red_line_points, selected_left_line, selected_right_line, follow_line_points, steering_angle = self.start_following(image, previous_left_id, previous_right_id)
        lane_processing_result = {
            'output_image': output_image,  # Optional: Save the image path or a smaller representation
            'left_line': selected_left_line,  # List of left line points
            'red_line_points': red_line_points,  # List of red line points (origin line)
            'right_line': selected_right_line,  # List of right line points
            'follow_line': follow_line_points,  # List of follow line points
            'steering': steering_angle,  # The calculated steering value
        }
        data_token.add_processing_result(self.id, lane_processing_result)

        data_token.set_flag('has_lane_data', True)

        if self.next_unit:
            return self.next_unit.process(data_token)
        return data_token

    def filter_detections(self, results, model, image, crop_height=None):
        height, width, channels = image.shape
        out_image = np.zeros((height, width, channels), dtype=np.uint8)
        filtered_results = []

        for result in results:
            # Create a copy of the result to ensure the original is not modified
            result_copy = copy.deepcopy(result)

            for i in range(len(result.boxes.cls)):
                class_id = int(result.boxes.cls[i].item())
                confidence = result.boxes.conf[i].item()

                # Check if the detected class is not 0, 3, or 4 and confidence is greater than 0.5
                if class_id not in [0, 3, 4] and confidence > 0.5:
                    mask = result.masks.data[i].cpu().numpy()
                    mask = np.squeeze(mask)

                    if mask.size > 0:
                        original_mask_shape = mask.shape  # Get the original mask shape
                        # Resize the mask to fit the cropped region width, but only apply to the cropped area height
                        mask_resized = cv2.resize(mask, (image.shape[1], crop_height), interpolation=cv2.INTER_NEAREST)

                        # Convert the resized mask to binary
                        binary_mask = (mask_resized > 0.5).astype(np.uint8)

                        # Create a colored mask for overlay
                        colored_mask = np.zeros_like(image, dtype=np.uint8)

                        # Only apply the mask to the top cropped region
                        colored_mask[:crop_height, :] = np.stack([binary_mask] * 3, axis=-1) * 255

                        # Overlay the mask onto the output image
                        out_image = cv2.addWeighted(out_image, 1, colored_mask, 0.5, 0)

                        # Shift the mask back to its correct position in the full image
                        full_mask = np.zeros((height, width), dtype=np.uint8)
                        full_mask[:crop_height, :] = binary_mask

                        # Resize the full mask back to the original mask size before assigning it to the result copy
                        full_mask_resized = cv2.resize(full_mask, (original_mask_shape[1], original_mask_shape[0]), interpolation=cv2.INTER_NEAREST)

                        # Modify the result's mask copy to represent its new full-image position
                        result_copy.masks.data[i] = torch.tensor(full_mask_resized).cpu()

                        # Adjust the bounding box to fit the full image's coordinate system
                        x_min, y_min, x_max, y_max = result.boxes.xyxy[i].cpu().numpy()
                        result_copy.boxes.xyxy[i] = torch.tensor([x_min, y_min, x_max, y_max])

                        # Append the modified copy to the filtered results
                        filtered_results.append(result_copy)
                    else:
                        print("Empty mask encountered.")

        return out_image, filtered_results

    def calculate_best_intersection_and_steering(self, green_slope, image_center_x, green_intercept, green_midpoint):
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

            # Check if this intersection point is within the image bounds
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

    def get_lines(self, filtered_results, image):
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
            # Return only the list of points
            selected_left_line = filtered_left_points
        else:
            selected_left_line = []

        # Process the right field line
        right_slope, right_intercept = None, None
        if selected_right_line:
            # Handle the case where the right field line is selected
            filtered_right_points = filter_outliers(selected_right_line['mask_points'])
            right_slope, right_intercept = draw_best_fit_line(filtered_right_points, (0, 150, 150))  # Neon green for best-fit line
            # Return only the list of points
            selected_right_line = filtered_right_points
        else:
            selected_right_line = []

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
                    follow_line_points.append((follow_x, y))  # Note: (x, y) format
        else:
            follow_line_points = []

        # Fit a line to the follow line points to get its slope and intercept
        if len(follow_line_points) > 1:
            # Get x and y coordinates separately
            x_coords, y_coords = zip(*follow_line_points)

            # Fit a line to the points
            follow_fit = np.polyfit(y_coords, x_coords, 1)
            follow_slope = follow_fit[0]
            follow_intercept = follow_fit[1]

            # Calculate the x-coordinate at the bottom of the image (y = image_height - 1)
            follow_x_bottom = int(follow_slope * (image_height - 1) + follow_intercept)
            follow_bottom_point = (follow_x_bottom, image_height - 1)

            # Call the steering function using the calculated follow line
            steering_angle = self.calculate_best_intersection_and_steering(
                follow_slope, image_center_x, follow_intercept, follow_bottom_point
            )
            print(f"Steering angle: {steering_angle}")  # Output the steering angle
        else:
            steering_angle = None

        # Save the processed image as test.png
        cv2.imwrite('test.png', output_image)

        return output_image, red_line_points, selected_left_line, selected_right_line, follow_line_points, steering_angle

    def follow_lane(self, out_image, filtered_results, original, previous_left_id=None, previous_right_id=None):
        bottom_length = 200
        top_length = 50
        output_image, red_line_points, selected_left_line, selected_right_line, follow_line_points, steering_angle = self.get_lines(filtered_results, out_image)

        return output_image, red_line_points, selected_left_line, selected_right_line, follow_line_points, steering_angle

    def start_following(self, frame, previous_left_id=None, previous_right_id=None):
        # Convert RGBA to RGB if needed
        if frame.shape[2] == 4:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)

        # Get original frame dimensions
        original_height, original_width = frame.shape[:2]

        cutoff_percent = 37

        # Calculate the height of the cropped frame
        crop_height = int(original_height * (1 - cutoff_percent / 100.0))

        # Crop the frame (keep only the top part)
        cropped_frame = frame[:crop_height, :]

        # Load the YOLO model
        model = YOLO('laneTest.pt')

        # Run detection on the cropped frame
        results = model.track(source=cropped_frame, persist=True, stream=True)

        # Filter the detections and prepare for further steps
        out_image, filtered_results = self.filter_detections(results, model, frame, crop_height)

        # Pass the original frame, not the cropped one, to the follow_lane function
        output_image, red_line_points, selected_left_line, selected_right_line, follow_line_points, steering_angle = self.follow_lane(out_image, filtered_results, frame, previous_left_id, previous_right_id)

        # Return results
        return output_image, red_line_points, selected_left_line, selected_right_line, follow_line_points, steering_angle
