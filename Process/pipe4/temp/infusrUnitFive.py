import threading
from units import Unit
import numpy as np
import matplotlib.pyplot as plt
from dataToken import DataToken

class infusrUnit(Unit):
    def __init__(self):
        super().__init__(id="infusrUnit", input_type=DataToken, output_type=DataToken)

    def process(self, data_token):
        image = data_token.get_sensor_data('camera')
        lidar_data = data_token.get_sensor_data('lidar')
        integrated_image, results = self.integrate_lidar_with_image(image, lidar_data)

        # Store the processed results back into the DataToken
        data_token.add_processing_result(self.id, results)

         # Set a flag to indicate that LiDAR data has been processed
        data_token.set_flag('has_lidar_data', True)

        # Pass the data_token to the next unit in the pipeline if it exists
        if self.next_unit:
            return self.next_unit.process(data_token)
        return data_token

    def integrate_lidar_with_image(self, image, lidar_data):
        # Get image dimensions
        image_height, image_width, _ = image.shape

        # Extract Cartesian coordinates from LiDAR data
        x = lidar_data[:, 0]
        y = lidar_data[:, 1]
        z = lidar_data[:, 2]
        
        angle_y = np.radians(-10)
        R = np.array([
            [np.cos(angle_y), 0, np.sin(angle_y),0],
            [0, 1, 0, 0],
            [-np.sin(angle_y), 0, np.cos(angle_y), 0],
            [0, 0, 0, 1]
        ])

        t = np.array([
            [1, 0, 0, -0.15],
            [0, 1, 0, 0],
            [0, 0, 1, 0.35],
            [0, 0, 0, 1]
        ])
        
        # Create empty array
        points_camera_rotate = np.empty((3, 0))
        
        for i in range(len(x)):
            # Cearate 4x1 matrix
            points_lidar_rotate = np.vstack([x[i], y[i], z[i], 1])
    
            # Apply transformations
            rotated_points = R @ t @ points_lidar_rotate

            # Stack the new points as a new column (axis=1)
            points_camera_rotate = np.hstack((points_camera_rotate, rotated_points[:3]))

        
        # Extract the rotated x, y, z coordinates
        x = points_camera_rotate[0, :]
        y = points_camera_rotate[1, :]
        z = points_camera_rotate[2, :]
        
        # Write x, y, z to lidar_data
        lidar_data[:, 0] = x
        lidar_data[:, 1] = y
        lidar_data[:, 2] = z

        # Compute r, θ (azimuth), and φ (elevation)
        r = np.sqrt(x**2 + y**2 + z**2)
        theta = np.arctan2(y, x)  # Azimuth (horizontal angle)
        phi = np.arcsin(z / r)    # Elevation (vertical angle)

        # Convert the FOV angles from degrees to radians
        horizontal_fov = np.radians(90 / 2)  # 90° horizontal FOV
        vertical_fov = np.radians((90 * (600 / 800)) / 2)    # 60° vertical FOV

        # Apply the initial FOV constraints to limit the LiDAR data to 90° horizontal and 60° vertical FOV
        fov_mask = (np.abs(theta) <= horizontal_fov) & (np.abs(phi) <= vertical_fov)
        filtered_data = lidar_data[fov_mask]
        filtered_r = r[fov_mask]

        # If no points are left after filtering, return the image unchanged
        if filtered_r.size == 0:
            return image, []

        # Store indices and 3D world positions
        indices_in_fov = np.where(fov_mask)[0]
        world_positions = filtered_data  # This keeps the x, y, z of points within FOV

        # Example intrinsic parameters (focal length and principal point)
        focal_length = image_width / (2 * np.tan(horizontal_fov))
        principal_point = np.array([image_width / 2, image_height / 2])

        # Perspective projection
        pixel_x = (focal_length * filtered_data[:, 1] / filtered_data[:, 0]) + principal_point[0]
        pixel_y = (focal_length * (-filtered_data[:, 2] / filtered_data[:, 0])) + principal_point[1]

        # Filter based on valid pixel coordinates within the image dimensions
        valid_pixels_mask = (pixel_x >= 0) & (pixel_x < image_width) & (pixel_y >= 0) & (pixel_y < image_height)
        pixel_x = pixel_x[valid_pixels_mask].astype(int)
        pixel_y = pixel_y[valid_pixels_mask].astype(int)
        filtered_r = filtered_r[valid_pixels_mask]  # Update filtered_r to correspond to valid pixels

        # Update indices and world positions based on valid pixels
        valid_indices = indices_in_fov[valid_pixels_mask]
        valid_world_positions = world_positions[valid_pixels_mask]

        # Normalize the distances (r) for color mapping
        norm = plt.Normalize(vmin=filtered_r.min(), vmax=filtered_r.max())
        cmap = plt.colormaps.get_cmap('plasma')  # Updated method for colormap
        colors = cmap(norm(filtered_r))[:, :3]  # Get RGB values from the colormap
        colors = (colors * 255).astype(int)

        return image, {
            'pixel_x': pixel_x,
            'pixel_y': pixel_y,
            'colors': colors,
            'valid_world_positions': valid_world_positions,
            'valid_indices': valid_indices,
            'filtered_r': filtered_r
        }