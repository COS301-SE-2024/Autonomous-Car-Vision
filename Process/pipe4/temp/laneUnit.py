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
import random
import itertools

class laneUnit(Unit):
    def __init__(self):
        super().__init__(id="laneUnit", input_type=DataToken, output_type=DataToken)

    def process(self, data_token):
        image = data_token.get_sensor_data('camera')
        output = data_token.get_processing_result('laneUnit')
        
        res, output = self.start_following(image)

        data_token.add_processing_result(self.id, output)

        data_token.set_flag('has_lane_data', True)

        if self.next_unit:
            return self.next_unit.process(data_token)
        return data_token

    def filter_detections(self, results, model, image):
        height, width, channels = image.shape
        out_image = np.zeros((height, width, channels), dtype=np.uint8)
        filtered_results = []  # Store filtered results

        # Iterate over the results generator
        for result in results:
            # Assuming result.boxes.cls and result.boxes.conf could be tensors with multiple values
            for i in range(len(result.boxes.cls)):
                class_id = int(result.boxes.cls[i].item())  # Extract the scalar value for class ID
                confidence = result.boxes.conf[i].item()    # Extract the scalar value for confidence

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

                        # Create a colored version of the mask with a random color
                        colored_mask = np.zeros_like(image, dtype=np.uint8)
                        random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                        colored_mask[binary_mask == 1] = random_color  # Assign a random color to the mask

                        # Add the mask to the output image with some transparency
                        out_image = cv2.addWeighted(out_image, 1, colored_mask, 0.5, 0)

                        # Add this result to the filtered list
                        filtered_results.append(result)
                    else:
                        print("Empty mask encountered.")
        
        return out_image, filtered_results

    def get_lines(self, filtered_results, image):
        output_image = image.copy()  # Create a copy of the original image to draw on
        lines = []  # Array to store the lines as objects (start_point, end_point, tracking_id)

        for result in filtered_results:
            # Get the boxes, ids, and masks for each object
            boxes = result.boxes.xyxy  # Bounding boxes in xyxy format
            ids = result.boxes.id  # Object tracking IDs
            masks = result.masks.data  # Segmentation masks

            # Iterate over the objects detected in the current frame
            for i in range(len(boxes)):
                # Get object tracking ID if available, otherwise use None
                object_id = int(ids[i]) if ids is not None else None
                class_id = int(result.boxes.cls[i].item())

                # Extract the binary mask for the detected object
                mask = masks[i].cpu().numpy()  # Convert mask to numpy array
                mask_resized = cv2.resize(mask, (image.shape[1], image.shape[0]))  # Resize mask to match the image size
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
                                        points.append((int(x_bound.item() if isinstance(x_bound, np.ndarray) else x_bound), int(y_bound.item() if isinstance(y_bound, np.ndarray) else y_bound)))
                            else:
                                # Intersection with vertical boundaries (x_min and x_max)
                                for x_bound in [x_min, x_max]:
                                    y_bound = vy / vx * (x_bound - x_start) + y_start
                                    if y_min <= y_bound <= y_max:
                                        points.append((int(x_bound.item() if isinstance(x_bound, np.ndarray) else x_bound), int(y_bound.item() if isinstance(y_bound, np.ndarray) else y_bound)))

                            # Handle horizontal lines (vy == 0)
                            if vy == 0:
                                y_bound = y_start
                                # Intersection with vertical boundaries
                                for x_bound in [x_min, x_max]:
                                    if x_min <= x_bound <= x_max:
                                        points.append((int(x_bound.item() if isinstance(x_bound, np.ndarray) else x_bound), int(y_bound.item() if isinstance(y_bound, np.ndarray) else y_bound)))
                            else:
                                # Intersection with horizontal boundaries (y_min and y_max)
                                for y_bound in [y_min, y_max]:
                                    x_bound = vx / vy * (y_bound - y_start) + x_start
                                    if x_min <= x_bound <= x_max:
                                        points.append((int(x_bound.item() if isinstance(x_bound, np.ndarray) else x_bound), int(y_bound.item() if isinstance(y_bound, np.ndarray) else y_bound)))

                            return points

                        # Calculate the intersection points of the fitted line with the bounding box
                        intersections = compute_intersection(x, y, vx, vy, x_min, x_max, y_min, y_max)

                        if len(intersections) >= 2:
                            # Sort intersections to get consistent line endpoints
                            intersections = sorted(intersections, key=lambda pt: (pt[0], pt[1]))
                            pt1, pt2 = intersections[0], intersections[1]

                            # Draw the line within the contour bounding box
                            cv2.line(output_image, pt1, pt2, (0, 255, 0), 2)

                            # Append the line as a tuple (start, end, tracking_id, class_id) to the lines array
                            lines.append((pt1, pt2, object_id, class_id))

        return output_image, lines

    def identify_dotted(self, lines, image):
        output_image = image.copy()
        dotted_lines = [line for line in lines if line[3] == 1]  # Class ID 1 represents dotted lines
        other_lines = [line for line in lines if line[3] != 1]  # Lines that are not dotted lines

        # Initialize groups as a list of lists
        groups = []

        # Function to calculate the slope of a line
        def calculate_slope(pt1, pt2):
            if (pt2[0] - pt1[0]) == 0:  # Avoid division by zero
                return float('inf')
            return (pt2[1] - pt1[1]) / (pt2[0] - pt1[0])

        # Function to check if three points form a smooth line
        def is_smooth_line(pt1, pt2, pt3):
            slope1 = calculate_slope(pt1, pt2)
            slope2 = calculate_slope(pt2, pt3)
            return abs(slope1 - slope2) < 0.2  # Threshold for smoothness

        # Grouping dotted lines based on smooth alignment
        for line in dotted_lines:
            pt1, pt2, _, _ = line
            added_to_group = False

            # Try to add the line to an existing group
            for group in groups:
                for grouped_line in group:
                    grouped_pt1, grouped_pt2, _, _ = grouped_line

                    # Check if the current line forms a smooth continuation with any line in the group
                    if is_smooth_line(grouped_pt1, grouped_pt2, pt1) or is_smooth_line(grouped_pt1, grouped_pt2, pt2):
                        group.append(line)
                        added_to_group = True
                        break
                if added_to_group:
                    break

            # If the line was not added to any group, create a new group
            if not added_to_group:
                groups.append([line])

        # Add each of the other lines as their own group
        for line in other_lines:
            groups.append([line])

        # Connect lines in the same group and add them as new lines
        for group in groups:
            if len(group) > 1:
                group_points = []
                for line in group:
                    group_points.append(line[0])  # Start point
                    group_points.append(line[1])  # End point

                # Sort points by x-coordinate to connect them sequentially
                group_points = sorted(group_points, key=lambda pt: pt[0])

                for i in range(len(group_points) - 1):
                    pt1 = group_points[i]
                    pt2 = group_points[i + 1]
                    new_line = (pt1, pt2, None, 1)  # Create a new line tuple
                    group.append(new_line)  # Add the new line to the group
                    cv2.line(output_image, pt1, pt2, (0, 255, 0), 2)  # Draw the connecting line

        # Draw each group with a random color
        for group in groups:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Generate random RGB color
            for line in group:
                pt1, pt2, _, _ = line
                cv2.line(output_image, pt1, pt2, color, 2)

        return output_image, groups

    def extend_lines(self, groups, image):
        output_image = image.copy()
        height, width, _ = image.shape

        for group in groups:
            # Find the line with the highest y-coordinate in the group (i.e., the lowest line)
            lowest_line = max(group, key=lambda line: max(line[0][1], line[1][1]))
            pt1, pt2, _, _ = lowest_line

            # Calculate the slope of the line
            if (pt2[0] - pt1[0]) != 0:
                slope = (pt2[1] - pt1[1]) / (pt2[0] - pt1[0])
            else:
                slope = float('inf')

            # Extend the line downward by its own slope until it reaches the bottom of the screen
            if slope != float('inf'):
                if pt1[1] > pt2[1]:
                    lower_point = pt1
                else:
                    lower_point = pt2

                # Calculate the new point that extends to the bottom of the image
                extension_length = height - lower_point[1]
                new_x = int(lower_point[0] + extension_length / slope) if slope != 0 else lower_point[0]
                new_y = height
            else:
                # Vertical line case
                new_x = pt1[0]
                new_y = height

            # Draw the extended line
            cv2.line(output_image, (lower_point[0], lower_point[1]), (new_x, new_y), (255, 0, 0), 2)
            group.append(((lower_point[0], lower_point[1]), (new_x, new_y), None, 1))

        return output_image, groups

    def get_current_lane(self, groups, image):
        output_image = image.copy()
        height, width, _ = image.shape
        center_x = width // 2

        # Define initial reference lines (slightly tilted inward)
        left_ref_line_start = (int(width * 0.3), height)  # Bottom of the image, 30% from the left
        left_ref_line_end = (int(width * 0.45), int(height * 0.6))  # 60% down the height, tilted inwards

        right_ref_line_start = (int(width * 0.7), height)  # Bottom of the image, 70% from the left
        right_ref_line_end = (int(width * 0.55), int(height * 0.6))  # 60% down the height, tilted inwards

        # Define wider reference lines (in purple, just a bit wider than the current reference lines)
        left_wide_ref_line_start = (int(width * 0.15), height)  # Slightly more to the left
        left_wide_ref_line_end = (int(width * 0.35), int(height * 0.6))  # 60% down the height, tilted inwards

        right_wide_ref_line_start = (int(width * 0.85), height)  # Slightly more to the right
        right_wide_ref_line_end = (int(width * 0.65), int(height * 0.6))  # 60% down the height, tilted inwards

        # Draw the initial reference lines
        cv2.line(output_image, left_ref_line_start, left_ref_line_end, (255, 0, 0), 2)  # Blue for left reference
        cv2.line(output_image, right_ref_line_start, right_ref_line_end, (0, 0, 255), 2)  # Red for right reference

        # Draw the wider reference lines
        cv2.line(output_image, left_wide_ref_line_start, left_wide_ref_line_end, (255, 0, 255), 2)  # Purple for wider left
        cv2.line(output_image, right_wide_ref_line_start, right_wide_ref_line_end, (255, 0, 255), 2)  # Purple for wider right

        # Initialize variables for the best matching lines
        best_left_line = None
        best_right_line = None
        min_left_weighted_dist = float('inf')
        min_right_weighted_dist = float('inf')

        # Function to calculate the Euclidean distance between two points
        def distance(pt1, pt2):
            return math.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)

        # Function to calculate the slope of a line
        def calculate_slope(pt1, pt2):
            if pt2[0] - pt1[0] == 0:
                return float('inf')  # Vertical line
            return (pt2[1] - pt1[1]) / (pt2[0] - pt1[0])

        # Function to calculate a weighted distance that gives preference to lines lower on the screen and with reasonable angles
        def weighted_distance(pt1, pt2, ref_pt1, ref_pt2, expected_slope):
            dist = (distance(pt1, ref_pt1) + distance(pt2, ref_pt2)) / 2
            # Add a preference for lines closer to the bottom of the image (larger y-values)
            avg_y = (pt1[1] + pt2[1]) / 2
            proximity_weight = (height - avg_y) / height  # Preference for lower lines (closer to bottom)

            # Calculate the slope of the detected line
            slope = calculate_slope(pt1, pt2)
            # Penalize the line if its slope deviates too much from the expected slope
            angle_penalty = abs(slope - expected_slope) / abs(expected_slope + 1e-5)  # Small value added to avoid division by zero

            # Adjust the distance with a weight based on proximity and slope (angle)
            return dist * (1 - 0.5 * proximity_weight) * (1 + 0.6 * angle_penalty)  # 0.3 factor for angle penalty

        # Expected slopes for left and right lanes (based on typical road angles)
        expected_left_slope = (left_ref_line_end[1] - left_ref_line_start[1]) / (left_ref_line_end[0] - left_ref_line_start[0])
        expected_right_slope = (right_ref_line_end[1] - right_ref_line_start[1]) / (right_ref_line_end[0] - right_ref_line_start[0])

        # Compare each group of detected lines with the reference lines
        for group in groups:
            for line in group:
                pt1, pt2, _, _ = line
                line_mid_x = (pt1[0] + pt2[0]) / 2

                # Calculate the weighted distance of the current line to the reference lines, including slope check
                left_weighted_dist = weighted_distance(pt1, pt2, left_ref_line_start, left_ref_line_end, expected_left_slope)
                right_weighted_dist = weighted_distance(pt1, pt2, right_ref_line_start, right_ref_line_end, expected_right_slope)

                # Ensure the left line is to the left of the center and the right line to the right
                if left_weighted_dist < min_left_weighted_dist and line_mid_x < center_x:
                    min_left_weighted_dist = left_weighted_dist
                    best_left_line = line

                if right_weighted_dist < min_right_weighted_dist and line_mid_x > center_x:
                    min_right_weighted_dist = right_weighted_dist
                    best_right_line = line

        # If we found a best left line, draw it
        if best_left_line:
            cv2.line(output_image, best_left_line[0], best_left_line[1], (0, 255, 0), 3)  # Green for detected left lane

        # If we found a best right line, draw it
        if best_right_line:
            cv2.line(output_image, best_right_line[0], best_right_line[1], (0, 255, 0), 3)  # Green for detected right lane

        # If only one line was found, extend it to fit the road
        if best_left_line and not best_right_line:
            best_right_line = ((best_left_line[1][0] + 100, best_left_line[1][1]), (best_left_line[0][0] + 100, best_left_line[0][1]), None, 1)
            cv2.line(output_image, best_right_line[0], best_right_line[1], (0, 255, 0), 3)  # Green for detected right lane

        if best_right_line and not best_left_line:
            best_left_line = ((best_right_line[1][0] - 100, best_right_line[1][1]), (best_right_line[0][0] - 100, best_right_line[0][1]), None, 1)
            cv2.line(output_image, best_left_line[0], best_left_line[1], (0, 255, 0), 3)  # Green for detected left lane

        # Return the output image, best left and right lines, and the outer reference lines
        return output_image, best_left_line, best_right_line, (left_wide_ref_line_start, left_wide_ref_line_end), (right_wide_ref_line_start, right_wide_ref_line_end)

    def analyse_steering(self, best_left_line, best_right_line, left_ref_line, right_ref_line, image_width):
        left_ref_start, left_ref_end = left_ref_line
        right_ref_start, right_ref_end = right_ref_line

        # Calculate the x-position of the middle of the image
        center_x = image_width // 2

        steering_value = 0
        steering_multiplier = 1.3  # Scaling factor to increase steering sensitivity

        if best_left_line and best_right_line:
            # Get the midpoint of the identified left and right lines
            left_line_mid_x = (best_left_line[0][0] + best_left_line[1][0]) / 2
            right_line_mid_x = (best_right_line[0][0] + best_right_line[1][0]) / 2

            # Average the left and right midpoints to get the center of the lane
            lane_center_x = (left_line_mid_x + right_line_mid_x) / 2

            # Calculate the deviation from the image center
            deviation = lane_center_x - center_x

            # Normalize the deviation into the range [-1, 1] (steering range)
            steering_value = deviation / (image_width / 2)

        elif best_left_line:
            # Use only the left lane line
            left_line_mid_x = (best_left_line[0][0] + best_left_line[1][0]) / 2
            deviation = left_line_mid_x - left_ref_start[0]

            # Normalize deviation to [-1, 1]
            steering_value = deviation / (image_width / 2)

        elif best_right_line:
            # Use only the right lane line
            right_line_mid_x = (best_right_line[0][0] + best_right_line[1][0]) / 2
            deviation = right_line_mid_x - right_ref_start[0]

            # Normalize deviation to [-1, 1]
            steering_value = deviation / (image_width / 2)

        # Amplify the steering value to make steering more sensitive, especially in corners
        steering_value = steering_value * steering_multiplier

        # Clip the steering value to stay within the range [-1, 1]
        steering_value = max(min(steering_value, 1), -1)

        return steering_value
    
    def follow_lane(self, out_image, filtered_results, original):
        bottom_length = 200
        top_length = 50
        
        # Process the filtered results to get lines and groups
        out_image, lines = self.get_lines(filtered_results, out_image)
        out_image, groups = self.identify_dotted(lines, out_image)
        # out_image, groups = self.extend_lines(groups, out_image)
        
        # Get the current lane information, including the best left and right lines and the reference lines
        out_image, left_line, right_line, left_ref_line, right_ref_line = self.get_current_lane(groups, out_image)
        
        # Calculate steering based on the detected lanes and reference lines
        image_width = out_image.shape[1]  # Get the width of the image
        steering_value = self.analyse_steering(left_line, right_line, left_ref_line, right_ref_line, image_width)
        
        # Return the output image, the detected lanes, and the steering value
        return out_image, None, steering_value


    def apply_blue_filter(self, frame):
        # Convert the frame to float32 to avoid clipping issues during manipulation
        frame = frame.astype(np.float32)

        # Increase the blue channel by multiplying the blue channel by a factor
        # This will give the image a blue tint
        blue_channel = 2  # Adjust this value to get the desired intensity
        frame[:, :, 0] = frame[:, :, 0] * blue_channel  # Blue channel (index 0)

        # Clip the values to be in the valid range [0, 255] and convert back to uint8
        frame = np.clip(frame, 0, 255).astype(np.uint8)

        return frame

    def start_following(self, frame):
        filtered_frame = self.apply_blue_filter(frame)

        # Load the YOLO model
        model = YOLO('laneTest.pt')

        # Run detection on the cropped frame
        results = model(frame)

        # Filter the detections and prepare for further steps
        out_image, filtered_results = self.filter_detections(results, model, frame)

        # Pass the original frame, not the cropped one, to the follow_lane function
        res, mask, steer = self.follow_lane(out_image, filtered_results, frame)

        # Return results
        output = {'image': res,'steering': steer, 'results': results, 'mask': mask}
        return res, output
