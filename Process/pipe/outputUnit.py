from units import Unit
import numpy as np
class outputUnit(Unit):
    def __init__(self):
        super().__init__(id="outputUnit", input_type=np.ndarray, output_type=np.ndarray)

    def process(self, data):
        print(f"{self.id}: Outputting final result: {data.shape}")
        return data