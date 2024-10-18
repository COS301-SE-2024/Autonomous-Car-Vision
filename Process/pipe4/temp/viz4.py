import open3d as o3d
import open3d.visualization.gui as gui
import open3d.visualization.rendering as rendering
import numpy as np
import matplotlib.cm as cm
import os
import sys

def apply_jet_colormap(pcd):
    points = np.asarray(pcd.points)
    z_values = points[:, 2]

    z_min = np.min(z_values)
    z_max = np.max(z_values)
    z_norm = (z_values - z_min) / (z_max - z_min)

    colormap = cm.get_cmap('jet')
    colors = colormap(z_norm)[:, :3]

    pcd.colors = o3d.utility.Vector3dVector(colors)

def visualize_point_cloud(filepath):
    pcd = o3d.io.read_point_cloud(filepath)

    apply_jet_colormap(pcd)

    points = np.asarray(pcd.points)
    points[:, 2] = -points[:, 2]
    pcd.points = o3d.utility.Vector3dVector(points)

    app = gui.Application.instance
    app.initialize()

    window = gui.Application.instance.create_window("Point Cloud Visualization with Jet Colormap", 1024, 768)

    scene_widget = gui.SceneWidget()
    scene_widget.scene = rendering.Open3DScene(window.renderer)

    material = rendering.MaterialRecord()
    material.point_size = 1.0
    scene_widget.scene.add_geometry("point_cloud", pcd, material)

    scene_widget.set_view_controls(gui.SceneWidget.FLY)

    bbox = pcd.get_axis_aligned_bounding_box()
    scene_widget.setup_camera(60, bbox, bbox.get_center() + np.array([0, 0, 10]))

    window.add_child(scene_widget)

    app.run()

if __name__ == "__main__":
    point_cloud_file = os.path.join(os.getcwd(), "combined_map.ply")

    if not os.path.exists(point_cloud_file):
        print(f"Error: 'combined_map.ply' not found in the current directory.")
        sys.exit(1)

    visualize_point_cloud(point_cloud_file)