import threading
from units import Unit
import numpy as np
import matplotlib.pyplot as plt
from dataToken import DataToken
from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import numpy as np
import math
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from collections import defaultdict

class laneUnit(Unit):
    def __init__(self):
        super().__init__(id="laneUnit", input_type=DataToken, output_type=DataToken)

    def process(self, data_token):
        image = data_token.get_sensor_data('camera')
        output = data_token.get_processing_result('laneUnit')
        
        previous_left_id = output.get('previous_left_id', None)
        previous_right_id = output.get('previous_right_id', None)
        
        res, output = self.start_following(image, previous_left_id, previous_right_id)

        data_token.add_processing_result(self.id, output)

        data_token.set_flag('has_lane_data', True)


        # Pass the data_token to the next unit in the pipeline if it exists
        if self.next_unit:
            return self.next_unit.process(data_token)
        return data_token

    def filter_detections(results, model, image):
        height, width, channels = image.shape
        out_image = np.zeros((height, width, channels), dtype=np.uint8)
        filtered_results = []  

        for result in results:
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

    def get_lines(filtered_results, image):
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

                            # Append the line as a tuple (start, end, tracking_id) to the lines array
                            lines.append((pt1, pt2, object_id))

        return output_image, lines

    def group_lines(self, image, lines):
        output_image = image.copy()  # Create a copy of the original image to draw on

        # Initialize a dictionary to store groups of lines by object_id
        grouped_lines = defaultdict(list)

        # Group lines based on the object_id
        for (start, end, object_id) in lines:
            grouped_lines[object_id].append((start, end))

        # Optionally, you can draw the lines on the output image
        for object_id, group in grouped_lines.items():
            color = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))  # Random color for each group
            for (start, end) in group:
                cv2.line(output_image, start, end, color, 2)
                # Optionally, label the group by object ID
                cv2.putText(output_image, f"ID: {object_id}", start, cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Convert defaultdict to a regular dict for returning
        grouped_lines = dict(grouped_lines)

        return output_image, grouped_lines

    def get_side_lines(self, image, grouped_lines, previous_left_id, previous_right_id):
        # Create a copy of the image to draw the lines on
        output_image = image.copy()
        height, width, _ = image.shape
        center_x = width // 2
        bottom_y = height - 1
        bottom_center = np.array([center_x, bottom_y])

        left_line, right_line = [], []
        left_id, right_id = None, None

        # Function to find the closest point in a line group to a reference point
        def closest_point_in_group(group, reference_point):
            min_dist = np.inf
            best_line = None
            for (start, end) in group:
                start, end = np.array(start), np.array(end)
                for point in [start, end]:
                    dist = np.linalg.norm(point - reference_point)
                    if dist < min_dist:
                        min_dist = dist
                        best_line = (start, end)
            return best_line, min_dist

        def calculate_slope(line):
            (x1, y1), (x2, y2) = line
            if x1 == x2:  # Avoid division by zero
                return np.inf
            return (y2 - y1) / (x2 - x1)

        left_group_distances = []
        right_group_distances = []

        # Case when both previous IDs are not None
        if previous_left_id is not None and previous_right_id is not None:
            # Select the one with the smallest ID and process normally for the other side
            if previous_left_id < previous_right_id:
                # Use the left ID and select the right side normally
                if previous_left_id in grouped_lines:
                    left_line = grouped_lines[previous_left_id]  # Use the previous left line group
                    left_id = previous_left_id
                    for (start, end) in left_line:
                        cv2.line(output_image, tuple(start), tuple(end), (0, 255, 0), 2)  # Draw in green

                # Select the right line using the normal method
                for object_id, group in grouped_lines.items():
                    best_line, min_dist = closest_point_in_group(group, bottom_center)
                    if best_line is not None:
                        slope = calculate_slope(best_line)
                        midpoint_x = (best_line[0][0] + best_line[1][0]) / 2  # Average x position of the line

                        # Only consider right lines with a positive slope and on the right of center
                        if slope > 0 and midpoint_x > center_x:
                            right_group_distances.append((min_dist, object_id, group))

                if right_group_distances:
                    right_group_distances.sort(key=lambda x: x[0])  # Sort by distance
                    _, right_id, right_line = right_group_distances[0]  # Get the closest right group
                    for (start, end) in right_line:
                        cv2.line(output_image, tuple(start), tuple(end), (255, 0, 0), 2)  # Draw in blue

            else:
                # Use the right ID and select the left side normally
                if previous_right_id in grouped_lines:
                    right_line = grouped_lines[previous_right_id]  # Use the previous right line group
                    right_id = previous_right_id
                    for (start, end) in right_line:
                        cv2.line(output_image, tuple(start), tuple(end), (255, 0, 0), 2)  # Draw in blue

                # Select the left line using the normal method
                for object_id, group in grouped_lines.items():
                    best_line, min_dist = closest_point_in_group(group, bottom_center)
                    if best_line is not None:
                        slope = calculate_slope(best_line)
                        midpoint_x = (best_line[0][0] + best_line[1][0]) / 2  # Average x position of the line

                        # Only consider left lines with a negative slope and on the left of center
                        if slope < 0 and midpoint_x < center_x:
                            left_group_distances.append((min_dist, object_id, group))

                if left_group_distances:
                    left_group_distances.sort(key=lambda x: x[0])  # Sort by distance
                    _, left_id, left_line = left_group_distances[0]  # Get the closest left group
                    for (start, end) in left_line:
                        cv2.line(output_image, tuple(start), tuple(end), (0, 255, 0), 2)  # Draw in green

        # Case when one or both previous IDs are None (fallback to the previous logic)
        else:
            # If previous left ID exists, use it
            if previous_left_id is not None and previous_left_id in grouped_lines:
                left_line = grouped_lines[previous_left_id]  # Use the previous left line group
                left_id = previous_left_id
                for (start, end) in left_line:
                    cv2.line(output_image, tuple(start), tuple(end), (0, 255, 0), 2)  # Draw in green

            # If previous right ID exists, use it
            if previous_right_id is not None and previous_right_id in grouped_lines:
                right_line = grouped_lines[previous_right_id]  # Use the previous right line group
                right_id = previous_right_id
                for (start, end) in right_line:
                    cv2.line(output_image, tuple(start), tuple(end), (255, 0, 0), 2)  # Draw in blue

            # Select closest left line if left ID is still None
            if left_id is None:
                for object_id, group in grouped_lines.items():
                    best_line, min_dist = closest_point_in_group(group, bottom_center)
                    if best_line is not None:
                        slope = calculate_slope(best_line)
                        midpoint_x = (best_line[0][0] + best_line[1][0]) / 2  # Average x position of the line

                        # Only consider left lines with a negative slope and on the left of center
                        if slope < 0 and midpoint_x < center_x:
                            left_group_distances.append((min_dist, object_id, group))

                if left_group_distances:
                    left_group_distances.sort(key=lambda x: x[0])  # Sort by distance
                    _, left_id, left_line = left_group_distances[0]  # Get the closest left group
                    for (start, end) in left_line:
                        cv2.line(output_image, tuple(start), tuple(end), (0, 255, 0), 2)  # Draw in green

            # Select closest right line if right ID is still None
            if right_id is None:
                for object_id, group in grouped_lines.items():
                    best_line, min_dist = closest_point_in_group(group, bottom_center)
                    if best_line is not None:
                        slope = calculate_slope(best_line)
                        midpoint_x = (best_line[0][0] + best_line[1][0]) / 2  # Average x position of the line

                        # Only consider right lines with a positive slope and on the right of center
                        if slope > 0 and midpoint_x > center_x:
                            right_group_distances.append((min_dist, object_id, group))

                if right_group_distances:
                    right_group_distances.sort(key=lambda x: x[0])  # Sort by distance
                    _, right_id, right_line = right_group_distances[0]  # Get the closest right group
                    for (start, end) in right_line:
                        cv2.line(output_image, tuple(start), tuple(end), (255, 0, 0), 2)  # Draw in blue

        # Return the output image, left and right lines, and their respective IDs
        return output_image, left_line, right_line, left_id, right_id

    def extend_lines(self, image, left_line, right_line):
        output_image = image.copy()
        height, width, _ = image.shape

        # Helper function to find the lowest line based on the highest y-value
        def find_lowest_line(line_group):
            lowest_y = -np.inf
            lowest_line = None
            for (start, end) in line_group:
                if max(start[1], end[1]) > lowest_y:  # Find the line with the highest y-coordinate (closest to the bottom)
                    lowest_y = max(start[1], end[1])
                    lowest_line = (start, end)
            return lowest_line

        # Helper function to extend a line downward in the same direction
        def extend_to_bottom_preserving_slope(start, end):
            # Calculate the slope (dy/dx) of the line
            dx = end[0] - start[0]
            dy = end[1] - start[1]

            # If the line is vertical, extend straight down
            if dx == 0:
                # Decide which point to use as new_start based on which is lower
                if start[1] > end[1]:  # If start is lower (closer to the bottom)
                    new_start = start
                else:
                    new_start = end
                new_end = (start[0], height)  # Keep x constant, set y to image height
            else:
                # Calculate the slope of the line
                slope = dy / dx  # Slope of the line
                if slope == 0:
                    # The line is horizontal; can't extend to the bottom
                    new_start = start if start[1] > end[1] else end
                    new_end = (new_start[0], height)  # Keep x constant
                else:
                    # Calculate how far we need to extend the line to reach the bottom of the image
                    y_extension = height - max(start[1], end[1])  # How much more to extend in the y-direction
                    x_extension = y_extension / slope  # Corresponding change in the x-direction

                    # Determine the new end point based on which point is lower (start or end)
                    if start[1] > end[1]:  # If start is lower (closer to the bottom)
                        new_end = (int(start[0] + x_extension), height)  # Extend from start
                        new_start = start
                    else:  # If end is lower
                        new_end = (int(end[0] + x_extension), height)  # Extend from end
                        new_start = end

            return new_start, new_end

        # Extend the leftmost line
        if len(left_line) > 0:
            lowest_left_line = find_lowest_line(left_line)
            if lowest_left_line:
                left_start, left_end = lowest_left_line
                new_left_start, new_left_end = extend_to_bottom_preserving_slope(left_start, left_end)
                cv2.line(output_image, new_left_start, new_left_end, (0, 255, 0), 2)  # Draw the extended left line (Green)
                left_line.append((new_left_start, new_left_end))  # Add the new extended line to the left group

        # Extend the rightmost line
        if len(right_line) > 0:
            lowest_right_line = find_lowest_line(right_line)
            if lowest_right_line:
                right_start, right_end = lowest_right_line
                new_right_start, new_right_end = extend_to_bottom_preserving_slope(right_start, right_end)
                cv2.line(output_image, new_right_start, new_right_end, (255, 0, 0), 2)  # Draw the extended right line (Blue)
                right_line.append((new_right_start, new_right_end))  # Add the new extended line to the right group

        return output_image, left_line, right_line

    def get_inners(self, image, left_line, right_line):
        output_image = image.copy()
        height, width, _ = image.shape

        # Initialize dictionaries to store the innermost line at each y level
        left_lines_at_height = {}
        right_lines_at_height = {}

        # Helper function to track the rightmost line for each height in the left group
        def track_rightmost_line_for_height(start, end, lines_at_height):
            for y in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                if y not in lines_at_height or max(start[0], end[0]) > lines_at_height[y][0]:
                    # Track the line with the highest x-value for this y-level
                    lines_at_height[y] = (max(start[0], end[0]), (start, end))

        # Helper function to track the leftmost line for each height in the right group
        def track_leftmost_line_for_height(start, end, lines_at_height):
            for y in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                if y not in lines_at_height or min(start[0], end[0]) < lines_at_height[y][0]:
                    # Track the line with the lowest x-value for this y-level
                    lines_at_height[y] = (min(start[0], end[0]), (start, end))

        # Track rightmost lines for the left line group
        for (start, end) in left_line:
            track_rightmost_line_for_height(start, end, left_lines_at_height)

        # Track leftmost lines for the right line group
        for (start, end) in right_line:
            track_leftmost_line_for_height(start, end, right_lines_at_height)

        # Collect innermost left and right lines (one per y-level)
        inner_left_lines = set()
        inner_right_lines = set()

        for y, (x, line) in left_lines_at_height.items():
            inner_left_lines.add(line)  # Add the rightmost line for this y-level

        for y, (x, line) in right_lines_at_height.items():
            inner_right_lines.add(line)  # Add the leftmost line for this y-level

        # Draw the left innermost lines in red
        color_left = (0, 0, 255)  # Red for the left inner lines
        for (start, end) in inner_left_lines:
            cv2.line(output_image, start, end, color_left, 2)

        # Draw the right innermost lines in purple
        color_right = (255, 0, 255)  # Purple for the right inner lines
        for (start, end) in inner_right_lines:
            cv2.line(output_image, start, end, color_right, 2)

        return output_image, list(inner_left_lines), list(inner_right_lines)

    def fill_polygon_between_lines(self, image, left_inner_lines, right_inner_lines):
        height, width, _ = image.shape
        center_x = width // 2  # Calculate the center x-coordinate of the image

        # If both sides are empty, return an empty mask and empty line arrays
        if (len(left_inner_lines) == 0) and (len(right_inner_lines) == 0):
            return image, np.zeros_like(image), ([], [])

        output_image = image.copy()
        mask = np.zeros_like(image)  # Create a mask with the same dimensions as the image

        # Initialize variables
        left_points = []
        right_points = []
        left_lines_returned = []
        right_lines_returned = []

        # Helper function to create symmetrical points across the center x-coordinate
        def mirror_points_across_center(points):
            mirrored_points = []
            for x, y in points:
                mirrored_x = 2 * center_x - x
                mirrored_points.append((mirrored_x, y))
            return mirrored_points

        # If left_inner_lines is empty, create mirrored left points from right_inner_lines
        if len(left_inner_lines) == 0 and len(right_inner_lines) > 0:
            # Collect points from right_inner_lines and mirror them
            for (start, end) in right_inner_lines:
                right_points.append(start)
                right_points.append(end)
            left_points = mirror_points_across_center(right_points)
            # Create mirrored left lines from mirrored points
            left_lines_returned = []
            for i in range(0, len(left_points), 2):
                if i+1 < len(left_points):
                    left_lines_returned.append((left_points[i], left_points[i+1]))
            # The right lines to return are the original right lines
            right_lines_returned = right_inner_lines
        # If right_inner_lines is empty, create mirrored right points from left_inner_lines
        elif len(right_inner_lines) == 0 and len(left_inner_lines) > 0:
            # Collect points from left_inner_lines
            for (start, end) in left_inner_lines:
                left_points.append(start)
                left_points.append(end)
            right_points = mirror_points_across_center(left_points)
            # Create mirrored right lines from mirrored points
            right_lines_returned = []
            for i in range(0, len(right_points), 2):
                if i+1 < len(right_points):
                    right_lines_returned.append((right_points[i], right_points[i+1]))
            # The left lines to return are the original left lines
            left_lines_returned = left_inner_lines
        else:
            # Both sides have lines; collect their points
            for (start, end) in left_inner_lines:
                left_points.append(start)
                left_points.append(end)
            for (start, end) in right_inner_lines:
                right_points.append(start)
                right_points.append(end)
            # The lines to return are the original lines
            left_lines_returned = left_inner_lines
            right_lines_returned = right_inner_lines

        # Sort both lists by y-coordinate (from top to bottom)
        left_points = sorted(left_points, key=lambda p: p[1])
        right_points = sorted(right_points, key=lambda p: p[1])

        # Ensure that both sides have points to form a polygon
        if len(left_points) == 0 or len(right_points) == 0:
            return output_image, mask, (left_lines_returned, right_lines_returned)  # Return if there's no valid data

        # Create the polygon by combining the left points (in order) and right points (in reverse order)
        polygon_points = np.array(left_points + right_points[::-1], dtype=np.int32)

        # Fill the polygon on the mask with green color (RGB: (0, 255, 0))
        cv2.fillPoly(mask, [polygon_points], (0, 255, 0))

        # Blend the mask with the original image
        output_image = cv2.addWeighted(output_image, 1, mask, 0.5, 0)  # Adjust the blending as needed

        return output_image, mask, (left_lines_returned, right_lines_returned)

    def get_safe_zone(self, image, lane_mask, left_lines, right_lines, factor):
        # Make a copy of the input image to avoid modifying the original
        output_image = image.copy()

        # Check if the lane_mask is empty
        if not np.any(lane_mask):
            # Return the copied image and an empty mask
            safe_zone_mask = np.zeros(output_image.shape[:2], dtype=np.uint8)
            return output_image, safe_zone_mask

        # Ensure factor is between 0 and 1
        factor = np.clip(factor, 0.0, 1.0)

        # Extract left and right boundary points
        left_points = []
        for line in left_lines:
            (x1, y1), (x2, y2) = line
            left_points.append([x1, y1])
            left_points.append([x2, y2])

        right_points = []
        for line in right_lines:
            (x1, y1), (x2, y2) = line
            right_points.append([x1, y1])
            right_points.append([x2, y2])

        # Convert to numpy arrays
        left_points = np.array(left_points)
        right_points = np.array(right_points)

        # Check if there are enough points
        if left_points.shape[0] < 2 or right_points.shape[0] < 2:
            print("Not enough points to compute safe zone.")
            safe_zone_mask = np.zeros(output_image.shape[:2], dtype=np.uint8)
            return output_image, safe_zone_mask  # Return the copied image and an empty mask

        # Sort points by y-coordinate (from top to bottom)
        left_points = left_points[np.argsort(left_points[:, 1])]
        right_points = right_points[np.argsort(right_points[:, 1])]

        # Extract x and y coordinates
        left_x = left_points[:, 0]
        left_y = left_points[:, 1]
        right_x = right_points[:, 0]
        right_y = right_points[:, 1]

        # Define common y-values for interpolation
        y_min = int(max(np.min(left_y), np.min(right_y)))
        y_max = int(min(np.max(left_y), np.max(right_y)))
        if y_min == y_max:
            print("No overlapping y-values between left and right lanes.")
            safe_zone_mask = np.zeros(output_image.shape[:2], dtype=np.uint8)
            return output_image, safe_zone_mask  # Return the copied image and an empty mask
        y_values = np.linspace(y_min, y_max, num=100)

        # Interpolate x-values for left and right boundaries
        x_left_values = np.interp(y_values, left_y, left_x)
        x_right_values = np.interp(y_values, right_y, right_x)

        # Compute center x-values
        x_center_values = (x_left_values + x_right_values) / 2

        # Compute new left and right x-values based on the factor
        x_left_new = x_center_values + factor * (x_left_values - x_center_values)
        x_right_new = x_center_values + factor * (x_right_values - x_center_values)

        # Create new boundary points
        left_boundary_new = np.column_stack((x_left_new, y_values))
        right_boundary_new = np.column_stack((x_right_new, y_values))

        # Combine boundary points to form the polygon
        right_boundary_new = np.flipud(right_boundary_new)
        polygon_points = np.vstack((left_boundary_new, right_boundary_new))
        polygon_points = np.int32([polygon_points])

        # Create a new mask for the safe zone
        safe_zone_mask = np.zeros(output_image.shape[:2], dtype=np.uint8)
        cv2.fillPoly(safe_zone_mask, polygon_points, 255)  # Fill with white color

        # Draw the safe zone mask in blue on the copied image
        blue_mask = np.zeros_like(output_image)
        blue_mask[:, :, 0] = safe_zone_mask  # Assign mask to blue channel

        # Blend the blue mask with the copied image
        alpha = 0.3  # Transparency factor
        cv2.addWeighted(blue_mask, alpha, output_image, 1 - alpha, 0, output_image)

        return output_image, safe_zone_mask

    def get_angle_lines(self, image):
        output_image = image.copy()

        height, width = output_image.shape[:2]

        center_x = width // 2

        line_length = height
        end_point_right = (center_x + line_length, height - line_length)
        end_point_left = (center_x - line_length, height - line_length)
        vertical_line = [center_x]

        slope_right = -1
        intercept_right = height - (slope_right * center_x)
        right_diagonal = [slope_right, intercept_right]

        slope_left = 1 
        intercept_left = height - (slope_left * center_x)
        left_diagonal = [slope_left, intercept_left]

        return output_image, vertical_line, right_diagonal, left_diagonal

    def find_intersections_and_draw(self, image, vertical_line, right_diagonal, left_diagonal, green_mask):
        # Make a copy of the passed-in image
        output_image = image.copy()

        # Function to check for intersections, mark red dots, draw tangent lines, calculate angles, and set in_lane
        def check_intersections(line_points, line_vector, mask, image, original):
            previous_in_mask = False  # To track whether the previous pixel was inside the mask
            in_lane = False  # Boolean to track if the starting point is inside the mask
            intersections = []  # To store intersection objects with angle and (x, y) coordinates

            # If mask has multiple channels (e.g., RGB), convert to single-channel grayscale
            if len(mask.shape) > 2:
                mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

            # Get mask dimensions
            height, width = mask.shape[:2]

            # Step 1: Find the bottom 2% of the mask (highest Y-values)
            mask_points = np.argwhere(mask > 0)
            if mask_points.size == 0:
                return False, intersections

            max_y = np.max(mask_points[:, 0])
            y_threshold = int(0.02 * height)
            bottom_2_percent_points = mask_points[mask_points[:, 0] >= (max_y - y_threshold)]
            if bottom_2_percent_points.size == 0:
                return False, intersections

            min_x = np.min(bottom_2_percent_points[:, 1])
            max_x = np.max(bottom_2_percent_points[:, 1])

            # Step 3: Check the starting point of the line
            x_start, y_start = line_points[0]
            if min_x <= x_start <= max_x:
                in_lane = True  # Starting point is within the bottom 2% region of the mask
            else:
                in_lane = False  # Starting point is outside the bottom 2% region

            if in_lane and original:
                previous_in_mask = True

            # Step 4: Continue checking the rest of the line for intersections
            for point in line_points:
                x, y = point

                if 0 <= x < mask.shape[1] and 0 <= y < mask.shape[0]:
                    if mask[y, x] > 0:
                        if not previous_in_mask:
                            cv2.circle(output_image, (x, y), 5, (0, 0, 255), -1)
                            angle = draw_fitted_line_and_calculate_angle(output_image, mask, x, y, line_vector)
                            intersections.append({"angle": angle, "x": x, "y": y})  # Add the object to the array
                        previous_in_mask = True
                    else:
                        if previous_in_mask:
                            cv2.circle(output_image, (x, y), 5, (0, 0, 255), -1)
                            angle = draw_fitted_line_and_calculate_angle(output_image, mask, x, y, line_vector)
                            intersections.append({"angle": angle, "x": x, "y": y})  # Add the object to the array
                        previous_in_mask = False

            return in_lane, intersections

        # Utility to generate points along a line using Bresenham's algorithm
        def get_line_points(x1, y1, x2, y2):
            points = []
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            sx = 1 if x1 < x2 else -1
            sy = 1 if y1 < y2 else -1
            err = dx - dy
            while True:
                points.append((x1, y1))
                if x1 == x2 and y1 == y2:
                    break
                e2 = err * 2
                if e2 > -dy:
                    err -= dy
                    x1 += sx
                if e2 < dx:
                    err += dx
                    y1 += sy
            return points

        # Function to calculate and draw the best-fitting line based on the closest contour, and calculate angle
        def draw_fitted_line_and_calculate_angle(image, mask, x, y, line_vector):
            _, binary_mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            closest_point = None
            min_dist = float('inf')
            closest_contour = None

            for contour in contours:
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)

                for contour_point in approx:
                    cx, cy = contour_point[0]
                    dist = np.sqrt((cx - x) ** 2 + (cy - y) ** 2)
                    if dist < min_dist:
                        min_dist = dist
                        closest_point = (cx, cy)
                        closest_contour = approx

            if closest_point is not None and closest_contour is not None:
                closest_edge = None
                min_edge_dist = float('inf')
                for i in range(len(closest_contour)):
                    pt1 = tuple(closest_contour[i][0])
                    pt2 = tuple(closest_contour[(i + 1) % len(closest_contour)][0])

                    # Calculate the distance from the point to the edge
                    edge_length = np.linalg.norm(np.array(pt2) - np.array(pt1))
                    if edge_length == 0:
                        continue
                    distance = abs((pt2[0] - pt1[0]) * (pt1[1] - y) - (pt1[0] - x) * (pt2[1] - pt1[1])) / edge_length

                    if distance < min_edge_dist:
                        min_edge_dist = distance
                        closest_edge = (pt1, pt2)

                if closest_edge is not None:
                    pt1, pt2 = closest_edge
                    cv2.line(output_image, pt1, pt2, (255, 0, 255), 2)
                    edge_vector = (pt2[0] - pt1[0], pt2[1] - pt1[1])
                    angle = calculate_angle_between_vectors(line_vector, edge_vector)
                    angle = min(angle, 180 - angle)  # Select the smallest angle
                    cv2.putText(output_image, f'{angle:.2f} deg', (int(x) + 10, int(y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    return angle  # Return the calculated angle

            return 0  # Return 0 if no angle was calculated

        # Function to calculate the angle between two vectors in degrees
        def calculate_angle_between_vectors(v1, v2):
            dot_product = v1[0] * v2[0] + v1[1] * v2[1]
            magnitude_v1 = np.sqrt(v1[0]**2 + v1[1]**2)
            magnitude_v2 = np.sqrt(v2[0]**2 + v2[1]**2)

            if magnitude_v1 == 0 or magnitude_v2 == 0:
                return 0

            cos_theta = dot_product / (magnitude_v1 * magnitude_v2)
            angle_radians = np.arccos(np.clip(cos_theta, -1.0, 1.0))
            angle_degrees = np.degrees(angle_radians)

            return angle_degrees

        # Vertical line points
        vertical_points = get_line_points(vertical_line[0], 0, vertical_line[0], output_image.shape[0])
        vertical_vector = (0, -1)

        # Right diagonal line points
        x_start_right = vertical_line[0]
        y_start_right = output_image.shape[0]
        x_end_right = x_start_right + output_image.shape[0]
        y_end_right = 0
        right_diagonal_points = get_line_points(x_start_right, y_start_right, x_end_right, y_end_right)
        right_diagonal_vector = (1, -1)

        # Left diagonal line points
        x_start_left = vertical_line[0]
        y_start_left = output_image.shape[0]
        x_end_left = x_start_left - output_image.shape[0]
        y_end_left = 0
        left_diagonal_points = get_line_points(x_start_left, y_start_left, x_end_left, y_end_left)
        left_diagonal_vector = (-1, -1)

        # Check intersections for each line with the green mask
        vertical_in_lane, vertical_intersections = check_intersections(vertical_points, vertical_vector, green_mask, output_image, True)
        right_diagonal_in_lane, right_diagonal_intersections = check_intersections(right_diagonal_points, right_diagonal_vector, green_mask, output_image, True)
        left_diagonal_in_lane, left_diagonal_intersections = check_intersections(left_diagonal_points, left_diagonal_vector, green_mask, output_image, True)

        # Sort the intersection points by their y-values in descending order
        vertical_intersections.sort(key=lambda p: p['y'], reverse=True)
        right_diagonal_intersections.sort(key=lambda p: p['y'], reverse=True)
        left_diagonal_intersections.sort(key=lambda p: p['y'], reverse=True)

        car_in_lane = False

        if vertical_in_lane and right_diagonal_in_lane and left_diagonal_in_lane:
            car_in_lane = True

        # Return the modified image, lane status, and arrays of intersections for each line
        return output_image, car_in_lane, left_diagonal_intersections, vertical_intersections, right_diagonal_intersections

    # Determine where the car should go
    def analise_results(self, in_lane, left, middle, right):
        steer = 0
        if in_lane: 
            left_angle = left[0]['angle']
            middle_angle = middle[0]['angle']
            right_angle = right[0]['angle']

            print("Keeping car in lane.")
            if left_angle < right_angle:
                print("Left angle", left_angle)
                print("Right angle", right_angle)
                difference = ((left_angle + right_angle) / 2) - left_angle
                percentage = difference / 90
                steer = -(1 * percentage)
            elif right_angle < left_angle:
                print("Left angle", left_angle)
                print("Right angle", right_angle)
                difference = ((left_angle + right_angle) / 2) - right_angle
                percentage = difference / 90
                steer = (1 * percentage)
            else:
                steer = 0
        else:
            print("Getting the car back in the lane.")
            if len(right) > 0 and len(middle) > 0 and len(left) == 0:
                middle_angle = middle[0]['angle']
                if (middle_angle > 35):
                    steer = 0.08
                elif (middle_angle < 15):
                    steer = 0.17
                else:
                    steer = 0.11
            elif len(left) > 0 and len(middle) > 0 and len(right) == 0:
                middle_angle = middle[0]['angle']
                if (middle_angle > 35):
                    steer = -0.08
                elif (middle_angle < 15):
                    steer = -0.17
                else:
                    steer = -0.11
            elif len(left) == 0 and len(middle) == 0 and len(right) > 0:
                steer = 0.2
            elif len(left) > 0 and len(middle) == 0 and len(right) == 0:
                steer = -0.2
            elif len(left) == 0 and len(middle) == 0 and len(right) == 0:
                steer = 0



        print(f"Steer: {steer}")
        return steer

    def follow_lane(self, out_image, filtered_results, original, previous_left_id=None, previous_right_id=None):
        bottom_length = 200
        top_length = 50
        out_image, lines = self.get_lines(filtered_results, out_image)
        out_image, lines = self.group_lines(out_image, lines)
        out_image, left, right, left_id, right_id = self.get_side_lines(out_image, lines, previous_left_id, previous_right_id) 

        previous_left_id = left_id
        previous_right_id = right_id

        out_image, left, right = self.extend_lines(out_image, left, right)
        out_image, left, right = self.get_inners(out_image, left, right)
        out_image, mask, (left, right) = self.fill_polygon_between_lines(out_image, left, right)
        out_image, mask = self.get_safe_zone(original, mask, left, right, 0.3)

        if np.any(mask):
            out_image, vertical_line, right_diagonal, left_diagonal = self.get_angle_lines(out_image)
            out_image, in_lane, left_intersections, middle_intersections, right_intersections = self.find_intersections_and_draw(out_image, vertical_line, right_diagonal, left_diagonal, mask)

            if in_lane:
                print("The vehicle is in the lane.")

            steer = self.analise_results(in_lane, left_intersections, middle_intersections, right_intersections)

            cv2.putText(out_image, f'Steer: {steer:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            return out_image, mask, steer, previous_left_id, previous_right_id
        else:
            steer = 0
            print("Take manual control of the vehicle.")
            return original, mask, steer, previous_left_id, previous_right_id

    # out_image, mask, steer = follow_lane(out_image, filtered_results, image)   

    def start_following(self, frame, previous_left_id=None, previous_right_id=None):
        if frame.shape[2] == 4:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
            
        model = YOLO('laneTest.pt')
        
        results = model.track(source=frame, persist=True, stream=True)
        out_image, filtered_results = self.filter_detections(results, model, frame)
        res, mask, steer, previous_left_id, previous_right_id = self.follow_lane(out_image, filtered_results, frame, previous_left_id, previous_right_id)
        output = {'steer': steer, 'results': results, 'mask': mask, 'previous_left_id': previous_left_id, 'previous_right_id': previous_right_id}
        return res, output
