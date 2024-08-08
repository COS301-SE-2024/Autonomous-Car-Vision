import pipe
import importlib

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
    if init_args:
        unit = unit_class(*init_args)
    else:
        unit = unit_class()
    return unit

def build_pipeline(input_string):
    tokens = input_string.split(',')
    pipeline = pipe.Pipe()

    for token in tokens:
        unit_type, init_args = parse_token(token)
        unit = create_unit(unit_type, init_args)
        pipeline.add_unit(unit)

    return pipeline

# Example usage

