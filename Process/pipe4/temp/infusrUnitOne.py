import threading
from units import Unit
import numpy as np
import matplotlib.pyplot as plt
from dataToken import DataToken
import cv2 

camera_parameters = {
    'x': 0.15, 'y': 0.00, 'z': 1.65, 'roll': 0, 'pitch': -10, 'yaw': 0,
    'width': 800, 'height': 600, 'fov': 90,
    'sensor_label': 'camera', 'sensor_type': 'camera'
}
lidar_parameters = {
    'x': 0, 'y': 0, 'z': 2.0, 'roll': 0, 'pitch': 0, 'yaw': 0,
    'channels': 64, 'range': 100.0, 'lower_fov': -30, 'upper_fov': 30,
    'points_per_second': 640000, 'rotation_frequency': 30,
    'sensor_label': 'lidar', 'sensor_type': 'lidar'
}

def calculate_extrinsic(camera_params, lidar_params):
    # Calculate translation vector (t) from LiDAR to camera
    t = np.array([
        camera_params['x'] - lidar_params['x'],
        camera_params['y'] - lidar_params['y'],
        camera_params['z'] - lidar_params['z']
    ])
    
    # Calculate rotation matrix (R) from LiDAR to camera
    roll = np.radians(camera_params['roll'])
    pitch = np.radians(camera_params['pitch'])
    yaw = np.radians(camera_params['yaw'])
    
    if roll != 0:
        Rx = np.array([
            [1, 0, 0],
            [0, np.cos(roll), -np.sin(roll)],
            [0, np.sin(roll), np.cos(roll)]
        ])
    else:
        Rx = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])
    
    if pitch != 0:
        Ry = np.array([
            [np.cos(pitch), 0, np.sin(pitch)],
            [0, 1, 0],
            [-np.sin(pitch), 0, np.cos(pitch)]
        ])
        print("Pitch:", pitch)
    else:
        Ry = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])
        
    if yaw != 0:
        Rz = np.array([
            [np.cos(yaw), -np.sin(yaw), 0],
            [np.sin(yaw), np.cos(yaw), 0],
            [0, 0, 1]
        ])
    else:
        Rz = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])
    
    # Combine rotations (assuming ZYX rotation order)
    R = Rz @ Ry @ Rx
    
    return Ry, t


class infusrUnit(Unit):
    def __init__(self):
        super().__init__(id="infusrUnit", input_type=DataToken, output_type=DataToken)

    def process(self, data_token):
        # # Concurrently process LiDAR data and run AI inference
        # def lidar_task():
        #     # Perform LiDAR processing and normalization
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

        # Apply rotation to LiDAR points to account for camera tilt
        angle_y = np.radians(-10)  # Camera is tilted 10 degrees downwards
        cos_angle_y = np.cos(angle_y)
        sin_angle_y = np.sin(angle_y)

        # Rotation matrix for 10 degrees around the Y-axis
        R_tilt = np.array([
            [cos_angle_y, 0, sin_angle_y],
            [0, 1, 0],
            [-sin_angle_y, 0, cos_angle_y]
        ])

        # Apply the rotation matrix to the LiDAR points
        points_lidar = np.vstack((x, y, z))  # 3xN matrix of LiDAR points
        points_rotated = R_tilt @ points_lidar

        # Extract rotated coordinates
        x_rotated = points_rotated[0, :]
        y_rotated = points_rotated[1, :]
        z_rotated = points_rotated[2, :]

        # Compute spherical coordinates after rotation
        r_rotated = np.sqrt(x_rotated**2 + y_rotated**2 + z_rotated**2)
        theta_rotated = np.arctan2(y_rotated, x_rotated)  # Azimuth (horizontal angle)
        phi_rotated = np.arcsin(z_rotated / r_rotated)    # Elevation (vertical angle)

        # Convert the FOV angles from degrees to radians
        horizontal_fov = np.radians(90 / 2)  # 90° horizontal FOV
        vertical_fov = np.radians((90 * (600 / 800)) / 2)  # Adjusted for aspect ratio

        # Apply FOV constraints to limit the LiDAR data to the camera's FOV after rotation
        fov_mask = (np.abs(theta_rotated) <= horizontal_fov) & (np.abs(phi_rotated) <= vertical_fov)
        filtered_data = lidar_data[fov_mask]
        filtered_r = r_rotated[fov_mask]

        # If no points are left after filtering, return the image unchanged
        if filtered_r.size == 0:
            return image, []

        # Extract filtered x, y, z coordinates after rotation
        x_filtered = x_rotated[fov_mask]
        y_filtered = y_rotated[fov_mask]
        z_filtered = z_rotated[fov_mask]

        # Store indices and 3D world positions
        indices_in_fov = np.where(fov_mask)[0]
        world_positions = lidar_data[fov_mask]  # This keeps the original x, y, z of points within FOV

        # Example intrinsic parameters (focal length and principal point)
        focal_length = image_width / (2 * np.tan(horizontal_fov))
        principal_point = np.array([image_width / 2, image_height / 2])

        # Transform filtered LiDAR points from rotated LiDAR coordinates to image plane
        pixel_x = (focal_length * y_filtered / x_filtered) + principal_point[0]
        pixel_y = (focal_length * (-z_filtered / x_filtered)) + principal_point[1]

        # Filter based on valid pixel coordinates within the image dimensions
        valid_pixels_mask = (pixel_x >= 0) & (pixel_x < image_width) & (pixel_y >= 0) & (pixel_y < image_height)
        pixel_x = pixel_x[valid_pixels_mask].astype(int)
        pixel_y = pixel_y[valid_pixels_mask].astype(int)
        filtered_r = filtered_r[valid_pixels_mask]

        # Update indices and world positions based on valid pixels
        valid_indices = indices_in_fov[valid_pixels_mask]
        valid_world_positions = world_positions[valid_pixels_mask]

        # Normalize the distances (r) for color mapping
        norm = plt.Normalize(vmin=filtered_r.min(), vmax=filtered_r.max())
        cmap = plt.colormaps.get_cmap('plasma')
        colors = cmap(norm(filtered_r))[:, :3]  # Get RGB values from the colormap
        colors = (colors * 255).astype(int)
        
        # self.draw_distances_opencv(image, pixel_x, pixel_y, filtered_r)  # Draw distances on the image

        return image, {
            'pixel_x': pixel_x,
            'pixel_y': pixel_y,
            'colors': colors,
            'valid_world_positions': valid_world_positions,
            'valid_indices': valid_indices,
            'filtered_r': filtered_r
        }

    def draw_distances_opencv(self, image, pixel_x, pixel_y, distances):
        for x, y, distance in zip(pixel_x, pixel_y, distances):
            text = f'{distance:.1f}'
            cv2.putText(image, text, (x, y), cv2.CAP_PROP_FPS, 0.35, (255, 255, 255), 1, cv2.LINE_AA)
