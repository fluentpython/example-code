"""StrKeyDict0 converts non-string keys to `str` on lookup

# BEGIN STRKEYDICT0_TESTS

Tests for item retrieval using `d[key]` notation::

    >>> d = StrKeyDict0([('2', 'two'), ('4', 'four')])
    >>> d['2']
    'two'
    >>> d[4]
    'four'
    >>> d[1]
    Traceback (most recent call last):
      ...
    KeyError: '1'

Tests for the `in` operator::

    >>> 2 in d
    True
    >>> 1 in d
    False

# END STRKEYDICT0_TESTS
"""

# BEGIN STRKEYDICT0

class StrKeyDict0(dict):  # <1>

    def __missing__(self, key):
        if isinstance(key, str):  # <2>
            raise KeyError(key)
        return self[str(key)]  # <3>

    def __contains__(self, key):
        return key in self.keys() or str(key) in self.keys()  # <4>

# END STRKEYDICT0