import units
class Pipe:
    def __init__(self):
        self.entry_point = None
        self.exit_point = None

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

# multiply_unit = units.MultiplyUnit(name="MultiplyUnit", factor=2)
# divide_unit = units.DivideUnit(name="DivideUnit", divisor=4)
# add_unit = units.AddUnit(name="AddUnit", addend=10)
# subtract_unit = units.SubtractUnit(name="SubtractUnit", subtrahend=5)
#
# pipeline = Pipe()
#
# pipeline.add_unit(multiply_unit)
# pipeline.add_unit(divide_unit)
# pipeline.add_unit(add_unit)
# pipeline.add_unit(subtract_unit)
#
#
# input_data = 20.0
# output_data = pipeline.process(input_data)
# print(f"Final Output: {output_data}")

# print(units.extractNodes())
