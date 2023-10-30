import network
import rp2
import machine
import utime


# network stuff
rp2.country("US")


def connect_network(max_wait=10):
    """Connect to the network, return the wlan object"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print('active')
    wlan.connect("sensor_hub", "FourCorners")
    while max_wait > 0:

        if wlan.isconnected():
            print("Connection Established")
            return wlan
        else:
            max_wait -= 1
            print(
                "waiting for connection, current status: {}".format(
                    wlan.status())
            )
            utime.sleep(1)

    if wlan.status() != 3:
        print("Connection Failed, resetting machine")
        machine.reset()


# other 
def try_until_i2c(func):
    def wrapper_try_until_runs(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except OSError as oserr:
                print(oserr)
                continue
            except Exception as e:
                raise e
    return wrapper_try_until_runs


def crc8(msg):
    print('crc8 running')
    crc = 0xFF
    for byte in msg:
        crc ^= byte
        for _ in range(8):
            crc = (crc << 1) ^ 0x07 if crc & 0x80 else crc << 1
        crc &= 0xff
    final = [crc ^ 0x00]
    print(final)
    return str(final)

if __name__ == '__main__':
    i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
    i2c.write (0x59, crc8(b'0x20, 0x03'))



# Included as a demo of how to create a custom CRC hash function
# for i2c sensors
# def crc8(data, table, poly=0x31, init_value=0xFF, final_xor=0x00):
    # crc = init_value
# 
    # for byte in data:
        # crc ^= byte
        # crc = int.from_bytes(table[crc], "big")
        # return bytes([crc ^ final_xor])_atm(msg00
