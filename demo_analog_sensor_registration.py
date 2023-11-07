from sensor import Sensor
from registration import register_analog_function_to_sensor
from soil_moisture import sm

sensor = Sensor(sensor_name="demo_sensor_1")
register_analog_function_to_sensor(sensor=sensor, def_dict=sm)