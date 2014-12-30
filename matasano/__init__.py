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


def score(text, upperize=True):
    """Scores a text so that
    an english text get a high score.
    A text in another language or in a non langugage
    should get a lower score.
    """
    char_score = {' ': 13, 'E': 12, 'T': 11, 'A': 11, 'O': 10, 'I': 9,
                  'N': 8, 'S': 7, 'H': 6, 'R': 5, 'D': 7, 'L': 6,
                  'U': 5}
    if upperize:
        text = text.upper()
    scores = defaultdict(int)
    for char in text:
        if char in char_score:
            scores[char] += char_score[char]
    return sum(scores.values()) / (12 * len(text))


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
            results[phrase] = score(phrase)
        sorted_results = sorted(results.items(),
                                key=operator.itemgetter(1),
                                reverse=True)
        return sorted_results[0][0]
