from sensor import Sensor
from lib.registration import register_analog_function_to_sensor
import unittest

class TestRegistration(unittest.TestCase):
    def setUp(self):
        self.sensor = Sensor(sensor_name="registration_test")

    def test_register_analog_sensor(self):
        register_analog_function_to_sensor(self.sensor, {"soil_moisture": 28})
        self.assertEqual(self.sensor.analog_sensor_functions["soil_moisture"], 28)
        