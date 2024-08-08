from units import Unit
import numpy as np


class inputUnit(Unit):
    def __init__(self):
        super().__init__(id="inputUnit", input_type=np.ndarray, output_type=np.ndarray)

    def process(self, iToken):
        if self.next_unit:
            return self.next_unit.process(iToken)
        return iToken

