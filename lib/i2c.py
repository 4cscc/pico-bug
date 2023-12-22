
#TODO: still in development

if I2CSensor:
    self.i2c_bus = machine.SoftI2C(sda=machine.Pin(0), scl=machine.Pin(1))
else:
    self.i2c_bus = None
    
def register_i2c_sensor_function(self, name, func_name, address, cmd, cmd_type, num_bytes=0):
    """Define data to read from i2c sensor
    
    name: name of the measurement
    address: i2c address of the sensor
    cmd: command to send to the sensor to initiate reading(will be a byte encoded integer)
    num_bytes: number of bytes to read from the sensor
    hash_func: function to hash the cmd to a byte encoded integer. If None, cmd will be sent as is. This is the default behavior, but some sensors require a hash function to be used, mostly those based on sensors used in safety critical applications in commercial applications, such as the air quality sensor.
    """
    target_dict = dict()
    
    if cmd_type == "init":
        target_dict = self.init_functions
    elif cmd_type == "measure":
        target_dict = self.measurement_functions
    else:
        raise ValueError("cmd_type must be one of: init, measure")
        
    if hash_func is None:
        target_dict[name] = (lambda : self.write_i2c(address, cmd))
    else:
        target_dict[name] = self.write_i2c(address, hash_func(cmd))

    print(target_dict)
    if cmd_type == 'measure':
        return self.read_i2c(address, num_bytes)
    

def _i2c_function_(self, address, cmd, num_bytes):
    self.write_i2c(address, cmd)
    return self.read_i2c(address, num_bytes)

def register_i2c_sensor_measurement_function(self, name, address, cmd, num_bytes):
    self.measurement_functions[name] = self._i2c_function_(address=address, cmd=cmd, num_bytes=num_bytes)

### SENSOR CLASS METHODS
 ### TODO: implement i2c functions and constructor
 def read_i2c(self, address, num_bytes):
     if self.i2c_bus is None:
         self.i2c_bus = machine.SoftI2C(sda=machine.Pin(0), scl=machine.Pin(1))
     return self.i2c_bus.readfrom(address, num_bytes)

 @try_until_i2c
 def write_i2c(self, address, data):
     if self.i2c_bus is None:
         self.i2c_bus = machine.SoftI2C(sda=machine.Pin(0), scl=machine.Pin(1))
     self.i2c_bus.writeto(address, data)
     time.sleep_ms(100)

#### dev/testing code)
    # INIT_AIR_QUALITY = b'\x20\x03'
    # MEASURE_AIR_QUALITY = bytearray([0x20, 0x08])
    # MEASURE_RAW_SIGNALS = bytearray([0x20, 0x50])
    # sensor.register_i2c_sensor_measurement_function(name = "air_quality_init", address=0x58, cmd=INIT_AIR_QUALITY, num_bytes=0)
    # sensor.register_i2c_sensor_measurement_function("measure_air_quality",
                                                    # address=0x58,
                                                    # cmd=MEASURE_AIR_QUALITY,
                                                    # num_bytes=3
                                                    # )
    # @sensor.register_measurement_function
    # def measure_air_quality(cls):
        # cls.write_i2c(0x58, MEASURE_AIR_QUALITY)
        # return cls.read_i2c(0x58, 3)
# 

    #                                                                      INIT_AIR_QUALITY = bytearray([0x20, 0x03]
     def register_i2c_measurement_function(name, address, cmd, num_bytes):
         def wrapper(*args, **kwargs):
             self.name = kwargs.get('name')
             self.write_i2c(address, cmd)
             self.read_i2c(address, num_bytes)
             out = func(*args, **kwargs)
             return out
         return wrapper
         # self.measurement_functions[f'{func.__name__}'] = wrapper

# generic measurment function decorator
    def register_measurement_function(self, func):
        def wrapper(*args, **kwargs):
            print(f'registering {func.__name__}')
            out = func(*args, **kwargs)
            print(f'"{func.__name__}" registered to "{self.sensor_name}"')
            return out
        # return wrapper
        self.measurement_functions[f'{func.__name__}'] = wrapper