import string
ALPHABET = string.ascii_uppercase + string.ascii_lowercase + \
    string.digits + '-_'
ALPHABET_REVERSE = dict((c, i) for (i, c) in enumerate(ALPHABET))
BASE = len(ALPHABET)
SIGN_CHARACTER = '$'

"""
A module for converting between
integer <--> b64-string:

Author:
http://stackoverflow.com/users/64474/miles

The "URL and Filename safe" Base 64 Alphabet, base64url
https://tools.ietf.org/html/rfc4648
"""

def to_b64(n):
    """Converts integer to base 64 string."""
    if n < 0:
        return SIGN_CHARACTER + num_encode(-n)
    s = []
    while True:
        n, r = divmod(n, BASE)
        s.append(ALPHABET[r])
        if n == 0:
            break
    return ''.join(reversed(s))

def from_b64(s):
    """Converts base 64 string to integer."""
    if s[0] == SIGN_CHARACTER:
        return -num_decode(s[1:])
    n = 0
    for c in s:
        n = n * BASE + ALPHABET_REVERSE[c]
    return n
