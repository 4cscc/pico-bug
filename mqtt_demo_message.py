import json
import random

# intialize network connection

# setup mqtt-client

# generate_msg:

def generate_sensor_data_msg():
    """generate mqtt message packet for testing:

    packet:
        {
            "sensor": str
            "data": {
                "measurement0": value,
                "measurement1": value,
                .........
                "measurement_n": value
            }
        }
        needs to be byte encoded
    """
    message_str = json.dumps(
        {
            "sensor": "testing_sensor_1",
            "data": {
                "test_measure_1": random.randint(0, 255),
                "test_measure_2": random.random(),
            }

        }

    )
    return message_str

# publish


if __name__ == '__main__':
    print(generate_message())
    