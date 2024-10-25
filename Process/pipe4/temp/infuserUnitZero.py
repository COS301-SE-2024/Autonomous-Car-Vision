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

        data_token.add_processing_result(self.id, results)

        data_token.set_flag('has_lidar_data', True)
        if self.next_unit:
            return self.next_unit.process(data_token)
        return data_token

    def integrate_lidar_with_image(self, image, lidar_data):
        image_height, image_width, _ = image.shape

        x = lidar_data[:, 0]
        y = lidar_data[:, 1]
        z = lidar_data[:, 2]

        r = np.sqrt(x**2 + y**2 + z**2)
        theta = np.arctan2(y, x)
        phi = np.arcsin(z / r)

        horizontal_fov = np.radians(90 / 2)
        vertical_fov = np.radians(60 / 2)

        fov_mask = (np.abs(theta) <= horizontal_fov) & (np.abs(phi) <= vertical_fov)
        filtered_data = lidar_data[fov_mask]
        filtered_r = r[fov_mask]

        if filtered_r.size == 0:
            return image, []

        x_filtered = filtered_data[:, 0]
        y_filtered = filtered_data[:, 1]
        z_filtered = filtered_data[:, 2]

        indices_in_fov = np.where(fov_mask)[0]
        world_positions = filtered_data

        focal_length = image_width / (2 * np.tan(horizontal_fov))
        principal_point = np.array([image_width / 2, image_height / 2])

        angle_y = np.radians(-10)
        R = np.array([
            [np.cos(angle_y), 0, np.sin(angle_y)],
            [0, 1, 0],
            [-np.sin(angle_y), 0, np.cos(angle_y)]
        ])

        t = np.array([0.0, 0.0, 0.2])

        points_lidar = np.vstack((x_filtered, y_filtered, z_filtered))
        points_camera = R @ points_lidar + t[:, np.newaxis]

        pixel_x = (focal_length * points_camera[1, :] / points_camera[0, :]) + principal_point[0]
        pixel_y = (focal_length * (-points_camera[2, :] / points_camera[0, :])) + principal_point[1]

        valid_pixels_mask = (pixel_x >= 0) & (pixel_x < image_width) & (pixel_y >= 0) & (pixel_y < image_height)
        pixel_x = pixel_x[valid_pixels_mask].astype(int)
        pixel_y = pixel_y[valid_pixels_mask].astype(int)
        filtered_r = filtered_r[valid_pixels_mask]

        valid_indices = indices_in_fov[valid_pixels_mask]
        valid_world_positions = world_positions[valid_pixels_mask]

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
