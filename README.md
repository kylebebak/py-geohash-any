# py-geohash-any
**py-geohash-any** is a Python geohash library designed to be used with any encoding, focused on simplicity and clarity.

## Implementation
The core functions of the library work with binary geohashes. The functions for hashing, dehashing and finding neighbors wrap the core functions with calls to `to_urlsafe()` and `to_binary()`, which in turn depend on functions in `urlsafe.py`. If you want to use a different encoding, simply change the `ALPHABET` variable in `urlsafe.py`.

Base 32 (5-bit) encoding is often used to create a compressed url-safe string from a binary geohash. In base 32, each character encodes 5 **longitude/latitude halvings** of the (longitude, latitude) space. If you want to use base 32, uncomment the standard geohash base 32 alphabet, which is included in `urlsafe.py`.

By default, this library uses base 64 (6-bit) encoding, specifically [base64url](https://tools.ietf.org/html/rfc4648#section-5), which is slightly more compressed than base 32. Each character encodes 6 longitude/latitude halvings (3 of each). Adding one character to the geohash will result in a bounding box that is 64 times smaller.

Using base 64, an 8 character geohash provides a lat/lon bounding box that measures **.00001 by .00002 degrees**. At the equator, where this box is largest, this is roughly equivalent to **1 by 2 meters**.

## Installation
```sh
pip install py-geohash-any
```

## Examples
```py
from gh_any import geohash as gh

# encoding
gh.encode(83.345326, -114.876748, 8)
# 'Xbxg6yNP'

# decoding
gh.decode('Xbxg6yNP')
# {'h': 1e-05, 'lat': 83.345326, 'lon': -114.876748, 'w': 2.1e-05}

# finding neighbors
gh.neighbors(gh.encode(83.345326, -114.876748, 8))
# {'e': 'Xbxg6yNl', 'n': 'Xbxg6yNO', 'ne': 'Xbxg6yNk', 'nw': 'Xbxg6yNM',
# 's': 'Xbxg6yNa', 'se': 'Xbxg6yNw', 'sw': 'Xbxg6yNY', 'w': 'Xbxg6yNN'}

# finding neighbors with larger bounding boxes,
# e.g. to increase the range of a proximity search
gh.neighbors(gh.encode(83.345326, -114.876748, 8), 4)
# {'e': 'Xbxi', 'n': 'Xbw1', 'ne': 'Xbw3', 'nw': 'Xbwf', 
# 's': 'Xbxh', 'se': 'Xbxj', 'sw': 'XbxL', 'w': 'XbxK'}
```

## Tests
```sh
# run all unit tests
python -m unittest discover py_geohash_any.tests -v

# run unit tests in a single module
python -m py_geohash_any.tests.<module> -v
```


## LICENSE
This code is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).

The author of `urlsafe.py` is: <http://stackoverflow.com/users/64474/miles>. The code was posted on Stack Overflow, and is thus licensed under a Creative Commons Attribution-ShareAlike License.
