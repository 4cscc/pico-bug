# import inspect
from demo_i2c import INIT_AIR_QUALITY
import time
import machine
from util import connect_network, crc8, try_until_i2c
import umqtt.simple as mqtt
import json
# from demo_i2c import create_message_packet

class Sensor:
    def __init__(self, sensor_name, topic='sensor_data', indicator_pin = "LED", reporting_interval_sec = 5, I2CSensor=False) -> None:
        # not sure that having the instance name is better than the sensor name
        # (_,_,_,text)=traceback.extract_stack()[-2]
        # self.instance_name = text[:text.find('=')].strip()

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

        # TODO: turn back on
        # try:
            # self.network = connect_network()
            # self.status = "network connection established"
        # except Exception as e:
            # self.status = "failed to establish network connection, error: {}".format(e)
            # machine.reset()

        # try:
            # self.mqtt_handler = mqtt.MQTTClient(sensor_name, "10.42.0.1")
        # except Exception as e:
            # self.status = "failed to establish mqtt connection, error: {}".format(e)
            # machine.reset()
        if I2CSensor:
            self.i2c_bus = machine.SoftI2C(sda=machine.Pin(0), scl=machine.Pin(1))
        else:
            self.i2c_bus = None
    
    # def register_i2c_sensor_function(self, name, func_name, func_code, hash_func):
# 
        # if not self.i2c_bus:
            # self.i2c_bus = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
# 

    def register_analog_sensor_function(self, name, pin):
        """adds a function to the sensor's measurement_functions dict"""
        # check to make sure pins unused 
        if pin in self.pins:
            raise ValueError(f"Pin {pin} already in use")
        else:
            self.pins.add(pin)

        if pin not in {26, 27, 28}: # Pins with ADC functionality on Pico W
            raise ValueError(f"Pin {pin} not a valid ADC pin")

        self.measurement_functions[name] = machine.ADC(pin).read_u16
        # print("{}: {}".format(name, self.measurement_functions[name]()))

    # def register_i2c_sensor_function(self, name, func_name, address, cmd, cmd_type, num_bytes=0):
        # """Define data to read from i2c sensor
        # 
        # name: name of the measurement
        # address: i2c address of the sensor
        # cmd: command to send to the sensor to initiate reading(will be a byte encoded integer)
        # num_bytes: number of bytes to read from the sensor
        # hash_func: function to hash the cmd to a byte encoded integer. If None, cmd will be sent as is. This is the default behavior, but some sensors require a hash function to be used, mostly those based on sensors used in safety critical applications in commercial applications, such as the air quality sensor.
        # """
        # target_dict = dict()
        # 
        # if cmd_type == "init":
            # target_dict = self.init_functions
        # elif cmd_type == "measure":
            # target_dict = self.measurement_functions
        # else:
            # raise ValueError("cmd_type must be one of: init, measure")
            # 
        # if hash_func is None:
            # target_dict[name] = (lambda : self.write_i2c(address, cmd))
        # else:
            # target_dict[name] = self.write_i2c(address, hash_func(cmd))

        # print(target_dict)
        # if cmd_type == 'measure':
            # return self.read_i2c(address, num_bytes)
        

    # def _i2c_function_(self, address, cmd, num_bytes):
        # self.write_i2c(address, cmd)
        # return self.read_i2c(address, num_bytes)

    # def register_i2c_sensor_measurement_function(self, name, address, cmd, num_bytes):
        # self.measurement_functions[name] = self._i2c_function_(address=address, cmd=cmd, num_bytes=num_bytes)
    
    
    ### TODO: implement i2c functions and constructor
    def read_i2c(self, address, num_bytes):
        if self.i2c_bus is None:
            self.i2c_bus = machine.SoftI2C(sda=machine.Pin(0), scl=machine.Pin(1))
        return self.i2c_bus.readfrom(address, num_bytes)

    # @try_until_i2c
    def write_i2c(self, address, data):
        if self.i2c_bus is None:
            self.i2c_bus = machine.SoftI2C(sda=machine.Pin(0), scl=machine.Pin(1))
        self.i2c_bus.writeto(address, data)
        time.sleep_ms(100)

    def measurements(self):
        measurements = json.dumps(
            {
                "sensor": self.sensor_name,
                "data": {
                    key: value() for key, value in self.measurement_functions.items()
                   },
               }
           )
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
        self.indicator_pin.off()
        time.sleep(self.reporting_interval_sec)


    def run(self):
        print(self.i2c_bus.scan())
        while True:
            for name, func in self.measurement_functions.items():
                print(name, func())
            # print(self.measurement_functions['air_quality_init']())
            # if not self.network.isconnected():
                # self.network = connect_network()
            # self.publish()
            time.sleep(self.reporting_interval_sec)
        
    def register_measurement_function(self, func):
        def wrapper(*args, **kwargs):
            print(f'registering {func.__name__}')
            out = func(*args, **kwargs)
            print(f'"{func.__name__}" registered to "{self.sensor_name}"')
            return out
        # return wrapper
        self.measurement_functions[f'{func.__name__}'] = wrapper

def register_i2c_measurement_function(name, address, cmd, num_bytes):
    def wrapper(*args, **kwargs):
        name = kwargs.get('name')
        self.write_i2c(address, cmd)
        self.read_i2c(address, num_bytes)
        out = func(*args, **kwargs)
        return out
    return wrapper
    # self.measurement_functions[f'{func.__name__}'] = wrapper

# Below for testing

if __name__ == "__main__":
    sensor = Sensor(sensor_name="lamest_demo_ever", I2CSensor=True)
    sensor.register_analog_sensor_function("soil_moisture", 28)


    # INIT_AIR_QUALITY = bytearray([0x20, 0x03])
    # INIT_AIR_QUALITY = b'\x20\x03'
    MEASURE_AIR_QUALITY = bytearray([0x20, 0x08])
    # MEASURE_RAW_SIGNALS = bytearray([0x20, 0x50])
    # sensor.register_i2c_sensor_measurement_function(name = "air_quality_init", address=0x58, cmd=INIT_AIR_QUALITY, num_bytes=0)
    # sensor.register_i2c_sensor_measurement_function("measure_air_quality",
                                                    # address=0x58,
                                                    # cmd=MEASURE_AIR_QUALITY,
                                                    # num_bytes=3
                                                    # )
    @sensor.register_measurement_function
    def measure_air_quality(cls):
        cls.write_i2c(0x58, MEASURE_AIR_QUALITY)
        return cls.read_i2c(0x58, 3)


    sensor.run()