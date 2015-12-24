"""
Look at README for implementation details. For changing the encoding used
for url-safe geohashes, edit in ALPHABET.
"""

from math import log
from . import urlsafe as url

BITS = log(len(url.ALPHABET)) / log(2)
if not BITS.is_integer():
    raise Exception('Alphabet length is not a power of two.')
BITS = int(BITS)

def to_urlsafe(geohash):
    """Converts binary geohash to compressed url-safe geohash."""
    return url.to_urlsafe(
        int(geohash, 2)).rjust(len(geohash)//BITS, url.ALPHABET[0])

def to_binary(geohash):
    """Converts url-safe geohash to binary geohash."""
    return bin(url.from_urlsafe(geohash))[2:].zfill(BITS*len(geohash))


def _truncate_decimal(num, precision):
    """To avoid coordinates whose precision greatly exceeds their accuracy."""
    return int(num * 10**precision) / 10**precision

def _interleave(lon, lat):
    """Interleaves a lon and lat array and joins the result
    into a binary string."""
    lon_lat = []
    for c in range(len(lon)):
        lon_lat.append(lon[c])
        if c >= len(lat):
            continue
        lon_lat.append(lat[c])
    return ''.join(lon_lat)

def _split(geohash, chars=None):
    """Splits an interleaved binary string into lon and lat arrays."""
    lon, lat = [], []
    for i, c in enumerate(geohash):
        if chars is not None and i >= chars:
            break
        lon.append(c) if i%2 == 0 else lat.append(c)
    return lon, lat


def _encode(coord, max_coord, chars):
    """Returns a binary geohash of longitude or latitude
    as an array of 0s and 1s."""
    encoding = []
    coord += max_coord
    for p in range(chars):
        if coord >= max_coord:
            coord -= max_coord
            encoding.append('1')
        else:
            encoding.append('0')
        max_coord /= 2
    return encoding

def encode_bin(lat, lon, chars):
    """Encodes longitude and latitude as a string of 0s and 1s."""
    p_lat = chars//2
    p_lon = p_lat if chars%2 == 0 else p_lat+1

    return _interleave( _encode(lon, 180, p_lon), _encode(lat, 90, p_lat) )

def _decode(geohash, max_coord):
    """Returns a tuple with the coord and the range of the boundary
    defined by the binary geohash."""
    coord = 0
    for c in geohash:
        max_coord /= 2
        coord = coord-max_coord if c == '0' else coord+max_coord
    return coord, max_coord*2


def _nbr_prev(geohash):
    """Helper function for computing S/W neighbors."""
    GH = list(geohash)
    for i in range(len(GH)-1, -1, -1):
        if GH[i] == '0':
            GH[i] = '1'
        else:
            GH[i] = '0'
            break
    return GH

def _nbr_next(geohash):
    """Helper function for computing N/E neighbors."""
    GH = list(geohash)
    for i in range(len(GH)-1, -1, -1):
        if GH[i] == '1':
            GH[i] = '0'
        else:
            GH[i] = '1'
            break
    return GH

def neighbors_bin(geohash, chars=None):
    """Returns a dict with binary geohashes of all 8
    neighbors of the box defined by the binary geohash argument."""
    lon, lat = _split(geohash, chars)

    W, S, E, N = _nbr_prev(lon), _nbr_prev(lat), _nbr_next(lon), _nbr_next(lat)
    return {
            'w': _interleave(W, lat), 'nw': _interleave(W, N),
            'n': _interleave(lon, N), 'ne': _interleave(E, N),
            'e': _interleave(E, lat), 'se': _interleave(E, S),
            's': _interleave(lon, S), 'sw': _interleave(W, S),
        }


def encode(lat, lon, chars):
    """Encodes longitude and latitude as a url-safe geohash."""
    return to_urlsafe(encode_bin(lat, lon, chars*BITS))

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

def neighbors(geohash, chars=None):
    """Returns a dict with url-safe geohashes of all 8 neighbors
    of the box defined by the url-safe geohash argument."""
    geohash = to_binary(geohash)

    nbrs = neighbors_bin(geohash) if chars is None \
        else neighbors_bin(geohash, chars*BITS)
    return {k: to_urlsafe(v) for k, v in nbrs.items()}


