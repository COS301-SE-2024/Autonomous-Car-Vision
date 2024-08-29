import numpy as np
import open3d as o3d
import os

test_data_folder = 'testData'

lidar_file_path = os.path.join(test_data_folder, 'frame_000300_raw_lidar.npy')

# Load the .npy file containing the LiDAR data
lidar_data = np.load(lidar_file_path)

lidar_data[:, 1] *= -1

# Create an Open3D point cloud object
point_cloud = o3d.geometry.PointCloud()

# Assign the numpy array of points to the point cloud
point_cloud.points = o3d.utility.Vector3dVector(lidar_data[:, :3])

# Visualize the point cloud
o3d.visualization.draw_geometries([point_cloud])