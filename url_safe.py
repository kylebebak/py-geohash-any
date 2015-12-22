import string
ALPHABET = string.ascii_lowercase + string.ascii_uppercase + \
           string.digits + '-_'
ALPHABET_REVERSE = dict((c, i) for (i, c) in enumerate(ALPHABET))
BASE = len(ALPHABET)
SIGN_CHARACTER = '$'

"""
Nice code written by this guy:
http://stackoverflow.com/users/64474/miles
"""

def to_base_64(n):
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

def from_base_64(s):
    """Converts base 64 string to integer."""
    if s[0] == SIGN_CHARACTER:
        return -num_decode(s[1:])
    n = 0
    for c in s:
        n = n * BASE + ALPHABET_REVERSE[c]
    return n
