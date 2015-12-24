import unittest
from .. import base64url as url

class TestBase64URL(unittest.TestCase):

    def test_to_b64(self):
        self.assertEqual( url.to_b64(103063661257551), 'Xbxg6yNP' )

    def test_from_b64(self):
        self.assertEqual( url.from_b64('Xbxg6yNP'), 103063661257551 )


if __name__ == '__main__':
    unittest.main()
