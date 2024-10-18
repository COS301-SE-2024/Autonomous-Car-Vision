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
    if init_args and not unit_type == "outputUnit" and not unit_type == "outputUnitTest":
        unit = unit_class(*init_args)
    else:
        unit = unit_class()

    if (unit_type == "outputUnit" or unit_type =="outputUnitTest") and init_args:
        unit.set_flags(init_args)

    return unit


def build_pipeline(input_string):
    tokens = input_string.split(',')
    pipeline = pipe.Pipe({'camera', 'lidar'})

    for token in tokens:
        if (token == ''): 
            continue
        unit_type, init_args = parse_token(token)
        unit = create_unit(unit_type, init_args)
        pipeline.add_unit(unit)

    return pipeline


def load_image(file_path):
    image = Image.open(file_path)
    return np.array(image)


def load_lidar_data(file_path):
    lidar_data = np.load(file_path)
    return lidar_data


def test_pipeline():
    test_data_folder = 'public/testData'

    camera_file_path = os.path.join(test_data_folder, 'image.png')
    lidar_file_path = os.path.join(test_data_folder, 'frame_000149_lidar.npy')
    camera_data = load_image(camera_file_path)
    lidar_data = load_lidar_data(lidar_file_path)

    input_string = 'inputUnit,yoloUnit.yolov8n,infusrUnit,taggrUnit,outputUnit.all'
    pipeline = build_pipeline(input_string)

    sensors = ['camera', 'lidar']
    data_token = pipe.DataToken(sensors)
    data_token.add_sensor_data('camera', camera_data)
    data_token.add_sensor_data('lidar', lidar_data)

    processed_image, img_lidar, img_taggr, img_bb, img_la = pipeline.process(data_token)

    bounding_boxes = data_token.get_processing_result('yoloUnit')

    processed_image_path = os.path.join(test_data_folder, 'processed_image.png')
    lidar_image_path = os.path.join(test_data_folder, 'lidar_image.png')
    taggr_image_path = os.path.join(test_data_folder, 'taggr_image.png')
    bb_image_path = os.path.join(test_data_folder, 'bb_image.png')
    lane_image_path = os.path.join('public/testData', 'lane_image.png')
    Image.fromarray(processed_image).save(processed_image_path)
    if img_lidar is not None: Image.fromarray(img_lidar).save(lidar_image_path)
    if img_taggr is not None: Image.fromarray(img_taggr).save(taggr_image_path)
    if img_bb is not None: Image.fromarray(img_bb).save(bb_image_path)
    if img_la is not None: Image.fromarray(img_la).save(lane_image_path)
    return processed_image, bounding_boxes

def test_lane():
    camera_file_path = os.path.join('public/testData/frame_000300_raw.png')
    camera_data = load_image(camera_file_path)
    
    input_string = 'inputUnit,infusrUnit,laneUnit,outputUnitTest.all'
    pipeline = build_pipeline(input_string)
    
    sensors = ['camera', 'lidar']
    data_token = pipe.DataToken(sensors)
    data_token.add_sensor_data('camera', camera_data)

    processed_image, img_lidar, img_taggr, img_bb, img_la = pipeline.process(data_token)
    lane_image_path = os.path.join('public/testData', 'lane_image.png')
    if img_la is not None: Image.fromarray(img_la).save(lane_image_path)
    output = data_token.get_processing_result('laneUnit')
    
    steer = output['steer']
    
    print("steer: ", steer)


processed_image, bounding_boxes = test_pipeline()
# test_lane()
