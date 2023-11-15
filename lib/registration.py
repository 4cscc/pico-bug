def register_analog_function_to_sensor(sensor,  def_dict):
    for k, v in def_dict.items():
        sensor.register_analog_sensor_function(name=k, pin=v)
    
# 
# def register_I2C_function_to_sensor(sensor,  def_dict):
    # for k, v in def_dict.items():
        # sensor.register_digital_sensor_function(name=k, pin=v)