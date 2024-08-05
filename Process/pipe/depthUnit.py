import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import cv2
from units import Unit

class DepthEstimationUnit(Unit):
    def __init__(self):
        super().__init__(id="DepthEstimationUnit", input_type=np.ndarray, output_type=np.ndarray)
        self.model_type = "DPT_Large"
        self.midas = torch.hub.load("intel-isl/MiDaS", self.model_type)
        self.midas.eval()
        self.transform = torch.hub.load("intel-isl/MiDaS", "transforms").dpt_transform

    def process(self, data):
        img = Image.fromarray(cv2.cvtColor(data, cv2.COLOR_BGR2RGB))
        input_batch = self.transform(img).unsqueeze(0)

        with torch.no_grad():
            prediction = self.midas(input_batch)

        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=img.size[::-1],
            mode="bicubic",
            align_corners=False,
        ).squeeze()

        depth_map = prediction.cpu().numpy()

        if self.next_unit:
            return self.next_unit.process(depth_map)
        return depth_map

def estimate_distances(detections, depth_map):
    distances = []
    for detection in detections:
        x, y, w, h = detection['box']
        roi = depth_map[y:y+h, x:x+w]
        distance = np.mean(roi)
        distances.append({
            "class_id": detection['class_id'],
            "confidence": detection['confidence'],
            "box": detection['box'],
            "distance": distance
        })
    return distances
