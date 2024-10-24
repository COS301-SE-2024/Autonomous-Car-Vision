import numpy as np
import cv2
import open3d as o3d
from units import Unit
from dataToken import DataToken
import matplotlib.pyplot as plt


class observerUnit(Unit):
    def __init__(self):
        super().__init__(id="observerUnit", input_type=DataToken, output_type=DataToken)

    def plot_point_cloud(self, pre_filtered_points, post_filtered_points):
        pre_filtered_points_np = np.array(pre_filtered_points)
        post_filtered_points_np = np.array(post_filtered_points)

        pre_filtered_points_np[:, 1] = -pre_filtered_points_np[:, 1]
        post_filtered_points_np[:, 1] = -post_filtered_points_np[:, 1]

        combined_cloud = o3d.geometry.PointCloud()
        combined_cloud.points = o3d.utility.Vector3dVector(pre_filtered_points_np)

        pre_colors = np.ones_like(pre_filtered_points_np) * 0.5
        combined_cloud.colors = o3d.utility.Vector3dVector(pre_colors)

        for post_point in post_filtered_points_np:
            distances = np.linalg.norm(pre_filtered_points_np - post_point, axis=1)
            min_index = np.argmin(distances)

            if distances[min_index] < 1e-6:
                pre_colors[min_index] = [1.0, 0.0, 0.0]

        combined_cloud.colors = o3d.utility.Vector3dVector(pre_colors)

        o3d.visualization.draw_geometries([combined_cloud],
                                          window_name="LiDAR Point Cloud: Pre-Filtered (Grey) and Post-Filtered (Red)")

    def process(self, data_token=DataToken):
        image = data_token.get_sensor_data('camera')
        if image is None:
            print("No camera data found in DataToken.")
            return data_token
        image_height, image_width, _ = image.shape

        lidar_data = data_token.get_processing_result('infusrUnit')
        if lidar_data is None:
            print("No processing results from infusrUnit found in DataToken.")
            return data_token

        valid_world_positions = lidar_data['valid_world_positions']
        print("Valid World Pos")
        print(valid_world_positions)
        # pixel_x = lidar_data['pixel_x']
        # print("pixel x")
        # print(pixel_x)
        # pixel_y = lidar_data['pixel_y']
        # print("pixel y")
        # print(pixel_y)
        if valid_world_positions is not None:
            zmin, zmax = 1, 2.3
            ymin, ymax = -0.9, 0.9
            xmin, xmax = 3, 25.0

            filtered_positions = valid_world_positions[
                (valid_world_positions[:, 0] >= xmin) & (valid_world_positions[:, 0] <= xmax) &
                (valid_world_positions[:, 1] >= ymin) & (valid_world_positions[:, 1] <= ymax) &
                (valid_world_positions[:, 2] >= zmin) & (valid_world_positions[:, 2] <= zmax)
                ]
            average_x_filtered = 0
            print("filtered_positions", filtered_positions)
            if len(filtered_positions) > 0:
                average_x_filtered = np.mean(filtered_positions[:, 0])
                print(f"Average x-value of filtered points: {average_x_filtered}")
            else:
                print("No points within the filtered region.")
            if average_x_filtered == 0:
                breaking = 0
            else:
                breaking = (1 - (average_x_filtered / 22))
            breaking1 = 0 if breaking < 0.25 else 1
            handbreak = False
            if breaking > 0.5:
                handbreak = True

            print("dist", breaking)

            # Plot the filtered points
            print("Plotting filtered valid world positions within the cuboid...")
            # self.plot_point_cloud(valid_world_positions, filtered_positions)


        else:
            print("No valid world positions found.")

        # Store the filtered points in data_token if needed
        data_token.add_processing_result(self.id, {'observed_lidar': filtered_positions, 'breaking': breaking1,
                                                   'handBreak': handbreak})
        data_token.set_flag('hasObserverData', True)

        if self.next_unit:
            return self.next_unit.process(data_token)
        return data_token
