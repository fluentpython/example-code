"""StrKeyDict always converts non-string keys to `str`

This is a variation of `strkeydict.StrKeyDict` implemented
as a `dict` built-in subclass (instead of a `UserDict` subclass)

Test for initializer: keys are converted to `str`.

    >>> d = StrKeyDict([(2, 'two'), ('4', 'four')])
    >>> sorted(d.keys())
    ['2', '4']

Tests for item retrieval using `d[key]` notation::

    >>> d['2']
    'two'
    >>> d[4]
    'four'
    >>> d[1]
    Traceback (most recent call last):
      ...
    KeyError: '1'

Tests for item retrieval using `d.get(key)` notation::

    >>> d.get('2')
    'two'
    >>> d.get(4)
    'four'
    >>> d.get(1, 'N/A')
    'N/A'

Tests for the `in` operator::

    >>> 2 in d
    True
    >>> 1 in d
    False

Test for item assignment using non-string key::

    >>> d[0] = 'zero'
    >>> d['0']
    'zero'

Tests for update using a `dict` or a sequence of pairs::

    >>> d.update({6:'six', '8':'eight'})
    >>> sorted(d.keys())
    ['0', '2', '4', '6', '8']
    >>> d.update([(10, 'ten'), ('12', 'twelve')])
    >>> sorted(d.keys())
    ['0', '10', '12', '2', '4', '6', '8']
    >>> d.update([1, 3, 5])
    Traceback (most recent call last):
      ...
    TypeError: 'int' object is not iterable

"""

import collections.abc


class StrKeyDict(dict):

    def __init__(self, iterable=None, **kwds):
        super().__init__()
        self.update(iterable, **kwds)

    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def __contains__(self, key):
        return key in self.keys() or str(key) in self.keys()

    def __setitem__(self, key, item):
        super().__setitem__(str(key), item)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def update(self, iterable=None, **kwds):
        if iterable is not None:
            if isinstance(iterable, collections.abc.Mapping):
                pairs = iterable.items()
            else:
                pairs = ((k, v) for k, v in iterable)
            for key, value in pairs:
                self[key] = value
        if kwds:
            self.update(kwds)
