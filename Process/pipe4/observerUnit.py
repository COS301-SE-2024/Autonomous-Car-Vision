import numpy as np
from units import Unit
from dataToken import DataToken


class observerUnit(Unit):
    def __init__(self):
        super().__init__(id="observerUnit", input_type=DataToken, output_type=DataToken)

    def process(self, data_token=DataToken):
        result = data_token.get_processing_result('infusrUnit')
        if result is None:
            print("No processing results from infusrUnit found in DataToken.")
        valid_world_pos = result['valid_world_positions']
        x = valid_world_pos[:, 0]
        y = valid_world_pos[:, 1]
        z = valid_world_pos[:, 2]
        xMax = x.max()
        xMin = x.min()
        yMax = y.max()
        yMin = y.min()
        results = {
            'xMax': xMax,
            'xMin': xMin,
            'yMax': yMax,
            'yMin': yMin,
        }
        data_token.add_processing_result(self.id, results)
        data_token.set_flag('hasObserverData', True)

        if self.next_unit:
            return self.next_unit.process(data_token)
        return data_token
