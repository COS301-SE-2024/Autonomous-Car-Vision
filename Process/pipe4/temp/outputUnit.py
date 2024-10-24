from units import Unit
import numpy as np
import cv2
from dataToken import DataToken


class outputUnit(Unit):
    def __init__(self):
        super().__init__(id="outputUnit", input_type=DataToken, output_type=np.ndarray)
        self.all = False
        self.lidar = False
        self.taggr = False
        self.bb = False
        self.la = False

    def set_flags(self, flags):
        if 'all' in flags:
            self.all = True
        if 'lidar' in flags:
            self.lidar = True
        if 'taggr' in flags:
            self.taggr = True
        if 'bb' in flags:
            self.bb = True
        if 'la' in flags:
            self.la = True

    def process(self, data_token):
        image = data_token.get_sensor_data('camera')
        image_two = data_token.get_sensor_data('camera_two')
        annotated_frame = image.copy()
        min_distances = []
        img_lidar = None
        img_taggr = None
        img_bb = None
        img_la = None

        if (self.lidar or self.all) and data_token.get_flag('has_lidar_data'):
            lidar_data = data_token.get_processing_result('infusrUnit')
            if lidar_data:

                pixel_x = lidar_data['pixel_x']
                pixel_y = lidar_data['pixel_y']
                colors = lidar_data['colors']
                img_lidar = image.copy()
                for i in range(len(pixel_x)):
                    color = (int(colors[i][2]), int(colors[i][1]), int(colors[i][0]))
                    cv2.circle(annotated_frame, (pixel_x[i], pixel_y[i]), radius=2, color=color, thickness=-1)
                    cv2.circle(img_lidar, (pixel_x[i], pixel_y[i]), radius=1, color=color, thickness=-1)

        if (self.taggr or self.all) and data_token.get_flag('has_tagger_data'):
            tagger_data = data_token.get_processing_result('taggrUnit')
            pixel_data = tagger_data['pixel_data']
            min_distances = [None] * len(pixel_data)
            img_taggr = image.copy()

            for data in pixel_data:
                pixel_x = data['pixel_x']
                pixel_y = data['pixel_y']
                min_distance = data['min_distance']
                bbox_index = data['bbox_index']

                cv2.circle(annotated_frame, (pixel_x, pixel_y), radius=1, color=(0, 255, 0), thickness=-1)
                cv2.circle(img_taggr, (pixel_x, pixel_y), radius=1, color=(0, 255, 0), thickness=-1)
                if (bbox_index < len(min_distances)) and (min_distances[bbox_index] is not None) and (min_distance < min_distances[bbox_index]):
                    min_distances[bbox_index] = min_distance

        if (self.bb or self.all) and data_token.get_flag('has_bb_data'):
            bounding_boxes = data_token.get_processing_result('yoloUnit')
            img_bb = image.copy()

            for i, bbox in enumerate(bounding_boxes):
                x_min, y_min, x_max, y_max, score, class_id = bbox
                x_min, y_min, x_max, y_max = int(x_min), int(y_min), int(x_max), int(y_max)

                cv2.rectangle(annotated_frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 1)
                cv2.rectangle(img_bb, (x_min, y_min), (x_max, y_max), (0, 255, 0), 1)

                if min_distances is not None and i < len(min_distances) and min_distances[i] is not None:
                    text = f"{bbox[-1]}  Dist: {min_distances[i]:.2f}m"
                    cv2.putText(annotated_frame, text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                    cv2.putText(img_bb, text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                else:
                    text = f"{bbox[-1]}"
                    cv2.putText(annotated_frame, text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                    cv2.putText(img_bb, text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)


        if (self.la or self.all) and data_token.get_flag('has_lane_data'):
            output = data_token.get_processing_result('laneUnit')
            mask = output.get('mask', None)
            # Extract relevant lines from the output
            left_line_points = output.get('left_line', [])
            right_line_points = output.get('right_line', [])
            red_line_points = output.get('red_line_points', [])
            follow_line_points = output.get('follow_line', [])
            # print(left_line_points, right_line_points, red_line_points, follow_line_points)

            # Prepare mask processing
            if mask is not None:
                if len(mask.shape) == 3 and mask.shape[2] == 3:
                    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

                if mask.shape != annotated_frame.shape[:2]:
                    mask = cv2.resize(mask, (annotated_frame.shape[1], annotated_frame.shape[0]), interpolation=cv2.INTER_NEAREST)

                # Apply the green mask overlay to the frame
                colored_mask = np.zeros_like(annotated_frame)
                colored_mask[mask > 0] = [0, 255, 0]  # Green mask

                alpha = 0.5
                img_la = image_two.copy()
                img_la = cv2.addWeighted(img_la, 1 - alpha, colored_mask, alpha, 0)

            # Draw the left field line using the best-fit line
            if left_line_points:
                points = np.array(left_line_points)
                y_coords = points[:, 0]
                x_coords = points[:, 1]
                if len(points) > 1:
                    # Calculate the best-fit line
                    best_fit = np.polyfit(y_coords, x_coords, 1)
                    slope = best_fit[0]
                    intercept = best_fit[1]

                    # Calculate points at the top and bottom of the image
                    y1 = 0
                    x1 = int(slope * y1 + intercept)
                    y2 = annotated_frame.shape[0] - 1
                    x2 = int(slope * y2 + intercept)

                    # Draw the line
                    cv2.line(annotated_frame, (x1, y1), (x2, y2), (57, 255, 20), 2)  # Neon green color

            # Draw the right field line using the best-fit line
            if right_line_points:
                points = np.array(right_line_points)
                y_coords = points[:, 0]
                x_coords = points[:, 1]
                if len(points) > 1:
                    # Calculate the best-fit line
                    best_fit = np.polyfit(y_coords, x_coords, 1)
                    slope = best_fit[0]
                    intercept = best_fit[1]

                    # Calculate points at the top and bottom of the image
                    y1 = 0
                    x1 = int(slope * y1 + intercept)
                    y2 = annotated_frame.shape[0] - 1
                    x2 = int(slope * y2 + intercept)

                    # Draw the line
                    cv2.line(annotated_frame, (x1, y1), (x2, y2), (0, 150, 150), 2)  # Neon green color

            # Draw the red origin line (vertical center line)
            if red_line_points:
                pt1 = tuple(red_line_points[0])
                pt2 = tuple(red_line_points[1])
                cv2.line(annotated_frame, pt1, pt2, (0, 0, 255), 2)  # Red color (BGR: 0, 0, 255)

            # Draw the follow line (blue line) using the best-fit line
            if follow_line_points:
                points = np.array(follow_line_points)
                x_coords = points[:, 0]
                y_coords = points[:, 1]
                if len(points) > 1:
                    # Calculate the best-fit line
                    best_fit = np.polyfit(y_coords, x_coords, 1)
                    slope = best_fit[0]
                    intercept = best_fit[1]

                    # Calculate points at the top and bottom of the image
                    y1 = 0
                    x1 = int(slope * y1 + intercept)
                    y2 = annotated_frame.shape[0] - 1
                    x2 = int(slope * y2 + intercept)

                    # Draw the line
                    cv2.line(annotated_frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Blue color



        # print(f"{self.id}: Outputting final result with shape: {annotated_frame.shape}, ")
        return annotated_frame, img_lidar, img_taggr, img_bb, img_la

