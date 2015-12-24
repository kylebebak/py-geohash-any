import unittest
from .. import urlsafe as url

class TestUrlSafe(unittest.TestCase):

    def test_to_urlsafe(self):
        self.assertEqual( url.to_urlsafe(103063661257551), 'Xbxg6yNP' )

    def test_from_urlsafe(self):
        self.assertEqual( url.from_urlsafe('Xbxg6yNP'), 103063661257551 )


if __name__ == '__main__':
    unittest.main()
