import numpy as np
import cv2
import open3d as o3d
from units import Unit
from dataToken import DataToken

class observerUnit(Unit):
    def __init__(self):
        super().__init__(id="observerUnit", input_type=DataToken, output_type=DataToken)

    def process(self, data_token=DataToken):
        # Get the image dimensions
        image = data_token.get_sensor_data('camera')
        if image is None:
            print("No camera data found in DataToken.")
            return data_token
        image_height, image_width, _ = image.shape

        # Get LiDAR data from infusrUnit
        lidar_data = data_token.get_processing_result('infusrUnit')
        if lidar_data is None:
            print("No processing results from infusrUnit found in DataToken.")
            return data_token

        valid_world_positions = lidar_data['valid_world_positions']
        pixel_x = lidar_data['pixel_x']
        pixel_y = lidar_data['pixel_y']

        # Ensure pixel_x and pixel_y are integers
        pixel_x = pixel_x.astype(np.int32)
        pixel_y = pixel_y.astype(np.int32)

        # Get lane data from laneUnit
        lane_data = data_token.get_processing_result('laneUnit')
        if lane_data is None:
            print("No processing results from laneUnit found in DataToken.")
            return data_token

        results = lane_data['results']  # Use results directly

        # Initialize an empty mask to match the image dimensions
        combined_lane_mask = np.zeros((image_height, image_width), dtype=np.uint8)

        # For each result in results[0], get the mask
        for result in results[0]:
            # Get the class label
            class_name = result.boxes.cls
            # Filter for lane classes (adjust class indices as needed)
            if int(class_name) == 0:  # Assuming class 0 corresponds to lanes
                # Get the mask from the result
                mask = result.masks.data.cpu().numpy()
                mask = np.squeeze(mask)
                if mask.size > 0:
                    # Resize the mask to match the image dimensions
                    mask_resized = cv2.resize(mask, (image_width, image_height), interpolation=cv2.INTER_NEAREST)
                    # Convert to binary mask
                    binary_mask = (mask_resized > 0.5).astype(np.uint8)
                    # Combine masks using logical OR
                    combined_lane_mask = np.logical_or(combined_lane_mask, binary_mask)

        # Ensure that pixel_x and pixel_y are within the image dimensions
        valid_indices = (pixel_x >= 0) & (pixel_x < image_width) & (pixel_y >= 0) & (pixel_y < image_height)
        pixel_x = pixel_x[valid_indices]
        pixel_y = pixel_y[valid_indices]
        valid_world_positions = valid_world_positions[valid_indices]

        # Check which LiDAR points fall within the lane masks
        mask_values = combined_lane_mask[pixel_y, pixel_x]  # Note: [row, col] indexing
        points_in_lane_mask = mask_values > 0

        # Filter the LiDAR points
        filtered_world_positions = valid_world_positions[points_in_lane_mask]

        # Display the filtered LiDAR points with Open3D
        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(filtered_world_positions)

        # Optionally, set colors for visualization
        colors = np.array([[1, 0, 0]] * len(filtered_world_positions))  # Red color
        point_cloud.colors = o3d.utility.Vector3dVector(colors)

        # Create an Open3D visualizer in blocking state
        vis = o3d.visualization.Visualizer()
        vis.create_window()
        vis.add_geometry(point_cloud)
        vis.run()  # Blocks until the window is closed
        vis.destroy_window()

        # Store the filtered points in data_token if needed
        data_token.add_processing_result(self.id, {'filtered_world_positions': filtered_world_positions})
        data_token.set_flag('hasObserverData', True)

        if self.next_unit:
            return self.next_unit.process(data_token)
        return data_token
