import numpy as np

class DataToken:
    def __init__(self, sensors):
        self.sensors = sensors
        self.sensor_data = {}  # Dictionary to hold sensor data
        self.processing_results = {}  # Dictionary to hold processing results
        self.flags = {'has_lidar_data':False, 'has_tagger_data': False}  # Dictionary to hold flags

    def add_sensor_data(self, sensor_name, data):
        if sensor_name not in self.sensors:
            raise ValueError(f"Sensor {sensor_name} is not registered in the pipeline.")
        
        self.sensor_data[sensor_name] = data
        # self.flags[f'has_{sensor_name}_data'] = True  # Set flag when data is added

    def get_sensor_data(self, sensor_name):
        return self.sensor_data.get(sensor_name)

    def add_processing_result(self, unit_id, result):
        self.processing_results[unit_id] = result

    def get_processing_result(self, unit_id):
        return self.processing_results.get(unit_id)

    def set_flag(self, flag_name, value=True):
        self.flags[flag_name] = value

    def get_flag(self, flag_name):
        return self.flags[f'{flag_name}']

    def cleanup(self):
        self.sensor_data.clear()
        self.processing_results.clear()
        self.flags.clear()
