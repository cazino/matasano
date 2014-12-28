import base64
import binascii
from collections import defaultdict
import difflib
import operator
import string


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


def score(text):
    """Scores plain english text  with
    "ETAOIN SHRDLU" occurences
    """

    ref = "ETAOINSHRDLU"
    exclude = " "
    occurences = defaultdict(int)
    for char in text:
        if char not in exclude:
            occurences[char] += 1
    sorted_occ = sorted(occurences.items(),
                        key=operator.itemgetter(1),
                        reverse=True)
    sorted_char = [x.capitalize() for (x, y) in sorted_occ]
    return difflib.SequenceMatcher(a=ref, b=sorted_char).ratio()


def decrypt(hexphrase):
    """ hex is hex encoded string
    hex is supposed to have been xor with a single character.
    Return the most likely unencoded original string
    """
    results = defaultdict(float)
    for char in string.printable:
        char_bytes = bytes(char, 'ascii')
        phrase = xor(hexphrase, binascii.hexlify(char_bytes).decode())\
            .decode()
        results[phrase] = score(phrase)
    sorted_results = sorted(results.items(),
                            key=operator.itemgetter(1),
                            reverse=True)
    return sorted_results[0][0]
