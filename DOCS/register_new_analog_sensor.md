# Register New Analog Sensor

Analog sensors can be registered by passing a dictionary and base sensor instance to the `registre_analog_function_to_sensor` function found in the `registration` module.

Because the analog sensors rely on directly taking a reading from the end-point
sensor, the only things we need to tell our board about them is what we would
like them to be called and the pin from which the analog reading should be
taken. The reading is taken using the Micropython `machine.ADC.read_u16`
function.

### Registering the Soil Moisture Sensor


As an example, we will here register a capacitive soil moisture sensor to our pico.

To begin with, we create the dictionary that associates the name `soil_moisture_reg_test` to the pin number we want to take our reading from.

On the Pico, the pins available for use as ADC pins are 26, 27, and 28. It is possible to use other pins as ADC pins through careful software sampling, but that is well beyond the usecase here, but the option is available to developers in the future.

Taking a look at the `soil_moisture.py` file in our library, the dictionary we use to define the soil moisture sensor looks like:

```
sm = {'soil_moisture_reg_test': 28}
```
In turn this is imported during the demon, and then handed to our registration function(you can run this from `demos/demo_analog_sensor_registration.py`).

```
from sensor import Sensor
from registration import register_analog_function_to_sensor
from soil_moisture import sm

sensor = Sensor(sensor_name="demo_sensor_1")
register_analog_function_to_sensor(sensor=sensor, def_dict=sm)
```

You must first initialize a base sensor instance, then hand that instance in as the `sensor` parameter of the registration function, and the dictionary associating the name with the pin number as the argument to `def_dict`.

Whatever name use for the sensor will be recorded as the `measurement` name in the SensorHub database.

To check that the sensor was registered appropriately, you can print `<sensor-instance>.measurement_functions`, and you should see the name you provided as one of the keys in the output.