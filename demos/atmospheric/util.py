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
