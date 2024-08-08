# bobthebuilder.py

import pipe
import units
import importlib
import numpy as np

def parse_token(token):
    parts = token.split('.')
    unit_type = parts[0]
    init_args = parts[1:]
    return unit_type, init_args

def get_unit_class(unit_type):
    try:
        module = importlib.import_module('units')
        unit_class = getattr(module, unit_type)
        return unit_class
    except (ImportError, AttributeError) as e:
        raise ValueError(f"Unknown unit type: {unit_type}")

def create_unit(unit_type, init_args):
    unit_class = get_unit_class(unit_type)
    init_kwargs = {arg.split('=')[0]: arg.split('=')[1] for arg in init_args}
    unit = unit_class(**init_kwargs)
    return unit

def build_pipeline(input_string):
    tokens = input_string.split(',')
    pipeline = pipe.Pipe()

    for token in tokens:
        unit_type, init_args = parse_token(token)
        unit = create_unit(unit_type, init_args)
        pipeline.add_unit(unit)

    return pipeline

# if __name__ == "__main__":
#     input_string = "InputUnit,yolov8n.rt.int8,OutputUnit"
#     pipeline = build_pipeline(input_string)
#     data = np.zeros((100, 100))  # Example input data
#     result = pipeline.process(data)
#     print(result)
