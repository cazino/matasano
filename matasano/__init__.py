import base64
from collections import defaultdict
import itertools
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


def _get_from_tuple(t):
    return t[1][0]


def decrypt_with_printable(bytes_phrase, encoding='utf-8'):
        """ hex is hex encoded string
        hex is supposed to have been xor with a single character.
        Return the most likely unencoded original string
        """
        results = dict()
        for char in string.printable:
            char_bytes = bytes(char, encoding)
            xored = xor(bytes_phrase, char_bytes)
            phrase = xored.decode(encoding)
            results[phrase] = (score(phrase), char_bytes)
        sorted_results = sorted(results.items(),
                                key=_get_from_tuple,
                                reverse=True)
        return sorted_results


def find_encrypted(filepath, encoding='utf-8'):
    results = list()
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            tmp_results = \
                [(line, decrypted, score) for (decrypted, (score, key))
                 in decrypt_with_printable(bytes.fromhex(line), encoding)]
            results.extend(tmp_results)
    return sorted(results,
                  key=operator.itemgetter(2),
                  reverse=True)


def encrypt_file(filepath, cryptkey):
    cryptkey_bytes = cryptkey.encode()
    with open(filepath, 'rb') as f:
        bytes_from_file = f.read()
        crypted_bytes = xor(bytes_from_file, cryptkey_bytes)
        return crypted_bytes


def hamming(bytes1, bytes2):
    assert len(bytes1) == len(bytes2)
    result = 0
    for b1, b2 in zip(bytes1, bytes2):
        result += bin(b1 ^ b2).count('1')
    return result


def chunk(bytes_data, size, number):
    for _ in range(number):
        yield bytes_data[:size]
        bytes_data = bytes_data[size:]


def compute_chunk_distance(bytes_data, key_size, chunk_num):
    distance = 0
    chunks1 = chunk(bytes_data, key_size, chunk_num)
    chunks2 = chunk(bytes_data, key_size, chunk_num)
    count = 0
    for c1, c2 in itertools.product(chunks1, chunks2):
        if c1 != c2:
            distance += hamming(c1, c2)
            count += 1
    distance_moy = distance / count
    distance_norm = distance_moy / key_size
    return distance_norm


def compute_distance_by_keysize(bytes_data, size_min, size_max, chunk_num):
    results = dict()
    for key_size in range(size_min, size_max):
        results[key_size] = compute_chunk_distance(
            bytes_data, key_size, chunk_num)
    return results


def transpose(bytes_data, size):
    blocks = list()
    while bytes_data:
        blocks.append(bytes_data[:size])
        bytes_data = bytes_data[size:]
    non_null_bytes = [t for t in itertools.zip_longest(*blocks)]
    return [bytes(filter(_is_not_None, bytes_array))
            for bytes_array in non_null_bytes]


def _is_not_None(x):
    return x is not None


def break_repeating_key_xor(bytes_data):
    distances_by_keysize = compute_distance_by_keysize(
        bytes_data, 2, 40, 4)
    ordered_distances = sorted(
        distances_by_keysize.items(), key=operator.itemgetter(1))
    keysize, distance = ordered_distances[0]
    transposed = transpose(bytes_data, keysize)
    secretkey = bytearray()
    for block in transposed:
        block_result = decrypt_with_printable(block)
        decrypted, (score, key) = block_result[0]
        secretkey.extend(key)
    return secretkey
