from sensor import Sensor
from bme280 import BME280
from machine import WDT

# sensor = Sensor(sensor_name="soil_moisture_demo_1")
# sensor.register_analog_sensor_function("soil_moisture", 28)

# I2C sensor example
sensor = Sensor(sensor_name="atmospheric",
                topic='sensor_data/atmospheric',
                I2CSensor=True,
                wdt=WDT(timeout=7000))

environ_sensor = BME280(i2c=sensor.i2c_bus)
sensor.register_i2c_sensor_function('temperature',
                                    environ_sensor.read_temperature)
sensor.register_i2c_sensor_function('humidity',
                                    environ_sensor.read_humidity)
sensor.register_i2c_sensor_function('pressure',
                                    environ_sensor.read_pressure)

if __name__ == "__main__":
    sensor.run()