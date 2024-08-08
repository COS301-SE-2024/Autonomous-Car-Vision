import torch
import cv2
import numpy as np
import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit
from ultralytics import YOLO
from units import Unit
import os

class SegUnit(Unit):
    def __init__(self, model_name):
        super().__init__(id="SegUnit", input_type=np.ndarray, output_type=np.ndarray)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Using device: {self.device}")

        if model_name:
            self.model_name = model_name
            self.model_path = f'{model_name}.pt'
            self.model = YOLO(self.model_path).to(self.device)
        else:
            raise ValueError("Model name must be provided")

        self.trt_engine = None
        self.context = None

    def process(self, frame):
        # Ensure the frame is resized to (640, 640) and normalized
        frame = cv2.resize(frame, (640, 640))
        frame = frame / 255.0  # Normalize to [0, 1]
        frame = frame.transpose((2, 0, 1))  # Change from HWC to CHW
        frame = np.expand_dims(frame, axis=0)  # Add batch dimension
        frame = torch.from_numpy(frame).to(self.device).float()

        results = self.model(frame)
        annotated_frame = results[0].plot() if hasattr(results[0], 'masks') else results[0].plot()

        if self.next_unit:
            return self.next_unit.process(annotated_frame)
        return annotated_frame
