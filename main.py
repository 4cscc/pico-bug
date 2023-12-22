from sensor import Sensor
from bme280 import BME280

sensor = Sensor(sensor_name="atmospheric",
                topic='sensor_data/atmospheric',
                reporting_interval_sec=2,
                I2CSensor=True)

environ_sensor = BME280(i2c=sensor.i2c_bus)
sensor.register_i2c_sensor_function('temperature',
                                    environ_sensor.read_temperature)
sensor.register_i2c_sensor_function('humidity',
                                    environ_sensor.read_humidity)
sensor.register_i2c_sensor_function('pressure',
                                    environ_sensor.read_pressure)


sensor.run()