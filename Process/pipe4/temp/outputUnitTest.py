from units import Unit
import numpy as np
import cv2
from dataToken import DataToken


class outputUnitTest(Unit):
    def __init__(self):
        super().__init__(id="outputUnitTest", input_type=DataToken, output_type=np.ndarray)
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
        img_lidar = None
        img_taggr = None
        img_bb = None
        img_la = None

        if (self.lidar or self.all) and data_token.get_flag('has_lidar_data'):
            lidar_data = data_token.get_processing_result('infusrUnit')
            pixel_x = lidar_data['pixel_x']
            pixel_y = lidar_data['pixel_y']
            colors = lidar_data['colors']
            img_lidar = image.copy()
            for i in range(len(pixel_x)):
                color = (int(colors[i][2]), int(colors[i][1]), int(colors[i][0]))
                cv2.circle(annotated_frame, (pixel_x[i], pixel_y[i]), radius=1, color=color, thickness=-1)
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

                if bbox_index < len(min_distances) and min_distances[bbox_index] is None or min_distance < min_distances[bbox_index]:
                    min_distances[bbox_index] = min_distance

        if (self.bb or self.all)and data_token.get_flag('has_bb_data'):
            bounding_boxes = data_token.get_processing_result('yoloUnit')
            img_bb = image.copy()
            for i, bbox in enumerate(bounding_boxes):
                x_min, y_min, x_max, y_max, score, class_id = bbox
                x_min, y_min, x_max, y_max = int(x_min), int(y_min), int(x_max), int(y_max)
                cv2.rectangle(annotated_frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                cv2.rectangle(img_bb, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

                if min_distances is not None and i < len(min_distances) and min_distances[i] is not None:
                    text = f"{bbox[-1]}  Dist: {min_distances[i]:.2f}m"
                    cv2.putText(annotated_frame, text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0),
                                2)
                    cv2.putText(img_bb, text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                else:
                    text = f"{bbox[-1]}"
                    cv2.putText(annotated_frame, text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0),
                                2)
                    cv2.putText(img_bb, text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    
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
            img_la = image.copy()
            annotated_frame = cv2.addWeighted(annotated_frame, 1 - alpha, colored_mask, alpha, 0)
            img_la = cv2.addWeighted(img_la, 1 - alpha, colored_mask, alpha, 0)
            # img_la = output['image']
            
        # if (self.la or self.all) and data_token.get_flag('has_lane_data'):
        #     output = data_token.get_processing_result('laneUnit')
        #     results = output['results']


        #     colored_mask = np.zeros_like(annotated_frame, dtype=np.uint8)

        #     for result in results[0]:

        #         class_name = result.boxes.cls

        #         if int(class_name) != 4 and int(class_name) != 3:
        #             mask = result.masks.data.cpu().numpy()
        #             mask = np.squeeze(mask)

        #             if mask.size > 0:
        #                 mask_resized = cv2.resize(mask, (annotated_frame.shape[1], annotated_frame.shape[0]), interpolation=cv2.INTER_NEAREST)

        #                 binary_mask = (mask_resized > 0.5).astype(np.uint8)

        #                 temp_colored_mask = np.zeros_like(annotated_frame, dtype=np.uint8)
        #                 temp_colored_mask[binary_mask == 1] = [255, 255, 255]

        #                 colored_mask = cv2.add(colored_mask, temp_colored_mask)

        #     alpha = 0.5
        #     img_la = image.copy()
        #     annotated_frame = cv2.addWeighted(annotated_frame, 1 - alpha, colored_mask, alpha, 0)
        #     img_la = cv2.addWeighted(img_la, 1 - alpha, colored_mask, alpha, 0)


        if (self.all and data_token.get_flag('hasObeserverData')):
            observer_results = data_token.get_processing_result('observerUnit')
            img_grid = image.copy()
            xMin = observer_results['xMin']
            xMax = observer_results['xMax']
            yMin = observer_results['yMin']
            yMax = observer_results['yMax']

        print(f"{self.id}: Outputting final result with shape: {annotated_frame.shape}, ")
        return annotated_frame, img_lidar, img_taggr, img_bb, img_la
