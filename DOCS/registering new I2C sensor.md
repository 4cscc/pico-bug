# Registering A New I2C Sensor

The process of registering an I2C sensor are somewhat more challenging than
those of registering an analog sensor. That is because the interface for
interacting with each particular sensor is determined by the design of the
sensor itself. If there is not a pre-built library for the sensor available in
`Micropython`, then it will be necessary to write one from scratch. To do so, it
is often helpful to look at various Arduino libraries, such as [`Arduino
SensorKit`](https://github.com/arduino-libraries/Arduino_SensorKit), or the
sensor IC's data sheet. When implementing the driver library for the particular
sensor, the end goal is to create a single function call that will request and
return a reading from the sensor.

In the `Sensor` class, the method `register_i2c_sensor_function` takes the name
you would like the measurement to be given, and the actual function to be called
to get the reading from the sensor module. As of now, the only type of function
with a place to be registered are measurement functions, though it would be
possible to add registration for other types of I2C functions in the future.

## BME280 example
Here we will take a look at using the BME280 with the Pico. To see how this done
at a high level, we can take a look at `mains/atmospheric_main.py`:

```python
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
```

Here, the sensor functions are defined in the `bme280` module. There is a single
function to get the reading value of each of our target measurements,
`temperature`, `humidity`, and `pressure`.

Setting `I2CSensor` to `True` to tell the Sensor base class to initialize with a
I2C bus connection enabled. The bus connection here is passed to the `BME280`
class for use when it is calling I2C functions.

