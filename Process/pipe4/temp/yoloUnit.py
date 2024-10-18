import torch
from ultralytics import YOLO
from units import Unit
from dataToken import DataToken
import json
import os
from datetime import datetime

def append_to_drive_log(results, log_file='output_frames/driveLog.json'):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    log_entry = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'preprocess_time': results[0].speed['preprocess'],
        'inference_time': results[0].speed['inference'],
        'postprocess_time': results[0].speed['postprocess'],
        'total_time': results[0].speed['preprocess'] + results[0].speed['inference'] + results[0].speed['postprocess'],
        'fps': 1.0 / (results[0].speed['preprocess'] + results[0].speed['inference'] + results[0].speed['postprocess']),
    }
    if os.path.exists(log_file):
        with open(log_file, 'r') as file:
            log_data = json.load(file)
    else:
        log_data = []
    log_data.append(log_entry)

    with open(log_file, 'w') as file:
        json.dump(log_data, file, indent=4)

    print(f"Logged YOLOv8 results to {log_file}.")


class yoloUnit(Unit):
    def __init__(self, model_name, use_tensorrt=False):
        super().__init__(id="yoloUnit", input_type=DataToken, output_type=DataToken)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"torch.cuda.is_available() = {torch.cuda.is_available()}")
        print(f"Using device: {self.device}")
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
        if data_token.get_sensor_data('camera') is None:
            raise ValueError("Yolo unit requires camera input. Please confirm the input stream.")

        frame = data_token.get_sensor_data('camera')

        results = self.model(frame)
        append_to_drive_log(results)

        bounding_boxes = results[0].boxes.data.tolist()
        for box in bounding_boxes:
            class_id = int(box[-1])
            class_label = self.model.names[class_id]
            box[-1] = class_label 
        # Now save the bounding boxes with class labels
        data_token.add_processing_result(self.id, bounding_boxes)
        data_token.set_flag('has_bb_data',True)
        
        if self.next_unit:
            return self.next_unit.process(data_token)
        return data_token
