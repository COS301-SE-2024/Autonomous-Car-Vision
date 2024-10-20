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
        
        if (output):
            previous_left_id = output.get('previous_left_id', None)
            previous_right_id = output.get('previous_right_id', None)
        else:
            previous_left_id = None
            previous_right_id = None
        
        res, output = self.start_following(image, previous_left_id, previous_right_id)

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
        bottom_center = (width // 2, height - 1)

        # Sort each group based on the x-coordinates of their start points
        sorted_groups = sorted(groups, key=lambda group: min(line[0][0] for line in group))

        # Iterate over the groups to find the current lane that contains the bottom center point
        for i in range(len(sorted_groups) - 1):
            left_group = sorted_groups[i]
            right_group = sorted_groups[i + 1]

            # Get all start and end points from the lines in the two groups
            left_points = list(itertools.chain.from_iterable([(line[0], line[1]) for line in left_group]))
            right_points = list(itertools.chain.from_iterable([(line[0], line[1]) for line in right_group]))

            # Sort points to form a polygon (we use x-coordinates to help sorting)
            left_points = sorted(left_points, key=lambda pt: pt[1])  # Sort by y-coordinate
            right_points = sorted(right_points, key=lambda pt: pt[1], reverse=True)  # Sort by y-coordinate in reverse

            # Create a polygon that connects the left and right line points
            polygon_points = left_points + right_points

            # Convert points to a numpy array in the format required by pointPolygonTest
            polygon_points_np = np.array(polygon_points, np.int32)

            # Check if the bottom center point is inside the polygon
            if cv2.pointPolygonTest(polygon_points_np, bottom_center, False) >= 0:
                # Fill the polygon with green color to indicate the current lane
                cv2.fillPoly(output_image, [polygon_points_np.reshape((-1, 1, 2))], (0, 255, 0))
                left_lines = [(line[0], line[1]) for line in left_group]
                right_lines = [(line[0], line[1]) for line in right_group]
                lane_mask = np.zeros(output_image.shape[:2], dtype=np.uint8)
                cv2.fillPoly(lane_mask, [polygon_points_np.reshape((-1, 1, 2))], 255)
                return output_image, lane_mask, left_lines, right_lines

        return output_image, None, None, None

    def get_safe_zone(self, image, lane_mask, left_lines, right_lines, factor):
        output_image = image.copy()

        if not np.any(lane_mask):
            safe_zone_mask = np.zeros(output_image.shape[:2], dtype=np.uint8)
            return output_image, safe_zone_mask

        factor = np.clip(factor, 0.0, 1.0)

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

        left_points = np.array(left_points)
        right_points = np.array(right_points)

        if left_points.shape[0] < 2 or right_points.shape[0] < 2:
            print("Not enough points to compute safe zone.")
            safe_zone_mask = np.zeros(output_image.shape[:2], dtype=np.uint8)

        left_points = left_points[np.argsort(left_points[:, 1])]
        right_points = right_points[np.argsort(right_points[:, 1])]

        left_x = left_points[:, 0]
        left_y = left_points[:, 1]
        right_x = right_points[:, 0]
        right_y = right_points[:, 1]

        y_min = int(max(np.min(left_y), np.min(right_y)))
        y_max = int(min(np.max(left_y), np.max(right_y)))
        if y_min == y_max:
            print("No overlapping y-values between left and right lanes.")
            safe_zone_mask = np.zeros(output_image.shape[:2], dtype=np.uint8)
            return output_image, safe_zone_mask 
        y_values = np.linspace(y_min, y_max, num=100)

        x_left_values = np.interp(y_values, left_y, left_x)
        x_right_values = np.interp(y_values, right_y, right_x)

        x_center_values = (x_left_values + x_right_values) / 2

        x_left_new = x_center_values + factor * (x_left_values - x_center_values)
        x_right_new = x_center_values + factor * (x_right_values - x_center_values)

        left_boundary_new = np.column_stack((x_left_new, y_values))
        right_boundary_new = np.column_stack((x_right_new, y_values))

        right_boundary_new = np.flipud(right_boundary_new)
        polygon_points = np.vstack((left_boundary_new, right_boundary_new))
        polygon_points = np.int32([polygon_points])

        safe_zone_mask = np.zeros(output_image.shape[:2], dtype=np.uint8)
        cv2.fillPoly(safe_zone_mask, polygon_points, 255)

        blue_mask = np.zeros_like(output_image)
        blue_mask[:, :, 0] = safe_zone_mask

        alpha = 0.3 
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
        output_image = image.copy()
        
        def check_intersections(line_points, line_vector, mask, image, original):
            previous_in_mask = False 
            in_lane = False 
            intersections = [] 

            if len(mask.shape) > 2:
                mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

            height, width = mask.shape[:2]

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

            x_start, y_start = line_points[0]
            if min_x <= x_start <= max_x:
                in_lane = True  
            else:
                in_lane = False 

            if in_lane and original:
                previous_in_mask = True

            for point in line_points:
                x, y = point

                if 0 <= x < mask.shape[1] and 0 <= y < mask.shape[0]:
                    if mask[y, x] > 0:
                        if not previous_in_mask:
                            cv2.circle(output_image, (x, y), 5, (0, 0, 255), -1)
                            angle = draw_fitted_line_and_calculate_angle(output_image, mask, x, y, line_vector)
                            intersections.append({"angle": angle, "x": x, "y": y})
                        previous_in_mask = True
                    else:
                        if previous_in_mask:
                            cv2.circle(output_image, (x, y), 5, (0, 0, 255), -1)
                            angle = draw_fitted_line_and_calculate_angle(output_image, mask, x, y, line_vector)
                            intersections.append({"angle": angle, "x": x, "y": y})
                        previous_in_mask = False

            return in_lane, intersections

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
                    angle = min(angle, 180 - angle)  
                    cv2.putText(output_image, f'{angle:.2f} deg', (int(x) + 10, int(y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    return angle 

            return 0 

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

        vertical_points = get_line_points(vertical_line[0], 0, vertical_line[0], output_image.shape[0])
        vertical_vector = (0, -1)

        x_start_right = vertical_line[0]
        y_start_right = output_image.shape[0]
        x_end_right = x_start_right + output_image.shape[0]
        y_end_right = 0
        right_diagonal_points = get_line_points(x_start_right, y_start_right, x_end_right, y_end_right)
        right_diagonal_vector = (1, -1)

        x_start_left = vertical_line[0]
        y_start_left = output_image.shape[0]
        x_end_left = x_start_left - output_image.shape[0]
        y_end_left = 0
        left_diagonal_points = get_line_points(x_start_left, y_start_left, x_end_left, y_end_left)
        left_diagonal_vector = (-1, -1)

        vertical_in_lane, vertical_intersections = check_intersections(vertical_points, vertical_vector, green_mask, output_image, True)
        right_diagonal_in_lane, right_diagonal_intersections = check_intersections(right_diagonal_points, right_diagonal_vector, green_mask, output_image, True)
        left_diagonal_in_lane, left_diagonal_intersections = check_intersections(left_diagonal_points, left_diagonal_vector, green_mask, output_image, True)

        vertical_intersections.sort(key=lambda p: p['y'], reverse=True)
        right_diagonal_intersections.sort(key=lambda p: p['y'], reverse=True)
        left_diagonal_intersections.sort(key=lambda p: p['y'], reverse=True)

        car_in_lane = False

        if vertical_in_lane and right_diagonal_in_lane and left_diagonal_in_lane:
            car_in_lane = True

        return output_image, car_in_lane, left_diagonal_intersections, vertical_intersections, right_diagonal_intersections

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


    def follow_lane(self, out_image, filtered_results, original):
        bottom_length = 200
        top_length = 50
        out_image, lines = self.get_lines(filtered_results, out_image)
        out_image, groups = self.identify_dotted(lines, out_image)
        out_image, groups = self.extend_lines(groups, out_image)
        out_image, lane_mask, left_lines, right_lines = self.get_current_lane(groups, out_image)
        out_image, mask = self.get_safe_zone(original, lane_mask, left_lines, right_lines, 0.3)

        if np.any(mask):
            out_image, vertical_line, right_diagonal, left_diagonal = self.get_angle_lines(out_image)
            out_image, in_lane, left_intersections, middle_intersections, right_intersections = self.find_intersections_and_draw(out_image, vertical_line, right_diagonal, left_diagonal, mask)
            if in_lane:
                print("The vehicle is in the lane.")
            steer = self.analise_results(in_lane, left_intersections, middle_intersections, right_intersections)
            cv2.putText(out_image, f'Steer: {steer:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            return out_image, mask, steer
        else:
            steer = 0
            print("Take manual control of the vehicle.")
            return original, mask, steer


    def start_following(self, frame, previous_left_id=None, previous_right_id=None):
        # # Convert RGBA to RGB if needed
        # if frame.shape[2] == 4:
        #     frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)

        # # Get original frame dimensions
        # original_height, original_width = frame.shape[:2]
        
        # cutoff_percent=0

        # # Calculate the height of the cropped frame
        # crop_height = int(original_height * (1 - cutoff_percent / 100.0))

        # # Crop the frame (keep only the top part)
        # cropped_frame = frame[:crop_height, :]

        # Load the YOLO model
        model = YOLO('laneTest.pt')

        # Run detection on the cropped frame
        results = model.track(source=frame, persist=True, stream=True)

        # Filter the detections and prepare for further steps
        out_image, filtered_results = self.filter_detections(results, model, frame)

        # Pass the original frame, not the cropped one, to the follow_lane function
        res, mask, steer = self.follow_lane(out_image, filtered_results, frame)

        # Return results
        output = {'image': res,'steer': steer, 'results': results, 'mask': mask, 'previous_left_id': None, 'previous_right_id': None}
        return res, output
