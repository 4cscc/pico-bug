## Register New Analog Sensor

Because analog sensors rely on directly taking a reading from the end-point
sensor, the only things we need to tell our board about them is what we would
like them to be called and the pin from which the analog reading should be
taken. The reading is taken using the Micropython `machine.ADC.read_u16`
function.

In addition to specifying the pin to be read and correctly attaching it, you should hook the power supply of the sensor to the `ADC_VREF` pin on the Pico(that is, pin #35), from which the Pico supplies a stable reference voltage, against which the analog sensor reading can be taken.

### Registering the Soil Moisture Sensor

As an example, we will here register a capacitive soil moisture sensor to a Pico.

On the Pico, the pins available for use as analog-to-digital converter (ADC) pins are 26, 27, and 28. It is possible to use other pins as ADC pins through careful software sampling, but that is well beyond the usecase here, but the option is available to developers in the future.

We can look at the `soil_moisture_main.py` file in the `mains` directory for how we can go about registering the soil moisture sensor.

```python
from sensor import Sensor

if __name__ == "__main__":
    sensor = Sensor(sensor_name="soil_moisture_demo_1")
    sensor.register_analog_sensor_function("soil_moisture", 28)

    sensor.run()
```

You must first initialize a base sensor instance, then use the `register_analog_sensor_function` method to name the reading to be taken from pin 28 "soil_moisture". Then at the specified reporting interval, the pico will take a reading from pin 28 and report it via MQTT message to the `Sensor-Hub`. Whatever name use for the sensor will be recorded as the `measurement` name in the `Sensor-Hub` database.

To check that the sensor was registered appropriately, you can print `<sensor-instance>.measurement_functions`, and you should see the name you provided as one of the keys in the output.