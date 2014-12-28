import base64
import binascii


def hextobase64(hex_str):
    bytes_data = bytes.fromhex(hex_str)
    return base64.b64encode(bytes_data).decode()


def xor(hex1, hex2):
    b1 = bytes.fromhex(hex1)
    b2 = bytes.fromhex(hex2)
    result = bytearray()
    iterb2 = iter(b2)
    for elem1 in b1:
        try:
            elem2 = next(iterb2)
        except StopIteration:
            iterb2 = iter(b2)
            elem2 = next(iterb2)
        result.append(elem1 ^ elem2)
    return binascii.hexlify(result).decode()
