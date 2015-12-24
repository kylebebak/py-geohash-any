"""
Module with geohashing functions. To simplify the implementation, the following
choices were made:
    - All binary geohashes have an even number of characters, i.e.
    the number of lon and lat divisions is always equal. Adding
    1 to the precision of binary encoding adds 2 chars, and corresponds
    to doubling the lon and lat precision
    - Compressed url-safe geohashes are base 64, which means
    6 divisions (3 lon and 3 lat) are encoded in each char
"""

from . import base64url as url


def _truncate_decimal(num, precision):
    return int(num * 10**precision) / 10**precision


def to_b64(geohash):
    """Converts binary geohash string to url safe base 64 string."""
    return url.to_b64(
        int(geohash, 2)).rjust(len(geohash)//6, url.ALPHABET[0])

def to_binary(geohash):
    """Converts base 64 geohash to binary string."""
    return bin(url.from_b64(geohash))[2:].zfill(6*len(geohash))


def _interleave(lon, lat):
    """Interleaves a lon and lat array and joins the result
    into a binary string."""
    lon_lat = []
    for c in range(len(lon)):
        lon_lat.append(lon[c])
        lon_lat.append(lat[c])
    return ''.join(lon_lat)

def _split(geohash, precision=None):
    """Splits an interleaved binary string into lon and lat arrays."""
    lon, lat = [], []
    for i, c in enumerate(geohash):
        if precision is not None and i >= precision*2:
            break
        lon.append(c) if i%2 == 0 else lat.append(c)
    return lon, lat


def _encode(coord, max_coord, precision):
    """Returns a binary hash of latitude or longitude
    as an array of 0s and 1s."""
    encoding = []
    coord += max_coord
    for p in range(precision):
        if coord >= max_coord:
            coord -= max_coord
            encoding.append('1')
        else:
            encoding.append('0')
        max_coord /= 2
    return encoding

def _decode(geohash, max_coord):
    """Returns a tuple with the coord and the range of the boundary
    defined by the binary geohash."""
    coord = 0
    for c in geohash:
        max_coord /= 2
        coord = coord-max_coord if c == '0' else coord+max_coord
    return coord, max_coord*2

def encode(lat, lon, precision):
    """Encodes latitude and longitude as a string of 0s and 1s."""
    return _interleave(
        _encode(lon, 180, precision), _encode(lat, 90, precision))

def decode(geohash, binary_in=False):
    """Returns a dict with the lat/lon coords at the center of the bounding
    rectangle defined by the geohash, along with the lat and lon "width" and
    "height" of the bounding rectangle:

    {'lat':__, 'lon':__, 'h':__, 'w':__}"""

    if not binary_in:
        geohash = to_binary(geohash)
    lon, lat = _split(geohash)

    coords = {}
    coords['lon'], coords['w'] = _decode(lon, 180)
    coords['lat'], coords['h'] = _decode(lat, 90)
    return {k: _truncate_decimal(v, 6) for k, v in coords.items()}


def _nbr_prev(geohash):
    """Helper function for computing N/W neighbors."""
    GH = list(geohash)
    for i in range(len(GH)-1, -1, -1):
        if GH[i] == '0':
            GH[i] = '1'
        else:
            GH[i] = '0'
            break
    return GH

def _nbr_next(geohash):
    """Helper function for computing S/E neighbors."""
    GH = list(geohash)
    for i in range(len(GH)-1, -1, -1):
        if GH[i] == '1':
            GH[i] = '0'
        else:
            GH[i] = '1'
            break
    return GH

def neighbors(geohash, binary_in=True, precision=None):
    """Returns a dict with binary geohashes of all 8
    neighbors of the box defined by the geohash argument."""
    if not binary_in:
        geohash = to_binary(geohash)
    lon, lat = _split(geohash, precision)

    W, N, E, S = _nbr_prev(lon), _nbr_prev(lat), _nbr_next(lon), _nbr_next(lat)
    return {
            'w': _interleave(W, lat), 'nw': _interleave(W, N),
            'n': _interleave(lon, N), 'ne': _interleave(E, N),
            'e': _interleave(E, lat), 'se': _interleave(E, S),
            's': _interleave(lon, S), 'sw': _interleave(W, S),
        }


def encode_b64(lat, lon, chars):
    """Encodes latitude and longitude as url safe base 64 string."""
    return to_b64(encode(lat, lon, chars*3))

def neighbors_b64(geohash, binary_in=False, precision=None):
    """Returns a dict with base 64 geohashes of all 8
    neighbors of the box defined by the geohash argument."""
    if not binary_in:
        geohash = to_binary(geohash)
    nbrs = neighbors(geohash) if precision is None \
        else neighbors(geohash, True, precision*3)
    return {k: to_b64(v) for k, v in nbrs.items()}


