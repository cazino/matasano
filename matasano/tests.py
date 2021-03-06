import base64
import binascii
import os
import unittest


class HexToBase64(unittest.TestCase):

    def test(self):
        from matasano import hextobase64
        hex_str = ('49276d206b696c6c696e6720796f757220627261696'
                   'e206c696b65206120706f69736f6e6f7573206d757368726f6f6d')
        base64_str = ('SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtl'
                      'IGEgcG9pc29ub3VzIG11c2hyb29t')
        result = hextobase64(hex_str)
        self.assertEqual(base64_str, result)


class Xor(unittest.TestCase):

    def test(self):
        from matasano import xor
        hex1 = '1c0111001f010100061a024b53535009181c'
        hex2 = '686974207468652062756c6c277320657965'
        expected_hex = '746865206b696420646f6e277420706c6179'
        result = binascii.b2a_hex(xor(bytes.fromhex(hex1),
                                      bytes.fromhex(hex2))).decode()
        self.assertEqual(expected_hex, result)

    def test_shortest(self):
        from matasano import xor
        hex1 = '0000'  # 00000000
        hex2 = 'ff'    # 1111
        result = bytes.fromhex('ffff')  # 11111111
        self.assertEqual(result,
                         xor(bytes.fromhex(hex1),
                             bytes.fromhex(hex2)))

    def test_set1_challenge5(self):
        from matasano import xor
        bytes1 = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal""".encode()
        bytes2 = 'ICE'.encode()
        result = bytes.fromhex("0b3637272a2b2e63622c"
                               "2e69692a23693a2a3c632"
                               "4202d623d63343c2a2622"
                               "6324272765272a282b2f20"
                               "430a652e2c652a3124333a6"
                               "53e2b2027630c692b2028316"
                               "5286326302e27282f")
        self.assertEqual(result,
                         xor(bytes1,
                             bytes2))


class EnglishScorerTest(unittest.TestCase):

    def test_full_score(self):
        from matasano import score
        text = ('EEEEEEEEEEEEE')
        self.assertEqual(1, score(text))

    def test_null_score(self):
        from matasano import score
        text = 'x'
        self.assertEqual(0, score(text))

    def test_real_data(self):
        from matasano import score
        score1 = score("Cooking mc's like a pound of bacon")
        score2 = score('Occgebk,ao+\x7f,`egi,m,|cybh,cj,nmocb')
        self.assertGreater(score1, score2)

    def test_real_data2(self):
        from matasano import score
        score1 = score("Cooking mc's like a pound of bacon")
        score2 = score(
            '0\x1c\x1c\x18\x1a\x1d\x14s>0t\x00s\x1f'
            '\x1a\x18\x16s\x12s\x03\x1c\x06\x1d\x17s'
            '\x1c\x15s\x11\x12\x10\x1c\x1d')
        self.assertGreater(score1, score2)

    def test_real_data3(self):
        from matasano import score
        score1 = score("Cooking mc's like a pound of bacon")
        score2 = score('Ieeacdm*gi-y*fcao*k*ze\x7fdn*el*hkied')
        self.assertGreater(score1, score2)

    def test_real_data4(self):
        from matasano import score
        score1 = score("Cooking mc's like a pound of bacon")
        score2 = score('Eiimoha&KE!u&jomc&g&vishb&i`&dgeih')
        self.assertGreater(score1, score2)


class DecryptTest(unittest.TestCase):
    """  Set 1 Challenge 3
    """
    def test(self):
        from matasano import decrypt_with_printable
        xored = ('1b37373331363f78151b7f'
                 '2b783431333d7839782837'
                 '2d363c78373e783a393b3736')
        self.assertEqual("Cooking MC's like a pound of bacon",
                         decrypt_with_printable(bytes.fromhex(xored))[0][0])


class FindEncryptedTest(unittest.TestCase):
    """  Set 1 Challenge 4
    """
    def test(self):
        from matasano import find_encrypted
        module_dir = os.path.abspath(os.path.dirname(__file__))
        test_file = os.path.join(module_dir, 'data/set1-challenge4.txt')
        results = find_encrypted(test_file, 'latin-1')
        self.assertEqual('Now that the party is jumping\n',
                         results[0][1])


class HammingTest(unittest.TestCase):

    def test(self):
        from matasano import hamming
        str1 = "this is a test"
        str2 = "wokka wokka!!!"
        self.assertEqual(
            37,
            hamming(str1.encode('utf-32'), str2.encode('utf-32')))


class ChunkTest(unittest.TestCase):

    def test_two_chunk(self):
        from matasano import chunk
        data = b'zefkjn akrhg larhg ergh ozi'
        chunks = chunk(data, size=2, number=2)
        chunk0 = bytes([122, 101])
        chunk1 = bytes([102, 107])
        self.assertEqual(chunk0, next(chunks))
        self.assertEqual(chunk1, next(chunks))


class TransposeTest(unittest.TestCase):

    def test_simple(self):
        from matasano import transpose
        data = bytes([0, 1, 2, 3, 0, 1, 2, 3])
        blocks = transpose(data, 4)
        self.assertEqual(4, len(blocks))
        self.assertEqual(bytes([0, 0]), blocks[0])
        self.assertEqual(bytes([1, 1]), blocks[1])
        self.assertEqual(bytes([2, 2]), blocks[2])
        self.assertEqual(bytes([3, 3]), blocks[3])

    def test_not_round_size(self):
        from matasano import transpose
        data = bytes([0, 1, 2, 3, 0, 1, 2])
        blocks = transpose(data, 4)
        self.assertEqual(4, len(blocks))
        self.assertEqual(bytes([0, 0]), blocks[0])
        self.assertEqual(bytes([1, 1]), blocks[1])
        self.assertEqual(bytes([2, 2]), blocks[2])
        self.assertEqual(bytes([3]), blocks[3])


class TestBreakRepeatingKeyXor(unittest.TestCase):

    def test(self):
        from matasano import break_repeating_key_xor
        module_dir = os.path.abspath(os.path.dirname(__file__))
        test_file = os.path.join(module_dir, 'data/6.txt')
        with open(test_file, 'r') as f:
            bytes_data = base64.b64decode(f.read())
            key = break_repeating_key_xor(bytes_data)
            self.assertEqual(
                bytearray(b'Terminator X: Bring the noise'),
                key)
