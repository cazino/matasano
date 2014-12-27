import base64


def hextobase64(hex_str):
    bytes_data = bytes.fromhex(hex_str)
    return base64.b64encode(bytes_data).decode()


def xor(hex1, hex2):
    result = int(hex1, 16) ^ int(hex2, 16)
    return '{:x}'.format(result)
