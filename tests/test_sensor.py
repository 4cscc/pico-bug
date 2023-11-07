from ..sensor import Sensor
import pytest

class TestSensorRegistration:
    def setUp(self):
        sensor = Sensor()
        sensor.register_analog_sensor_function('test_analog_1', [28])