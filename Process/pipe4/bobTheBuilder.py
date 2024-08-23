import pipe
import importlib
import numpy as np
from PIL import Image
import os


def parse_token(token):
    parts = token.split('.')
    unit_type = parts[0]
    init_args = parts[1:]
    return unit_type, init_args


def get_unit_class(unit_type):
    try:
        module = importlib.import_module(unit_type)
        unit_class = getattr(module, unit_type)
        return unit_class
    except (ImportError, AttributeError) as e:
        raise ValueError(f"Unknown unit type: {unit_type}")


def create_unit(unit_type, init_args):
    unit_class = get_unit_class(unit_type)
    print(unit_type)
    if init_args and not unit_type == "outputUnit":
        unit = unit_class(*init_args)
    else:
        unit = unit_class()

    if unit_type == "outputUnit" and init_args:
        unit.set_flags(init_args)

    return unit


def build_pipeline(input_string):
    tokens = input_string.split(',')
    pipeline = pipe.Pipe({'camera', 'lidar'})

    for token in tokens:
        unit_type, init_args = parse_token(token)
        unit = create_unit(unit_type, init_args)
        pipeline.add_unit(unit)

    return pipeline


def load_image(file_path):
    image = Image.open(file_path)
    return np.array(image)


def load_lidar_data(file_path):
    # Load the LiDAR data from a .npy file
    lidar_data = np.load(file_path)
    return lidar_data


def test_pipeline():
    test_data_folder = 'testData'

    camera_file_path = os.path.join(test_data_folder, 'frame_000191_raw.png')
    lidar_file_path = os.path.join(test_data_folder, 'frame_000191_raw_lidar.npy')
    camera_data = load_image(camera_file_path)
    lidar_data = load_lidar_data(lidar_file_path)

    input_string = 'inputUnit,yoloUnit.yolov8n,infusrUnit,taggrUnit,outputUnit.'
    pipeline = build_pipeline(input_string)

    sensors = ['camera', 'lidar']
    data_token = pipe.DataToken(sensors)
    data_token.add_sensor_data('camera', camera_data)
    data_token.add_sensor_data('lidar', lidar_data)

    processed_image = pipeline.process(data_token)

    bounding_boxes = data_token.get_processing_result('yoloUnit')

    processed_image_path = os.path.join(test_data_folder, 'processed_image.png')
    Image.fromarray(processed_image).save(processed_image_path)

    return processed_image, bounding_boxes


processed_image, bounding_boxes = test_pipeline()
