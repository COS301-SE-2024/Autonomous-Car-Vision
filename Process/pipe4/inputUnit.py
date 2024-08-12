from units import Unit
from dataToken import DataToken

class inputUnit(Unit):
    def __init__(self):
        super().__init__(id="inputUnit", input_type=DataToken, output_type=DataToken)

    def process(self, iToken):
        # You can add processing logic here if needed
        if self.next_unit:
            return self.next_unit.process(iToken)
        return iToken
