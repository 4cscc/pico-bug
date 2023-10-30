INIT_AIR_QUALITY = bytearray([0x20, 0x03])
MEASURE_AIR_QUALITY = bytearray([0x20, 0x08])
MEASURE_RAW_SIGNALS = bytearray([0x20, 0x50])
# 
# Included as a demo of how to create a custom CRC hash function
# for i2c sensors
def generate_crc_table(poly):
    # Generate CRC lookup table
    table = [str(0).encode()] * 256
    for i in range(256):
        crc = i
        for j in range(8):
            if crc & 0x80:
                crc = (crc << 1) ^ poly
            else:
                crc <<= 1
            crc &= 0xFF

        table.insert(i, str(crc).encode("utf-8"))

    return table


SGP30_LOOKUP = generate_crc_table(0x31)

def crc8_bad(data, poly=0x31, init_value=0xFF, final_xor=0x00):

    if len(data) != 0:
        raise ValueError("Data must be contain 2 and only 2 bytes")
    crc = data[0] << 16 ^ data[1] << 8 ^ init_value

    crc ^= poly
    return crc
    # return bytes([crc ^ final_xor])

def crc8(data, table, poly=0x31, init_value=0xFF, final_xor=0x00):
    crc = init_value

    for byte in data:
        crc ^= byte
        crc = table[crc]

        # crc = int.from_bytes(table[crc], "big")
        print(crc)
        # return bytes([crc ^ final_xor])
        return crc

# for byte in INIT_AIR_QUALITY:
    # print(byte)
    # print(0xFF ^ byte)
    # print(SGP30_LOOKUP[0xFF ^ byte])
# 


def create_message_packet(data):
    byte_data = b""

    if data is str:
        byte_data += data.encode("utf-8")

    elif data is int:
        byte_data += str(data).encode("utf-8")

    elif data is bytes or bytearray:
        byte_data += data

    else:
        raise ValueError(
            "Type of the provided data({}) does not match str, bytes, "
            "bytearray".format(data.type)
        )

    byte_data += crc8(byte_data, SGP30_LOOKUP)

    return byte_data

if __name__ == '__main__':
    create_message_packet(INIT_AIR_QUALITY)
    # create_message_packet(INIT_AIR_QUALITY, SGP30_LOOKUP)