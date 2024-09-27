from units import Unit
from dataToken import DataToken
import json
import os
from datetime import datetime

# Parallel streams allows lidar normalization to happen dually with the
class streamUnit(Unit):
    def __init__(self, ):
        super().__init__(id="streamUnit", input_type=DataToken, output_type=DataToken)
        if model_name:
            self.model_name = model_name
            self.model_path = f'{model_name}.pt'
            self.model = YOLO(self.model_path).to(self.device)
        else:
            raise ValueError("Model name must be provided")

        self.use_tensorrt = use_tensorrt
        self.trt_engine = None
        self.context = None

    def process(self, data_token):
        # Ensure camera data is available
        if data_token.get_sensor_data('camera') is None:
            raise ValueError("Yolo unit requires camera input. Please confirm the input stream.")

        # Get the camera frame
        frame = data_token.get_sensor_data('camera')

        # Run the YOLO model to get results
        results = self.model(frame)
        append_to_drive_log(results)

        # Extract and store only the bounding boxes
        bounding_boxes = results[0].boxes.data.tolist()
        for box in bounding_boxes:
            class_id = int(box[-1])  # Assuming class ID is the last element in each box
            class_label = self.model.names[class_id]
            box[-1] = class_label  # Replace class ID with the class label
        # Now save the bounding boxes with class labels
        data_token.add_processing_result(self.id, bounding_boxes)

        # Continue processing with the next unit, if available
        if self.next_unit:
            return self.next_unit.process(data_token)
        return data_token
