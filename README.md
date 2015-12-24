# py-geohash64
**py-geohash64** is a base 64 Python geohashing library, focused on simplicity and clarity.

## Implementation details
Base 32 (5-bit) encoding is often used to create a compressed url-safe string from a binary geohash. In base 32, each character encodes 5 **longitude/latitude** halvings of the `(longitude, latitude)` space.

This library uses base 64 (6-bit) encoding, specifically [base64url](https://tools.ietf.org/html/rfc4648#section-5), which is slightly more compressed than base 32. This means that each character encodes 6 **longitude/latitude** halvings (3 of each) per character. Adding one character to the geohash will result in a bounding box that is 64 (8x8) times smaller.

One consequence of using base 64 is that all geohashes encode an equal number of longitude and latitude halvings. This allows some functions in the library to be simplified and reused.

If you want to use a different encoding, the core functions of the library work with binary geohashes. The functions for hashing, dehashing and finding neighbors wrap these core functions with **base64url** encoding functions, and you could easily do the same with other **even-bit** encodings.


## Examples
```py
# encoding

# decoding

# finding neighbors

```

## Tests
```sh


```


## LICENSE
This code is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).

The author of base64url is: <http://stackoverflow.com/users/64474/miles>. The code was posted on Stack Overflow, and is thus licensed under a CC Attribution-ShareAlike license.
