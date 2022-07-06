from dns import *
import unittest

class TestDns(unittest.TestCase):

    def test_upper(self):
        assert len(header_bytes) == 2 * 6,  len(header_bytes)
        bytes_head = bytes([0x01,0x00,0x00,0x01])
        assert request_bytes[2:len(bytes_head) + 2] == bytes_head, request_bytes[2:len(bytes_head) + 2]
    
    def test_encoding(self):
        assert encode_domain("image.google.com") == bytes([
                5,
            ]) + "image".encode() + bytes([
                6
            ]) + "google".encode() + bytes([
                3
            ]) + "com".encode() + bytes([0x0])

if __name__ == '__main__':
    unittest.main()

