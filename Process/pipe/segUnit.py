import torch
import cv2
import os
import numpy as np
from ultralytics import YOLO
from units import Unit

class SegUnit(Unit):
    def __init__(self, model_path='yolov8n-seg.pt'):
        super().__init__(id="SegUnit", input_type=np.ndarray, output_type=np.ndarray)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Using device: {self.device}")
        self.model = YOLO(model_path).to(self.device)

    def process(self, frame):
        results = self.model(frame)
        if hasattr(results[0], 'masks'):
            # Handle segmentation/masking
            annotated_frame = results[0].plot()
        else:
            # Handle normal object detection
            annotated_frame = results[0].plot()

        if self.next_unit:
            return self.next_unit.process(annotated_frame)
        return annotated_frame