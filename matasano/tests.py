import binascii
import unittest


class HexToBase64(unittest.TestCase):

    def test(self):
        from matasano import hextobase64
        hex_str = ('49276d206b696c6c696e6720796f757220627261696'
                   'e206c696b65206120706f69736f6e6f7573206d757368726f6f6d')
        base64_str = ('SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtl'
                      'IGEgcG9pc29ub3VzIG11c2hyb29t')
        result = hextobase64(hex_str)
        self.assertEquals(base64_str, result)


class Xor(unittest.TestCase):

    def test(self):
        from matasano import xor
        hex1 = '1c0111001f010100061a024b53535009181c'
        hex2 = '686974207468652062756c6c277320657965'
        expected_hex = '746865206b696420646f6e277420706c6179'
        result = binascii.b2a_hex(xor(bytes.fromhex(hex1),
                                      bytes.fromhex(hex2))).decode()
        self.assertEquals(expected_hex, result)

    def test_shortest(self):
        from matasano import xor
        hex1 = '0000'  # 00000000
        hex2 = 'ff'    # 1111
        result = bytes.fromhex('ffff')  # 11111111
        self.assertEquals(result,
                          xor(bytes.fromhex(hex1),
                              bytes.fromhex(hex2)))


class EnglishScorerTest(unittest.TestCase):

    def test_full_score(self):
        from matasano import score
        text = ('EEEEEEEEEEEEE')
        self.assertEquals(1, score(text))

    def test_null_score(self):
        from matasano import score
        text = 'x'
        self.assertEquals(0, score(text))

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
        from matasano import decrypt
        xored = ('1b37373331363f78151b7f'
                 '2b783431333d7839782837'
                 '2d363c78373e783a393b3736')
        self.assertEquals("Cooking MC's like a pound of bacon",
                          decrypt(xored)[0][0])
