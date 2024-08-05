import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import cv2
from units import Unit

class DepthEstimationUnit(Unit):
    def __init__(self):
        super().__init__(id="DepthEstimationUnit", input_type=np.ndarray, output_type=np.ndarray)
        self.model_type = "DPT_Hybrid"  # Use the faster DPT_Hybrid model
        self.midas = torch.hub.load("intel-isl/MiDaS", self.model_type)
        self.midas.eval()

        # Check if a GPU is available and if so, use it
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.midas.to(self.device)

        self.transform = torch.hub.load("intel-isl/MiDaS", "transforms").dpt_transform

    def process(self, data):
        # Convert the input data to a PIL Image
        img = Image.fromarray(cv2.cvtColor(data, cv2.COLOR_BGR2RGB))

        # Convert PIL Image to NumPy array and normalize
        img_np = np.array(img) / 255.0

        # Apply the transformation
        input_batch = self.transform(img_np).unsqueeze(0).to(self.device)

        # Check and correct the shape of the input batch
        if input_batch.dim() == 5:
            input_batch = input_batch.squeeze(1)

        # Print the shape of the input batch
        print(f"Transformed input batch shape: {input_batch.shape}")

        # Check if the shape is correct
        if input_batch.dim() != 4:
            raise ValueError(f"Input batch has incorrect shape: {input_batch.shape}. Expected 4 dimensions.")

        # Perform depth estimation
        with torch.no_grad():
            prediction = self.midas(input_batch)

        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=img.size[::-1],
            mode="bicubic",
            align_corners=False,
        ).squeeze()

        depth_map = prediction.cpu().numpy()

        # Normalize the depth map for visualization
        depth_map = (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min())
        depth_map = (depth_map * 255).astype(np.uint8)

        # Process the depth map with the next unit if available
        if self.next_unit:
            return self.next_unit.process(depth_map)
        return depth_map
