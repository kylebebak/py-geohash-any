"""
Module with geohashing functions. To simplify code, the following
assumptions are made:
    - all binary geohashes have an even number of characters, i.e.
    the number of lon and lat divisions is always equal. adding
    1 to the precision of binary encoding adds 2 chars, and corresponds
    to doubling the lon and lat precision
    - compressed url-safe geohashes are base 64, which means
    6 divisions (3 lon and 3 lat) are encoded in each char
    - NEIGHBORS
        * for binary geohashes, neighbors can be found at any level
        of precision
        * for base_64 geohashes, neighbors can be found for any number of
        characters, which means that neighbors can be found at any 3rd
        level of precision

from custom import geohash as gh

gh.encode_base_64(90, 180, 8)
gh.encode_base_64(-90, -180, 8)
gh.encode(83.34533, -114.87675, 24)
gh.encode_base_64(83.34533, -114.87675, 8)

gh.neighbors(gh.encode(83.34533, -114.87675, 24))
gh.neighbors(gh.encode(83.34533, -114.87675, 24), precision=12)
gh.neighbors_base_64(gh.encode_base_64(83.34533, -114.87675, 8))
gh.neighbors_base_64(gh.encode_base_64(83.34533, -114.87675, 8), precision=4)
"""

from . import url_safe

def _interleave(lon, lat):
    """Interleaves a lat and lon array and joins the result
    into a string."""
    lon_lat = []
    for c in range(len(lon)):
        lon_lat.append(lon[c])
        lon_lat.append(lat[c])
    return ''.join(lon_lat)


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

def encode(lat, lon, precision):
    """Encodes latitude and longitude as a string of 0s and 1s."""
    lon_hash = _encode(lon, 180, precision)
    lat_hash = _encode(lat, 90, precision)
    return _interleave(lon_hash, lat_hash)


def _nbr_prev(gh):
    """Helper function for computing N/W neighbors."""
    GH = list(gh)
    for i in range(len(GH)-1, -1, -1):
        if GH[i] == '0':
            GH[i] = '1'
        else:
            GH[i] = '0'
            break
    return GH

def _nbr_next(gh):
    """Helper function for computing S/E neighbors."""
    GH = list(gh)
    for i in range(len(GH)-1, -1, -1):
        if GH[i] == '1':
            GH[i] = '0'
        else:
            GH[i] = '1'
            break
    return GH

def neighbors(geohash, binary=True, precision=None):
    """Returns a dict with binary geohashes of all 8
    neighbors of the box defined by the geohash argument."""
    if not binary:
        geohash = to_binary(geohash)
    lon, lat = [], []
    for i, c in enumerate(geohash):
        if precision is not None and i >= precision*2:
            break
        lon.append(c) if i%2 == 0 else lat.append(c)

    W, N, E, S = _nbr_prev(lon), _nbr_prev(lat), _nbr_next(lon), _nbr_next(lat)
    return {
            'w': _interleave(W, lat), 'nw': _interleave(W, N),
            'n': _interleave(lon, N), 'ne': _interleave(E, N),
            'e': _interleave(E, lat), 'se': _interleave(E, S),
            's': _interleave(lon, S), 'sw': _interleave(W, S),
        }


def to_base_64(geohash):
    """Converts binary geohash string to url safe base 64 string."""
    return url_safe.to_base_64(
        int(geohash, 2)).rjust(len(geohash)//6, url_safe.ALPHABET[0])

def to_binary(geohash):
    """Converts base 64 geohash to binary string."""
    return bin(url_safe.from_base_64(geohash))[2:].zfill(6*len(geohash))

def encode_base_64(lat, lon, chars):
    """Encodes latitude and longitude as url safe base 64 string."""
    return to_base_64(encode(lat, lon, chars*3))

def neighbors_base_64(geohash, binary=False, precision=None):
    """Returns a dict with base 64 geohashes of all 8
    neighbors of the box defined by the geohash argument."""
    if not binary:
        geohash = to_binary(geohash)
    nbrs = neighbors(geohash) if precision is None \
        else neighbors(geohash, True, precision*3)
    return {k: to_base_64(v) for k, v in nbrs.items()}



