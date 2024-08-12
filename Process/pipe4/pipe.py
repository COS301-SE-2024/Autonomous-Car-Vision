from dataToken import DataToken
class Pipe:
    def __init__(self, sensors):
        self.entry_point = None
        self.exit_point = None
        self.sensors = None
        self.dataToken = DataToken(sensors)

    def set_entry_point(self, unit):
        self.entry_point = unit
        self.exit_point = unit

    def add_unit(self, unit):
        if self.entry_point is None:
            self.set_entry_point(unit)
        else:
            self.exit_point.set_next(unit)
            self.exit_point = unit

    def process(self, data):
        if self.entry_point is None:
            raise ValueError("Pipeline has no units")
        if not isinstance(data, self.entry_point.input_type):
            raise TypeError(f"Input data type {type(data)} does not match expected type {self.entry_point.input_type}")
        return self.entry_point.process(data)
