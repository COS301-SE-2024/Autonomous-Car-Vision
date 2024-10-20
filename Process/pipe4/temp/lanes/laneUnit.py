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
        
        if (output):
            previous_left_id = output.get('previous_left_id', None)
            previous_right_id = output.get('previous_right_id', None)
        else:
            previous_left_id = None
            previous_right_id = None

        output_image, lines, solid_line_points, red_line_points, green_line_points, steering = self.start_following(image, previous_left_id, previous_right_id)
        lane_processing_result = {
            'output_image': output_image,  # Optional: Save the image path or a smaller representation
            'lines':lines,  # Convert line data
            'solid_line_points': solid_line_points,  # List of solid line points
            'red_line_points': red_line_points,  # List of red line points (origin line)
            'green_line_points': green_line_points,  # List of green line points (recommended line)
            'steering': steering,  # The calculated steering value
           # Right lane ID from the previous frame
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


    def get_lines(self, filtered_results, image):
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
            steering = self.calculate_best_intersection_and_steering(
                best_fit_slope, image_center[0], best_fit_intercept, green_midpoint
            )
            print(f"Steering angle: {steering}")  # Output the steering angle

        else:
            steering = None

        return output_image, lines, solid_line_points, red_line_points, green_line_points, steering

    def follow_lane(self, out_image, filtered_results, original, previous_left_id=None, previous_right_id=None):
        bottom_length = 200
        top_length = 50
        output_image, lines, solid_line_points, red_line_points, green_line_points, steering = self.get_lines(filtered_results, out_image)

        return output_image, lines, solid_line_points, red_line_points, green_line_points, steering


    def start_following(self, frame, previous_left_id=None, previous_right_id=None):
        # Convert RGBA to RGB if needed
        if frame.shape[2] == 4:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)

        # Get original frame dimensions
        original_height, original_width = frame.shape[:2]
        
        cutoff_percent=37

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
        output_image, lines, solid_line_points, red_line_points, green_line_points, steering= self.follow_lane(out_image, filtered_results, frame, previous_left_id, previous_right_id)

        # Return results
        # output = {'image': res,'steer': steer, 'results': results, 'mask': mask, 'previous_left_id': previous_left_id, 'previous_right_id': previous_right_id}
        return output_image, lines, solid_line_points, red_line_points, green_line_points, steering
