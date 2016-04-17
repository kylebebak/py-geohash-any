"""
A module for converting between
integer <--> urlsafe-string:

Author:
http://stackoverflow.com/users/64474/miles
"""

import string

# base64url
ALPHABET = string.ascii_uppercase + string.ascii_lowercase + \
    string.digits + '-_'

# standard geohash base 32
# ALPHABET = string.digits + 'bcdefghjkmnpqrstuvwxyz'

ALPHABET_REVERSE = dict((c, i) for (i, c) in enumerate(ALPHABET))
BASE = len(ALPHABET)
SIGN_CHARACTER = '$'

def to_urlsafe(n):
    """Converts integer to url-safe string."""
    if n < 0:
        return SIGN_CHARACTER + to_urlsafe(-n)
    s = []
    while True:
        n, r = divmod(n, BASE)
        s.append(ALPHABET[r])
        if n == 0:
            break
    return ''.join(reversed(s))

def from_urlsafe(s):
    """Converts base url-safe string to integer."""
    if s[0] == SIGN_CHARACTER:
        return -from_urlsafe(s[1:])
    n = 0
    for c in s:
        n = n * BASE + ALPHABET_REVERSE[c]
    return n
