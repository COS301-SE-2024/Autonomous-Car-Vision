class Unit:
    def __init__(self, name, input_type, output_type):
        self.name = name
        self.input_type = input_type
        self.output_type = output_type
        self.next_unit = None

    def process(self, data):
        raise NotImplementedError("Each unit must implement the process method")

    def set_next(self, next_unit):
        if self.output_type != next_unit.input_type:
            raise TypeError(f"Type mismatch: {self.output_type} cannot be linked to {next_unit.input_type}")
        self.next_unit = next_unit

class MultiplyUnit(Unit):
    def __init__(self, name, factor):
        super().__init__(name, input_type=float, output_type=float)
        self.factor = factor

    def process(self, data):
        result = data * self.factor
        print(f"{self.name}: Multiplying {data} by {self.factor} to get {result}")
        if self.next_unit:
            return self.next_unit.process(result)
        return result

class DivideUnit(Unit):
    def __init__(self, name, divisor):
        super().__init__(name, input_type=float, output_type=float)
        self.divisor = divisor

    def process(self, data):
        result = data / self.divisor
        print(f"{self.name}: Dividing {data} by {self.divisor} to get {result}")
        if self.next_unit:
            return self.next_unit.process(result)
        return result

class AddUnit(Unit):
    def __init__(self, name, addend):
        super().__init__(name, input_type=float, output_type=float)
        self.addend = addend

    def process(self, data):
        result = data + self.addend
        print(f"{self.name}: Adding {self.addend} to {data} to get {result}")
        if self.next_unit:
            return self.next_unit.process(result)
        return result

class SubtractUnit(Unit):
    def __init__(self, name, subtrahend):
        super().__init__(name, input_type=float, output_type=float)
        self.subtrahend = subtrahend

    def process(self, data):
        result = data - self.subtrahend
        print(f"{self.name}: Subtracting {self.subtrahend} from {data} to get {result}")
        if self.next_unit:
            return self.next_unit.process(result)
        return result

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

multiply_unit = MultiplyUnit(name="MultiplyUnit", factor=2)
divide_unit = DivideUnit(name="DivideUnit", divisor=4)
add_unit = AddUnit(name="AddUnit", addend=10)
subtract_unit = SubtractUnit(name="SubtractUnit", subtrahend=5)

pipeline = Pipe()

pipeline.add_unit(multiply_unit)
pipeline.add_unit(divide_unit)
pipeline.add_unit(add_unit)
pipeline.add_unit(subtract_unit)


input_data = 20.0
output_data = pipeline.process(input_data)
print(f"Final Output: {output_data}")
