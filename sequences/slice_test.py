"""

    >>> s = SliceDemo()
    >>> s[1]
    __getitem__: 1
    1
    >>> s[2:5]
    __getitem__: slice(2, 5, None)
    [2, 3, 4]
    >>> s[:2]
    __getitem__: slice(None, 2, None)
    [0, 1]
    >>> s[7:]
    __getitem__: slice(7, None, None)
    [7, 8, 9]
    >>> s[:]
    __getitem__: slice(None, None, None)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> s[1:9:3]
    __getitem__: slice(1, 9, 3)
    [1, 4, 7]
    >>> s[1:9:3, 2:3]
    __getitem__: (slice(1, 9, 3), slice(2, 3, None))
    ERROR: list indices must be integers, not tuple

"""

class SliceDemo:

    def __init__(self):
        self.items = list(range(10))

    def __getitem__(self, pos):
        print('__getitem__:', pos)
        try:
            return self.items.__getitem__(pos)
        except TypeError as e:
            print('ERROR:', e)
