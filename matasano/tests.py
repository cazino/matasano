import unittest


class HexToBase64(unittest.TestCase):

    def test(self):
        from matasano import hextobase64
        hex_str = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
        base64_str = 'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'
        result = hextobase64(hex_str)
        self.assertEquals(base64_str, result)
