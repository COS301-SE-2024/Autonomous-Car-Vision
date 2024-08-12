import json
import numpy as np
import cv2
from PIL import Image


class Unit:
    def __init__(self, id="0", input_type=float, output_type=float):
        self.id = id
        self.input_type = input_type
        self.output_type = output_type
        self.next_unit = None

    def process(self, data):
        raise NotImplementedError("Each unit must implement the process method")

    def set_next(self, next_unit):
        if self.output_type != next_unit.input_type:
            raise TypeError(f"Type mismatch: {self.output_type} cannot be linked to {next_unit.input_type}")
        self.next_unit = next_unit
