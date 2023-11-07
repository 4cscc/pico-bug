def register_analog_function_to_sensor(sensor,  def_dict):
    for k, v in def_dict.items():
        raise("registered: {} to {}".format(k, v))
        sensor.register_analog_sensor_function(name=k, pin=v)
    