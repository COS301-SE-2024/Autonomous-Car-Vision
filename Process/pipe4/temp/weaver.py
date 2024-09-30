import os
import sys
import numpy as np
import json
import open3d as o3d

def load_lidar_data(file_path):
    try:
        data = np.load(file_path)
        return data
    except Exception as e:
        print(f"Error loading LiDAR data from {file_path}: {e}")
        return None

def load_sensor_position(json_path):
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading sensor position from {json_path}: {e}")
        return None

def transform_point_cloud(points, position, orientation):
    try:
        # Extract rotation angles (in radians)
        roll, pitch, yaw = np.radians([orientation['roll'], orientation['pitch'], orientation['yaw']])

        # Rotation matrices
        Rx = np.array([
            [1, 0, 0],
            [0, np.cos(roll), -np.sin(roll)],
            [0, np.sin(roll), np.cos(roll)]
        ])

        Ry = np.array([
            [np.cos(pitch), 0, np.sin(pitch)],
            [0, 1, 0],
            [-np.sin(pitch), 0, np.cos(pitch)]
        ])

        Rz = np.array([
            [np.cos(yaw), -np.sin(yaw), 0],
            [np.sin(yaw), np.cos(yaw), 0],
            [0, 0, 1]
        ])

        # Combined rotation matrix
        R = Rz @ Ry @ Rx

        # Separate the point coordinates (x, y, z) from the intensity
        xyz_points = points[:, :3]

        # Apply rotation and translation to the 3D coordinates
        transformed_points = (R @ xyz_points.T).T + np.array([position['x'], position['y'], position['z']])

        # Re-attach the intensity values (if needed)
        transformed_points_with_intensity = np.hstack((transformed_points, points[:, 3:4]))

        return transformed_points_with_intensity
    except Exception as e:
        print(f"Error transforming point cloud: {e}")
        return None

def weave_point_clouds(output_dir):
    point_clouds = []

    try:
        for file in sorted(os.listdir(output_dir)):
            if file.endswith('_lidar.npy'):
                print(f"Processing file: {file}")
                frame_number = file.split('_')[1]
                lidar_path = os.path.join(output_dir, file)
                json_path = os.path.join(output_dir, f"frame_{frame_number}_weaver.json")

                # Load point cloud and sensor data
                points = load_lidar_data(lidar_path)
                if points is None:
                    continue

                sensor_data = load_sensor_position(json_path)
                if sensor_data is None:
                    continue

                # Transform the point cloud to the global coordinate system
                transformed_points = transform_point_cloud(points, sensor_data['position'], sensor_data['orientation'])
                if transformed_points is None:
                    continue

                # Append to the list of all point clouds
                point_clouds.append(transformed_points)

        # Check if point_clouds is empty
        if not point_clouds:
            print("No point clouds found. Please check the input files.")
            return

        # Combine all point clouds into a single array
        combined_points = np.vstack(point_clouds)

        # Flip the scene along the Z-axis
        combined_points[:, 2] = -combined_points[:, 2]

        # Only use the first three columns (x, y, z) for saving
        combined_xyz = combined_points[:, :3]

        # Create Open3D point cloud object
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(combined_xyz)

        # Save the combined point cloud
        output_file = os.path.join(output_dir, 'combined_map.ply')
        o3d.io.write_point_cloud(output_file, pcd)
        print(f"Combined point cloud saved to {output_file}")

    except Exception as e:
        print(f"Error in weave_point_clouds: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the output directory as an argument.")
        sys.exit(1)

    output_dir = sys.argv[1]
    weave_point_clouds(output_dir)
