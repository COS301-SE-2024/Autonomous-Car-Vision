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

        if output:
            previous_left_id = output.get('previous_left_id', None)
            previous_right_id = output.get('previous_right_id', None)
        else:
            previous_left_id = None
            previous_right_id = None

        output_image, lines, solid_line_points, red_line_points, green_line_points, steering = self.start_following(image, previous_left_id, previous_right_id)
        lane_processing_result = {
            'output_image': output_image,  # Optional: Save the image path or a smaller representation
            'lines': lines,  # Convert line data
            'solid_line_points': solid_line_points,  # List of solid line points
            'red_line_points': red_line_points,  # List of red line points (origin line)
            'green_line_points': green_line_points,  # List of green line points (recommended line)
            'steering': steering,  # The calculated steering value
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
            result_copy = copy.deepcopy(result)

            for i in range(len(result.boxes.cls)):
                class_id = int(result.boxes.cls[i].item())
                confidence = result.boxes.conf[i].item()

                if class_id not in [0, 3, 4] and confidence > 0.5:
                    mask = result.masks.data[i].cpu().numpy()
                    mask = np.squeeze(mask)

                    if mask.size > 0:
                        original_mask_shape = mask.shape
                        mask_resized = cv2.resize(mask, (image.shape[1], crop_height), interpolation=cv2.INTER_NEAREST)

                        binary_mask = (mask_resized > 0.5).astype(np.uint8)

                        colored_mask = np.zeros_like(image, dtype=np.uint8)

                        colored_mask[:crop_height, :] = np.stack([binary_mask] * 3, axis=-1) * 255

                        out_image = cv2.addWeighted(out_image, 1, colored_mask, 0.5, 0)

                        full_mask = np.zeros((height, width), dtype=np.uint8)
                        full_mask[:crop_height, :] = binary_mask

                        full_mask_resized = cv2.resize(full_mask, (original_mask_shape[1], original_mask_shape[0]), interpolation=cv2.INTER_NEAREST)

                        result_copy.masks.data[i] = torch.tensor(full_mask_resized).cpu()

                        x_min, y_min, x_max, y_max = result.boxes.xyxy[i].cpu().numpy()
                        result_copy.boxes.xyxy[i] = torch.tensor([x_min, y_min, x_max, y_max])

                        filtered_results.append(result_copy)
                    else:
                        print("Empty mask encountered.")

        return out_image, filtered_results

    def calculate_best_intersection_and_steering(self, green_slope, image_center_x, green_intercept, green_midpoint):
        red_line_x = image_center_x

        if green_slope is not None:
            green_y_at_red_x = green_slope * red_line_x + green_intercept

            if 0 <= green_y_at_red_x <= 1:
                angle_radians = np.arctan(green_slope)

                max_angle = np.pi / 2
                steering = angle_radians / max_angle

                return np.clip(steering, -1, 1)

        red_origin = (image_center_x, 0)

        green_midpoint_x, green_midpoint_y = green_midpoint

        base = green_midpoint_x - image_center_x
        height = green_midpoint_y

        if height == 0:
            return 0.0

        angle_radians = np.arctan2(base, height)

        max_angle = np.pi / 2
        steering = angle_radians / max_angle

        return np.clip(steering, -1, 1)

    def get_lines(self, filtered_results, image):
        output_image = image.copy()
        lines = []
        image_height = image.shape[0]
        image_center = (image.shape[1] // 2, image.shape[0] // 2)
        closest_line = None
        min_distance = float('inf')
        dotted_points = []
        fallback_lines = []

        purple_lines = []
        solid_line_points = []
        divisor_points = []

        for result in filtered_results:
            boxes = result.boxes.xyxy
            ids = result.boxes.id
            masks = result.masks.data
            class_ids = result.boxes.cls

            for i in range(len(boxes)):
                object_id = int(ids[i]) if ids is not None else None
                class_id = int(class_ids[i].item())
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

                            # For both double and solid lines, we treat them the same, evaluating distance
                            if class_id in [2, 5]:  # 2: double-line, 5: solid-line
                                purple_lines.append((pt1, pt2))
                                lines.append((pt1, pt2, object_id))
                                fallback_lines.append((pt1, pt2))

                                midpoint = ((pt1[0] + pt2[0]) // 2, (pt1[1] + pt2[1]) // 2)
                                distance_to_center = abs(midpoint[0] - image_center[0])

                                # Update closest line regardless of class_id
                                if distance_to_center < min_distance:
                                    min_distance = distance_to_center
                                    solid_line_points = [pt1, pt2]
                                    closest_line = (pt1, pt2)

                            if class_id == 1:
                                midpoint = ((pt1[0] + pt2[0]) // 2, (pt1[1] + pt2[1]) // 2)
                                dotted_points.append(midpoint)

        for pt1, pt2 in purple_lines:
            cv2.line(output_image, pt1, pt2, (128, 0, 128), 2)

        best_fit_slope, best_fit_intercept = None, None
        if len(dotted_points) > 1:
            x_coords, y_coords = zip(*dotted_points)
            median_x = np.median(x_coords)
            median_y = np.median(y_coords)

            threshold_x = 0.2 * median_x
            threshold_y = 0.2 * median_y

            filtered_points = [
                (x, y) for x, y in dotted_points
                if abs(x - median_x) < threshold_x and abs(y - median_y) < threshold_y
            ]

            if len(filtered_points) > 1:
                filtered_x, filtered_y = zip(*filtered_points)

                best_fit_slope, best_fit_intercept = np.polyfit(filtered_y, filtered_x, 1)

                for y in range(image_height):
                    x = int(best_fit_slope * y + best_fit_intercept)
                    if 0 <= x < image.shape[1]:
                        output_image[y, x] = (255, 105, 180)
                    divisor_points.append((x, y))

        elif len(fallback_lines) > 0:
            pt1, pt2 = fallback_lines[0]
            cv2.line(output_image, pt1, pt2, (255, 105, 180), 2)
            divisor_points.append(pt1)
            divisor_points.append(pt2)

        else:
            print("Error: No valid dotted, solid, or double lines found for the divisor.")

        red_line_points = [(image_center[0], 0), (image_center[0], image.shape[0])]
        cv2.line(output_image, red_line_points[0], red_line_points[1], (0, 0, 255), 2)

        solid_slope, solid_intercept = None, None
        if len(solid_line_points) > 1:
            solid_x, solid_y = zip(*solid_line_points)
            solid_slope, solid_intercept = np.polyfit(solid_y, solid_x, 1)

            for y in range(image_height):
                x = int(solid_slope * y + solid_intercept)
                if 0 <= x < image.shape[1]:
                    output_image[y, x] = (0, 165, 255)

        green_line_points = []
        if best_fit_slope is not None and solid_slope is not None:
            for y in range(image_height):
                best_fit_x = int(best_fit_slope * y + best_fit_intercept)
                solid_x = int(solid_slope * y + solid_intercept)
                midpoint_x = (best_fit_x + solid_x) // 2

                if 0 <= midpoint_x < image.shape[1]:
                    output_image[y, midpoint_x] = (0, 255, 0)
                    green_line_points.append((midpoint_x, y))

            green_midpoint_x = None
            if green_line_points and len(green_line_points) > 1:  # Null-safe check
                green_midpoint_x = (green_line_points[0][0] + green_line_points[-1][0]) // 2
                green_midpoint = (green_midpoint_x, image_height - 1)

                steering = self.calculate_best_intersection_and_steering(
                    best_fit_slope, image_center[0], best_fit_intercept, green_midpoint
                )
                print(f"Steering angle: {steering}")
            else:
                print("Warning: No green line points detected. Steering cannot be calculated.")
                steering = None

        else:
            steering = None

        return output_image, lines, solid_line_points, red_line_points, green_line_points, steering

    def follow_lane(self, out_image, filtered_results, original, previous_left_id=None, previous_right_id=None):
        output_image, lines, solid_line_points, red_line_points, green_line_points, steering = self.get_lines(filtered_results, out_image)

        return output_image, lines, solid_line_points, red_line_points, green_line_points, steering

    def start_following(self, frame, previous_left_id=None, previous_right_id=None):
        if frame.shape[2] == 4:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)

        original_height, original_width = frame.shape[:2]

        cutoff_percent = 37

        crop_height = int(original_height * (1 - cutoff_percent / 100.0))

        cropped_frame = frame[:crop_height, :]

        model = YOLO('laneTest.pt')

        results = model.track(source=cropped_frame, persist=True, stream=True)

        out_image, filtered_results = self.filter_detections(results, model, frame, crop_height)

        output_image, lines, solid_line_points, red_line_points, green_line_points, steering = self.follow_lane(out_image, filtered_results, frame, previous_left_id, previous_right_id)

        return output_image, lines, solid_line_points, red_line_points, green_line_points, steering
