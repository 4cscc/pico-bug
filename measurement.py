import inspect


class Measurement:
    def __init__(self):
        self.measurement_functions = dict()
        self.pins = set()
    
    # def __repr__(self):
        # return "Sensor(measurement_functions={}, pins={})".format(
            # self.measurement_functions, self.pins)
# 
    def register_function(self, name, func, pins):
        # check to make sure pins unused 
        for pin in pins:
            if pin in self.pins:
                raise ValueError(f"Pin {pin} already in use")
            else:
                self.pins.add(pin)

        if not callable(func):
            raise ValueError(f"Function {func} is not callable")

        if str(inspect.signature(func)) != '()':
            raise ValueError(f"Function {func.__name__} takes arguments "
                             f"{str(inspect.signature(func))} but should not.")

        self.measurement_functions[name] = func
        self.pins = pins