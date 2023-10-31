class Tools:
    def __init__(self):
        self.__name__ = 'Tools'
        self.pliers = dict()
        self.wrench = dict()
        self.screwdrivers = dict()


    def display_pliers(self):
        print(self.pliers)
        for tool in self.pliers:
            self.pliers[tool]


    def register_tool(func, cls):
    
        print(cls.__name__)
    
        def wrapper(*args, **kwargs):
            print('registering tool')
            # cls.pliers[f'{func.__name__}'] =
            out = func(*args, **kwargs)
            print('tool registered')
            return out
        # return wrapper
        cls.pliers[f'{func.__name__}'] = wrapper







# def register_i2c_function(address, cmd, num_bytes, hash_func=None):
    # """Define data to read from i2c sensor
    # 
    # address: i2c address of the sensor
    # cmd: command to send to the sensor to initiate reading(will be a byte encoded integer)
    # num_bytes: number of bytes to read from the sensor
    # hash_func: function to hash the cmd to a byte encoded integer. If None, cmd will be sent as is. This is the default behavior, but some sensors require a hash function to be used, mostly those based on sensors used in safety critical applications in commercial applications, such as the air quality sensor.
    # """
    # def decorator(func):
        # def wrapper(*args, **kwargs):
            # if hash_func is None:
                # return func(*args, **kwargs)
            # else:
                # return func(*args, **kwargs)
        # return wrapper
    # return decorator

tools = Tools()


def needlenose(plier_cnt):
    print('needlenose')
    return plier_cnt

register_tool(func=needlenose, cls=tools)
print("-"*25)
# b(5)
# b(7)
print(tools.pliers)
print(tools.pliers['needlenose'](4))
# tools.register_tool(func=needlenose, dup_num=1)
# 
# def adjustable():
    # print('adjustable')
# tools.register_tool(func=adjustable, dup_num=9)
# 
# tools.display_pliers()

# class Test(object):
    # def _decorator(foo):
        # def magic( self ) :
            # print("start magic")
            # foo( self )
            # print("end magic")
        # return magic
# 
    # @_decorator
    # def bar( self ) :
        # print("normal call")
# 
# test = Test()

# test.bar()