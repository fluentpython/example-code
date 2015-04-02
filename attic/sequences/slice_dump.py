"""

    >>> sd = SliceDump()
    >>> sd[1]
    1
    >>> sd[2:5]
    slice(2, 5, None)
    >>> sd[:2]
    slice(None, 2, None)
    >>> sd[7:]
    slice(7, None, None)
    >>> sd[:]
    slice(None, None, None)
    >>> sd[1:9:3]
    slice(1, 9, 3)
    >>> sd[1:9:3, 2:3]
    (slice(1, 9, 3), slice(2, 3, None))
    >>> s = sd[1:9:3]
    >>> s.indices(20)
    (1, 9, 3)
    >>> s.indices(5)
    (1, 5, 3)
    >>> s.indices(1)
    (1, 1, 3)
    >>> s.indices(0)
    (0, 0, 3)

"""

class SliceDump:

    def __getitem__(self, pos):
        return pos
