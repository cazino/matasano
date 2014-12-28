import base64
from collections import defaultdict
import operator
import string


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


def score(text):
    """Scores plain english text  with
    "ETAOIN SHRDLU" occurences
    """
    text = text.upper()
    ref = "ETAOINSHRDLU"
    occurences = defaultdict(int)
    for char in text:
        if char in string.ascii_uppercase:
            occurences[char] += 1
    sorted_occ = sorted(occurences.items(),
                        key=operator.itemgetter(1),
                        reverse=True)
    sorted_char = [x for (x, y) in sorted_occ
                   if x in string.ascii_uppercase + " "]
    distance = 0
    restricted_sorted_char = sorted_char[:12]
    for char in restricted_sorted_char:
        try:
            tmp_dist = abs(restricted_sorted_char.index(char) -
                           ref.index(char))
        except ValueError:
            tmp_dist = 12
        distance += tmp_dist
    if restricted_sorted_char:
        return distance / (12 * len(restricted_sorted_char))
    return 1


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

        phrase = xored.decode().capitalize()
        results[phrase] = score(phrase)
    sorted_results = sorted(results.items(),
                            key=operator.itemgetter(1))
    import ipdb
    ipdb.set_trace()
    return sorted_results[0][0]
