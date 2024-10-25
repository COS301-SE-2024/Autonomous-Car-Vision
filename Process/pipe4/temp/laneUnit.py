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
        filtered_results = [] 

        for result in results:
            for i in range(len(result.boxes.cls)):
                class_id = int(result.boxes.cls[i].item()) 
                confidence = result.boxes.conf[i].item()    

                if class_id not in [0, 3, 4] and confidence > 0.5:
                    mask = result.masks.data[i].cpu().numpy()  

                    mask = np.squeeze(mask)  

                    if mask.size > 0:
                        mask_resized = cv2.resize(mask, (image.shape[1], image.shape[0]))

                        binary_mask = (mask_resized > 0.5).astype(np.uint8)

                        colored_mask = np.zeros_like(image, dtype=np.uint8)
                        random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                        colored_mask[binary_mask == 1] = random_color

                        out_image = cv2.addWeighted(out_image, 1, colored_mask, 0.5, 0)

                        filtered_results.append(result)
                    else:
                        print("Empty mask encountered.")
        
        return out_image, filtered_results

    def get_lines(self, filtered_results, image):
        output_image = image.copy()  
        lines = []  

        for result in filtered_results:
            boxes = result.boxes.xyxy  
            ids = result.boxes.id
            masks = result.masks.data 

            for i in range(len(boxes)):
                object_id = int(ids[i]) if ids is not None else None
                class_id = int(result.boxes.cls[i].item())

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
                                        points.append((int(x_bound.item() if isinstance(x_bound, np.ndarray) else x_bound), int(y_bound.item() if isinstance(y_bound, np.ndarray) else y_bound)))
                            else:
                                for x_bound in [x_min, x_max]:
                                    y_bound = vy / vx * (x_bound - x_start) + y_start
                                    if y_min <= y_bound <= y_max:
                                        points.append((int(x_bound.item() if isinstance(x_bound, np.ndarray) else x_bound), int(y_bound.item() if isinstance(y_bound, np.ndarray) else y_bound)))

                            if vy == 0:
                                y_bound = y_start
                                for x_bound in [x_min, x_max]:
                                    if x_min <= x_bound <= x_max:
                                        points.append((int(x_bound.item() if isinstance(x_bound, np.ndarray) else x_bound), int(y_bound.item() if isinstance(y_bound, np.ndarray) else y_bound)))
                            else:
                                for y_bound in [y_min, y_max]:
                                    x_bound = vx / vy * (y_bound - y_start) + x_start
                                    if x_min <= x_bound <= x_max:
                                        points.append((int(x_bound.item() if isinstance(x_bound, np.ndarray) else x_bound), int(y_bound.item() if isinstance(y_bound, np.ndarray) else y_bound)))

                            return points

                        intersections = compute_intersection(x, y, vx, vy, x_min, x_max, y_min, y_max)

                        if len(intersections) >= 2:
                            intersections = sorted(intersections, key=lambda pt: (pt[0], pt[1]))
                            pt1, pt2 = intersections[0], intersections[1]

                            cv2.line(output_image, pt1, pt2, (0, 255, 0), 2)

                            lines.append((pt1, pt2, object_id, class_id))

        return output_image, lines

    def identify_dotted(self, lines, image):
        output_image = image.copy()
        dotted_lines = [line for line in lines if line[3] == 1] 
        other_lines = [line for line in lines if line[3] != 1] 

        groups = []

        def calculate_slope(pt1, pt2):
            if (pt2[0] - pt1[0]) == 0: 
                return float('inf')
            return (pt2[1] - pt1[1]) / (pt2[0] - pt1[0])

        def is_smooth_line(pt1, pt2, pt3):
            slope1 = calculate_slope(pt1, pt2)
            slope2 = calculate_slope(pt2, pt3)
            return abs(slope1 - slope2) < 0.2

        for line in dotted_lines:
            pt1, pt2, _, _ = line
            added_to_group = False

            for group in groups:
                for grouped_line in group:
                    grouped_pt1, grouped_pt2, _, _ = grouped_line

                    if is_smooth_line(grouped_pt1, grouped_pt2, pt1) or is_smooth_line(grouped_pt1, grouped_pt2, pt2):
                        group.append(line)
                        added_to_group = True
                        break
                if added_to_group:
                    break

            if not added_to_group:
                groups.append([line])

        for line in other_lines:
            groups.append([line])

        for group in groups:
            if len(group) > 1:
                group_points = []
                for line in group:
                    group_points.append(line[0])  
                    group_points.append(line[1])  

                group_points = sorted(group_points, key=lambda pt: pt[0])

                for i in range(len(group_points) - 1):
                    pt1 = group_points[i]
                    pt2 = group_points[i + 1]
                    new_line = (pt1, pt2, None, 1)  
                    group.append(new_line)
                    cv2.line(output_image, pt1, pt2, (0, 255, 0), 2) 

        for group in groups:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) 
            for line in group:
                pt1, pt2, _, _ = line
                cv2.line(output_image, pt1, pt2, color, 2)

        return output_image, groups

    def extend_lines(self, groups, image):
        output_image = image.copy()
        height, width, _ = image.shape

        for group in groups:
            lowest_line = max(group, key=lambda line: max(line[0][1], line[1][1]))
            pt1, pt2, _, _ = lowest_line

            if (pt2[0] - pt1[0]) != 0:
                slope = (pt2[1] - pt1[1]) / (pt2[0] - pt1[0])
            else:
                slope = float('inf')

            if slope != float('inf'):
                if pt1[1] > pt2[1]:
                    lower_point = pt1
                else:
                    lower_point = pt2

                extension_length = height - lower_point[1]
                new_x = int(lower_point[0] + extension_length / slope) if slope != 0 else lower_point[0]
                new_y = height
            else:
                new_x = pt1[0]
                new_y = height

            cv2.line(output_image, (lower_point[0], lower_point[1]), (new_x, new_y), (255, 0, 0), 2)
            group.append(((lower_point[0], lower_point[1]), (new_x, new_y), None, 1))

        return output_image, groups

    def get_current_lane(self, groups, image):
        output_image = image.copy()
        height, width, _ = image.shape
        center_x = width // 2

        left_ref_line_start = (int(width * 0.3), height) 
        left_ref_line_end = (int(width * 0.45), int(height * 0.6))  

        right_ref_line_start = (int(width * 0.7), height)  
        right_ref_line_end = (int(width * 0.55), int(height * 0.6)) 

        left_wide_ref_line_start = (int(width * 0.15), height)
        left_wide_ref_line_end = (int(width * 0.35), int(height * 0.6)) 

        right_wide_ref_line_start = (int(width * 0.85), height)
        right_wide_ref_line_end = (int(width * 0.65), int(height * 0.6)) 

        cv2.line(output_image, left_ref_line_start, left_ref_line_end, (255, 0, 0), 2)
        cv2.line(output_image, right_ref_line_start, right_ref_line_end, (0, 0, 255), 2)

        cv2.line(output_image, left_wide_ref_line_start, left_wide_ref_line_end, (255, 0, 255), 2)
        cv2.line(output_image, right_wide_ref_line_start, right_wide_ref_line_end, (255, 0, 255), 2)

        best_left_line = None
        best_right_line = None
        min_left_weighted_dist = float('inf')
        min_right_weighted_dist = float('inf')

        def distance(pt1, pt2):
            return math.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)

        def calculate_slope(pt1, pt2):
            if pt2[0] - pt1[0] == 0:
                return float('inf') 
            return (pt2[1] - pt1[1]) / (pt2[0] - pt1[0])

        def weighted_distance(pt1, pt2, ref_pt1, ref_pt2, expected_slope):
            dist = (distance(pt1, ref_pt1) + distance(pt2, ref_pt2)) / 2
            avg_y = (pt1[1] + pt2[1]) / 2
            proximity_weight = (height - avg_y) / height 

            slope = calculate_slope(pt1, pt2)
            angle_penalty = abs(slope - expected_slope) / abs(expected_slope + 1e-5)

            return dist * (1 - 0.5 * proximity_weight) * (1 + 0.6 * angle_penalty)

        expected_left_slope = (left_ref_line_end[1] - left_ref_line_start[1]) / (left_ref_line_end[0] - left_ref_line_start[0])
        expected_right_slope = (right_ref_line_end[1] - right_ref_line_start[1]) / (right_ref_line_end[0] - right_ref_line_start[0])

        for group in groups:
            for line in group:
                pt1, pt2, _, _ = line
                line_mid_x = (pt1[0] + pt2[0]) / 2

                left_weighted_dist = weighted_distance(pt1, pt2, left_ref_line_start, left_ref_line_end, expected_left_slope)
                right_weighted_dist = weighted_distance(pt1, pt2, right_ref_line_start, right_ref_line_end, expected_right_slope)

                if left_weighted_dist < min_left_weighted_dist and line_mid_x < center_x:
                    min_left_weighted_dist = left_weighted_dist
                    best_left_line = line

                if right_weighted_dist < min_right_weighted_dist and line_mid_x > center_x:
                    min_right_weighted_dist = right_weighted_dist
                    best_right_line = line

        if best_left_line:
            cv2.line(output_image, best_left_line[0], best_left_line[1], (0, 255, 0), 3) 

        if best_right_line:
            cv2.line(output_image, best_right_line[0], best_right_line[1], (0, 255, 0), 3)

        if best_left_line and not best_right_line:
            best_right_line = ((best_left_line[1][0] + 100, best_left_line[1][1]), (best_left_line[0][0] + 100, best_left_line[0][1]), None, 1)
            cv2.line(output_image, best_right_line[0], best_right_line[1], (0, 255, 0), 3)

        if best_right_line and not best_left_line:
            best_left_line = ((best_right_line[1][0] - 100, best_right_line[1][1]), (best_right_line[0][0] - 100, best_right_line[0][1]), None, 1)
            cv2.line(output_image, best_left_line[0], best_left_line[1], (0, 255, 0), 3)

        return output_image, best_left_line, best_right_line, (left_wide_ref_line_start, left_wide_ref_line_end), (right_wide_ref_line_start, right_wide_ref_line_end)

    def analyse_steering(self, best_left_line, best_right_line, left_ref_line, right_ref_line, image_width):
        left_ref_start, left_ref_end = left_ref_line
        right_ref_start, right_ref_end = right_ref_line

        center_x = image_width // 2

        steering_value = 0
        steering_multiplier = 1.3

        if best_left_line and best_right_line:
            left_line_mid_x = (best_left_line[0][0] + best_left_line[1][0]) / 2
            right_line_mid_x = (best_right_line[0][0] + best_right_line[1][0]) / 2

            lane_center_x = (left_line_mid_x + right_line_mid_x) / 2

            deviation = lane_center_x - center_x

            steering_value = deviation / (image_width / 2)

        elif best_left_line:
            left_line_mid_x = (best_left_line[0][0] + best_left_line[1][0]) / 2
            deviation = left_line_mid_x - left_ref_start[0]

            steering_value = deviation / (image_width / 2)

        elif best_right_line:
            right_line_mid_x = (best_right_line[0][0] + best_right_line[1][0]) / 2
            deviation = right_line_mid_x - right_ref_start[0]

            steering_value = deviation / (image_width / 2)

        steering_value = steering_value * steering_multiplier

        steering_value = max(min(steering_value, 1), -1)

        return steering_value
    
    def follow_lane(self, out_image, filtered_results, original):
        bottom_length = 200
        top_length = 50
        
        out_image, lines = self.get_lines(filtered_results, out_image)
        out_image, groups = self.identify_dotted(lines, out_image)
        
        out_image, left_line, right_line, left_ref_line, right_ref_line = self.get_current_lane(groups, out_image)
        
        image_width = out_image.shape[1] 
        steering_value = self.analyse_steering(left_line, right_line, left_ref_line, right_ref_line, image_width)
        
        return out_image, None, steering_value


    def apply_blue_filter(self, frame):
        frame = frame.astype(np.float32)

        frame[:, :, 0] = frame[:, :, 0] * blue_channel  

        frame = np.clip(frame, 0, 255).astype(np.uint8)

        return frame

    def start_following(self, frame):
        filtered_frame = self.apply_blue_filter(frame)

        model = YOLO('laneTest.pt')

        results = model(frame)

        out_image, filtered_results = self.filter_detections(results, model, frame)

        res, mask, steer = self.follow_lane(out_image, filtered_results, frame)

        output = {'image': res,'steering': steer, 'results': results, 'mask': mask}
        return res, output
