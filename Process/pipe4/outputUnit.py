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


    def set_flags(self, flags):
        if 'all' in flags:
            self.all = True
        if 'lidar' in flags:
            self.lidar = True
        if 'taggr' in flags:
            self.taggr = True
        if 'bb' in flags:
            self.bb = True


    def process(self, data_token):
        image = data_token.get_sensor_data('camera')
        annotated_frame = image.copy()
        min_distance = None

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
            region_pixel_x, region_pixel_y = tagger_data['region_pixel_x'], tagger_data['region_pixel_y']
            min_distance = tagger_data['min_distance']
            for i in range(len(region_pixel_x)):
                cv2.circle(annotated_frame, (region_pixel_x[i], region_pixel_y[i]), radius=2, color=(0, 255, 0),
                           thickness=-1)

        if (self.bb or self.all):
            bounding_boxes = data_token.get_processing_result('yoloUnit')
            for bbox in bounding_boxes:
                x_min, y_min, x_max, y_max, score, class_id = bbox
                x_min, y_min, x_max, y_max = int(x_min), int(y_min), int(x_max), int(y_max)
                cv2.rectangle(annotated_frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                text = f"{bbox[-1]}  {min_distance if min_distance else ''}"
                cv2.putText(annotated_frame, text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        print(f"{self.id}: Outputting final result with shape: {annotated_frame.shape}")
        return annotated_frame
