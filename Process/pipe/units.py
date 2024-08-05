import json
import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import cv2
class Unit:
    def __init__(self, id="0", input_type=float, output_type=float, dimW=200, dimH=100, inputs=1, outputs=1,
                 useDefaults=False, bgColor="theme dependent",
                 borderColor="theme dependent", textColor="theme dependent", selectionColor="theme dependent", label="",
                 editable=True, dynamic=False):
        self.id = id
        self.input_type = input_type
        self.output_type = output_type
        self.dimW = dimW
        self.dimH = dimH
        self.inputs = inputs
        self.outputs = outputs
        self.useDefaults = useDefaults
        self.bgColor = bgColor
        self.borderColor = borderColor
        self.textColor = textColor
        self.selectionColor = selectionColor
        self.label = label
        self.editable = editable
        self.dynamic = dynamic
        self.next_unit = None

    def process(self, data):
        raise NotImplementedError("Each unit must implement the process method")

    def set_next(self, next_unit):
        if self.output_type != next_unit.input_type:
            raise TypeError(f"Type mismatch: {self.output_type} cannot be linked to {next_unit.input_type}")
        self.next_unit = next_unit

    def printProps(self):
        properties = {
            "dimensions": {"width": self.dimW, "height": self.dimH},
            "id": self.id,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "useDefaults": self.useDefaults,
            "bgColor": self.bgColor,
            "borderColor": self.borderColor,
            "textColor": self.textColor,
            "selectionColor": self.selectionColor,
            "label": self.label,
            "editable": self.editable,
            "dynamic": self.dynamic
        }
        return json.dumps(properties, indent=4)


class InputUnit(Unit):
    def __init__(self):
        super().__init__(id="InputUnit", input_type=np.ndarray, output_type=np.ndarray)

    def process(self, iToken):
        if self.next_unit:
            return self.next_unit.process(iToken)
        return iToken


class OutputUnit(Unit):
    def __init__(self):
        super().__init__(id="OutputUnit", input_type=np.ndarray, output_type=np.ndarray)

    def process(self, data):
        print(f"{self.id}: Outputting final result: {data.shape}")
        return data


def extractNodes():
    nodes = {}
    for subclass in Unit.__subclasses__():
        instance = subclass()
        nodes[subclass.__name__] = json.loads(instance.printProps())
    return json.dumps(nodes, indent=4)


print(extractNodes())
