import time
import machine
from util import connect_network

# TODO: add a way to register a fun
try:
    import umqtt.simple as mqtt
except ImportError:
    connect_network()
    import mip
    mip.install('umqtt.simple')
    machine.reset()

import json

class Sensor:
    def __init__(self, sensor_name, topic='sensor_data', indicator_pin="LED", reporting_interval_sec=5, I2CSensor=False) -> None:
        self.sensor_name = sensor_name
        self.status = "initializing"
        self.network = None
        self.mqtt_handler = None
        self.topic = topic
        self.measurement_functions = dict()
        self.init_functions = dict()
        self.indicator_pin = machine.Pin(indicator_pin, machine.Pin.OUT)
        self.reporting_interval_sec = reporting_interval_sec
        self.pins = set()
        self.wdt = machine.WDT(timeout=8000)

        # setup i2c bus
        if I2CSensor:
            self.i2c_bus = machine.SoftI2C(sda=machine.Pin(0), scl=machine.Pin(1))
        else:
            self.i2c_bus = None

        # TODO: turn back on
        try:
            self.network = connect_network()
            self.status = "network connection established"
        except Exception as e:
            self.status = "failed to establish network connection, "
            "error: {}".format(e)

            machine.reset()
        
        mqtt_error_cnt = 0
        try:
            self.mqtt_handler = mqtt.MQTTClient(sensor_name, "10.42.0.1")
            mqtt_error_cnt = 0
        except Exception as e:
            self.status = "failed to establish mqtt connection, error: {}".format(e)
            mqtt_error_cnt += 1
            print(self.status)
            
            if mqtt_error_cnt > 5:
                machine.reset()
        
    def register_analog_sensor_function(self, name, pin):
        """adds a function to the sensor's measurement_functions dict"""

        # check to make sure pins unused.
        if pin in self.pins:
            raise ValueError(f"Pin {pin} already in use")
        else:
            self.pins.add(pin)

        if pin not in {26, 27, 28}: # Pins with ADC functionality on Pico W
            raise ValueError(f"Pin {pin} not a valid ADC pin")

        self.measurement_functions[name] = machine.ADC(pin).read_u16
        print("{}: {}".format(name, self.measurement_functions[name]()))

    
    def register_i2c_sensor_function(self, measurement_name, func):
        if self.i2c_bus is None:
            self.i2c_bus = machine.SoftI2C(sda=machine.Pin(0),
                                           scl=machine.Pin(1))
            print("I2C bus initialized")

        self.measurement_functions[measurement_name] = func

    def measurements(self):
        measurements = json.dumps(
            {
                "sensor": self.sensor_name,
                "data": {
                    key: value() for key, value in 
                    self.measurement_functions.items()
                   },
               }
           )
        print(measurements, "\n")
        return measurements

    def publish(self):
        self.indicator_pin.on()
        self.mqtt_handler.connect()
        self.mqtt_handler.publish(
            topic=bytes(self.topic, "utf-8"),
            msg=self.measurements(),
            qos=0
        )
        self.mqtt_handler.disconnect()
        self.wdt.feed()
        self.indicator_pin.off()
        time.sleep(self.reporting_interval_sec)

    def run(self):
        while True:
            for name, func in self.measurement_functions.items():
                print(name, func())
            self.publish()
            time.sleep(self.reporting_interval_sec)

