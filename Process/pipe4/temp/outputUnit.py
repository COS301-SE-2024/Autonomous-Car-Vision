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
        annotated_frame = image.copy()
        min_distances = [] 

        if (self.lidar or self.all) and data_token.get_flag('has_lidar_data'):
            lidar_data = data_token.get_processing_result('infusrUnit')
            pixel_x = lidar_data['pixel_x']
            pixel_y = lidar_data['pixel_y']
            colors = lidar_data['colors']
            for i in range(len(pixel_x)):
                color = (int(colors[i][2]), int(colors[i][1]), int(colors[i][0]))
                cv2.circle(annotated_frame, (pixel_x[i], pixel_y[i]), radius=2, color=color, thickness=-1)

        if (self.taggr or self.all) and data_token.get_flag('has_tagger_data'):
            tagger_data = data_token.get_processing_result('taggrUnit')
            pixel_data = tagger_data['pixel_data']

            min_distances = [None] * len(pixel_data)

            for data in pixel_data:
                pixel_x = data['pixel_x']
                pixel_y = data['pixel_y']
                min_distance = data['min_distance']
                bbox_index = data['bbox_index'] 

                cv2.circle(annotated_frame, (pixel_x, pixel_y), radius=2, color=(0, 255, 0), thickness=-1)
                
                if min_distances[bbox_index] is None or min_distance < min_distances[bbox_index]:
                    min_distances[bbox_index] = min_distance

        if (self.bb or self.all)and data_token.get_flag('has_bb_data'):
            bounding_boxes = data_token.get_processing_result('yoloUnit')
            for i, bbox in enumerate(bounding_boxes):
                x_min, y_min, x_max, y_max, score, class_id = bbox
                x_min, y_min, x_max, y_max = int(x_min), int(y_min), int(x_max), int(y_max)
                cv2.rectangle(annotated_frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 1)
                
                if min_distances and min_distances[i] is not None:
                    if min_distances[i] is not None:
                        text = f"{bbox[-1]}  Dist: {min_distances[i]:.2f}m"
                        cv2.putText(annotated_frame, text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    else:
                        text = f"{bbox[-1]}"
                        cv2.putText(annotated_frame, text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        if (self.la or self.all) and data_token.get_flag('has_lane_data'):
            output = data_token.get_processing_result('laneUnit')
            mask = output['mask']
            
            if len(mask.shape) == 3 and mask.shape[2] == 3:
                mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

            if mask.shape != annotated_frame.shape[:2]:
                mask = cv2.resize(mask, (annotated_frame.shape[1], annotated_frame.shape[0]), interpolation=cv2.INTER_NEAREST)

            colored_mask = np.zeros_like(annotated_frame)
            colored_mask[mask > 0] = [0, 255, 0] 

            alpha = 0.5
            annotated_frame = cv2.addWeighted(annotated_frame, 1 - alpha, colored_mask, alpha, 0)
            

        print(f"{self.id}: Outputting final result with shape: {annotated_frame.shape}")
        return annotated_frame
