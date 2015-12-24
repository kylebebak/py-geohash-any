import unittest
from .. import geohash as gh

class TestGeohash(unittest.TestCase):

    def test_encode(self):
        self.assertEqual( gh.encode(90, 180, 8), '________' )
        self.assertEqual( gh.encode(-90, -180, 8), 'AAAAAAAA' )
        self.assertEqual( gh.encode(0, 0, 8), 'wAAAAAAA' )

    def test_encode_bin(self):
        self.assertEqual(
            gh.encode_bin(83.345326, -114.876748, 23),
            '01011101101111000110000' )
        self.assertEqual(
            gh.encode_bin(83.345326, -114.876748, 24),
            '010111011011110001100000' )

    def test_decode(self):
        coords = gh.decode(
            '010111011011110001100000111010110010001101001111', binary_in=True)
        self.assertEqual( coords['lon'], -114.876748 )
        self.assertEqual( coords['lat'], 83.345326 )
        coords = gh.decode('Xbxg6yNP')
        self.assertEqual( coords['lon'], -114.876748 )
        self.assertEqual( coords['lat'], 83.345326 )

    def test_neighbors(self):
        nbrs = gh.neighbors_bin(gh.encode_bin(83.345326, -114.876748, 17))
        self.assertEqual( nbrs['ne'], '01011101101110011' )
        self.assertEqual( nbrs['sw'], '01011101101101111' )
        nbrs = gh.neighbors_bin(gh.encode_bin(83.345326, -114.876748, 17), 12)
        self.assertEqual( nbrs['ne'], '010111110000' )
        self.assertEqual( nbrs['sw'], '010111011100' )


if __name__ == '__main__':
    unittest.main()
