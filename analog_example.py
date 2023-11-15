from sensor import Sensor

if __name__ == "__main__":
    sensor = Sensor(sensor_name="soil_moisture_demo_1")
    sensor.register_analog_sensor_function("soil_moisture", 28)

    sensor.run()