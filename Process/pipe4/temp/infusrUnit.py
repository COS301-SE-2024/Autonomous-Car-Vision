import threading
from units import Unit
import numpy as np
import matplotlib.pyplot as plt
from dataToken import DataToken

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

class infusrUnit(Unit):
    def __init__(self):
        super().__init__(id="infusrUnit", input_type=DataToken, output_type=DataToken)

    def process(self, data_token):
        image = data_token.get_sensor_data('camera')
        lidar_data = data_token.get_sensor_data('lidar')
        integrated_image, results = self.integrate_lidar_with_image(image, lidar_data)

        data_token.add_processing_result(self.id, results)

        data_token.set_flag('has_lidar_data', True)

        if self.next_unit:
            return self.next_unit.process(data_token)
        return data_token

    def integrate_lidar_with_image(self, image, lidar_data):
        image_height, image_width, _ = image.shape

        # Extract Cartesian coordinates from LiDAR data
        x = lidar_data[:, 0]
        y = lidar_data[:, 1]
        z = lidar_data[:, 2]
        
        x_offset = lidar_parameters['x'] - camera_parameters['x']
        y_offset = lidar_parameters['y'] - camera_parameters['y']
        z_offset = lidar_parameters['z'] - camera_parameters['z']
        
        roll_offset = lidar_parameters['roll'] + camera_parameters['roll']
        pitch_offset = lidar_parameters['pitch'] + camera_parameters['pitch']
        yaw_offset = lidar_parameters['yaw'] + camera_parameters['yaw']
        
        # Make a 4x4 0 matrix
        M = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        
        if roll_offset != 0:
            angle_x = np.radians(roll_offset)
            Rx = np.array([
                [1, 0, 0, 0],
                [0, np.cos(angle_x), -np.sin(angle_x), 0],
                [0, np.sin(angle_x), np.cos(angle_x), 0],
                [0, 0, 0, 1]
            ])
            
            M = M @ Rx
        
        if pitch_offset != 0:
            angle_y = np.radians(pitch_offset)
            Ry = np.array([
                [np.cos(angle_y), 0, np.sin(angle_y),0],
                [0, 1, 0, 0],
                [-np.sin(angle_y), 0, np.cos(angle_y), 0],
                [0, 0, 0, 1]
            ])
            
            M = M @ Ry
            
        if yaw_offset != 0:
            angle_z = np.radians(yaw_offset)
            Rz = np.array([
                [np.cos(angle_z), -np.sin(angle_z), 0, 0],
                [np.sin(angle_z), np.cos(angle_z), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ])
            
            M = M @ Rz

        t = np.array([
            [1, 0, 0, x_offset],
            [0, 1, 0, y_offset],
            [0, 0, 1, z_offset],
            [0, 0, 0, 1]
        ])
        
        # Create empty array
        points_camera_rotate = np.empty((3, 0))
        
        M = M @ t
        
        for i in range(len(x)):
            # Create 4x1 matrix
            points_lidar_rotate = np.vstack([x[i], y[i], z[i], 1])
    
            rotated_points = M @ points_lidar_rotate

            points_camera_rotate = np.hstack((points_camera_rotate, rotated_points[:3]))

        
        x = points_camera_rotate[0, :]
        y = points_camera_rotate[1, :]
        z = points_camera_rotate[2, :]
        
        modified_lidar_data = np.vstack((x, y, z)).T
        
        modified_lidar_data[:, 0] = x
        modified_lidar_data[:, 1] = y
        modified_lidar_data[:, 2] = z

        # Compute r, θ (azimuth), and φ (elevation)
        r = np.sqrt(x**2 + y**2 + z**2)
        theta = np.arctan2(y, x) 
        phi = np.arcsin(z / r)

        horizontal_fov = np.radians(90 / 2) 
        vertical_fov = np.radians((90 * (600 / 800)) / 2) 

        # Apply the initial FOV constraints to limit the LiDAR data to 90° horizontal and 60° vertical FOV
        fov_mask = (np.abs(theta) <= horizontal_fov) & (np.abs(phi) <= vertical_fov)
        filtered_data = modified_lidar_data[fov_mask]
        filtered_r = r[fov_mask]

        # If no points are left after filtering, return the image unchanged
        if filtered_r.size == 0:
            return image, []

        # Store indices and 3D world positions
        indices_in_fov = np.where(fov_mask)[0]
        world_positions = filtered_data

        focal_length = image_width / (2 * np.tan(horizontal_fov))
        principal_point = np.array([image_width / 2, image_height / 2])

        # Perspective projection
        pixel_x = (focal_length * filtered_data[:, 1] / filtered_data[:, 0]) + principal_point[0]
        pixel_y = (focal_length * (-filtered_data[:, 2] / filtered_data[:, 0])) + principal_point[1]

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
        colors = cmap(norm(filtered_r))[:, :3]
        colors = (colors * 255).astype(int)

        return image, {
            'pixel_x': pixel_x,
            'pixel_y': pixel_y,
            'colors': colors,
            'valid_world_positions': valid_world_positions,
            'valid_indices': valid_indices,
            'filtered_r': filtered_r
        }
