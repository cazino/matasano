import base64
from collections import defaultdict
import operator
import string

from matasano.language import EnglishScorer


def hextobase64(hex_str):
    bytes_data = bytes.fromhex(hex_str)
    return base64.b64encode(bytes_data).decode()


def xor(bytes1, bytes2):
    result = bytearray()
    iterb2 = iter(bytes2)
    for elem1 in bytes1:
        try:
            elem2 = next(iterb2)
        except StopIteration:
            iterb2 = iter(bytes2)
            elem2 = next(iterb2)
        result.append(elem1 ^ elem2)
    return result


def decrypt(hexphrase):
        """ hex is hex encoded string
        hex is supposed to have been xor with a single character.
        Return the most likely unencoded original string
        """
        bytes_phrase = bytes.fromhex(hexphrase)
        results = defaultdict(float)
        for char in string.printable:
            char_bytes = bytes(char, 'ascii')
            xored = xor(bytes_phrase, char_bytes)
            phrase = xored.decode()  # .capitalize()
            results[phrase] = EnglishScorer().score(phrase)
        sorted_results = sorted(results.items(),
                                key=operator.itemgetter(1))
        return sorted_results[0][0]
