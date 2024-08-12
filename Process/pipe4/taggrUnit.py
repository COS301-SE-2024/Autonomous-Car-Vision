from units import Unit
import numpy as np
import matplotlib.pyplot as plt
from dataToken import DataToken
from sklearn.decomposition import PCA


class taggrUnit(Unit):
    def __init__(self):
        super().__init__(id="taggrUnit", input_type=DataToken, output_type=DataToken)

    def process(self, data_token):
        image = data_token.get_sensor_data('camera')
        lidar_data = data_token.get_sensor_data('lidar')

        if not data_token.get_processing_result('infusrUnit') or not data_token.get_processing_result('yoloUnit'):
            if self.next_unit:
                return self.next_unit.process(data_token)
            return data_token
        infusrUnitData = data_token.get_processing_result('infusrUnit')
        bounding_boxes = data_token.get_processing_result('yoloUnit')
        pixel_x = infusrUnitData['pixel_x']
        pixel_y = infusrUnitData['pixel_y']
        filtered_r = infusrUnitData['filtered_r']
        valid_world_positions = infusrUnitData['valid_world_positions']
        world_data = []
        for bbox in bounding_boxes:
            label = bbox[-1]
            x_min, y_min, x_max, y_max, score, class_id = bbox
            x_min, y_min, x_max, y_max = int(x_min), int(y_min), int(x_max), int(y_max)
            inside_bbox_mask = (pixel_x >= x_min) & (pixel_x <= x_max) & (pixel_y >= y_min) & (pixel_y <= y_max)
            if np.any(inside_bbox_mask):
                # Get the minimum distance within the bounding box
                min_distance_idx = np.argmin(filtered_r[inside_bbox_mask])
                min_distance = filtered_r[inside_bbox_mask][min_distance_idx]

                world_position = valid_world_positions[inside_bbox_mask][min_distance_idx]

                # Start building the region of connected points
                region_points = [world_position]

                # Create a local mask for points inside the bounding box
                local_world_positions = valid_world_positions[inside_bbox_mask]
                local_region_mask = np.zeros(local_world_positions.shape[0], dtype=bool)
                local_region_mask[min_distance_idx] = True

                distance_limit = min_distance / 10

                while True:
                    current_region_size = len(region_points)
                    for i, wp in enumerate(local_world_positions):
                        if not local_region_mask[i]:  # Only consider points not already in the region
                            if np.any(np.linalg.norm(np.array(region_points) - wp, axis=1) < distance_limit):
                                region_points.append(wp)
                                local_region_mask[i] = True
                    # Break if no new points are added
                    if len(region_points) == current_region_size:
                        break

                # Get the pixel coordinates for the region points
                region_pixel_x = pixel_x[inside_bbox_mask][local_region_mask]
                region_pixel_y = pixel_y[inside_bbox_mask][local_region_mask]

                # Only apply PCA if there are at least 2 points
                if len(local_world_positions[local_region_mask]) >= 2:
                    # Apply PCA to the region points to determine the orientation
                    pca = PCA(n_components=2)
                    pca.fit(local_world_positions[local_region_mask])
                    orientation_vector = pca.components_[0]  # First principal component (dominant direction)

                    # Calculate the angle of the orientation vector relative to the x-axis in radians
                    orientation_angle = np.arctan2(orientation_vector[1], orientation_vector[0])

                    # Display the orientation and distance inside the bounding box
                    # Save the world position with label, distance, and orientation in the list
                    world_data.append({
                        "label": f"{label}",  # Change "object" to actual detected object class from YOLO if available
                        "world_position": {
                            "x": float(world_position[0]),
                            "y": float(world_position[1]),
                            "z": float(world_position[2])
                        },
                        "distance": float(min_distance),
                        "orientation": {
                            "angle_degrees": float(np.degrees(orientation_angle)),
                            "vector": {
                                "x": float(orientation_vector[0]),
                                "y": float(orientation_vector[1])
                            }
                        }
                    })
                else:
                    world_data.append({
                        "label": f"{label}",  # Change "object" to actual detected object class from YOLO if available
                        "world_position": {
                            "x": float(world_position[0]),
                            "y": float(world_position[1]),
                            "z": float(world_position[2])
                        },
                        "distance": float(min_distance),
                        "orientation": {
                            "angle_degrees": float(np.degrees(0)),
                            "vector": {
                                "x": float(0),
                                "y": float(0)
                            }
                        }
                    })
                data_token.add_processing_result('taggrUnit',
                                                 {'region_pixel_x': region_pixel_x, 'region_pixel_y': region_pixel_y,
                                                  'world_data': world_data, 'min_distance': min_distance})
                data_token.set_flag('has_tagger_data')
            # Pass the data_token to the next unit in the pipeline if it exists
            if self.next_unit:
                return self.next_unit.process(data_token)
            return data_token
