"""
Extended slicing:

    >>> s = SliceViewer()
    >>> s[1]
    1
    >>> s[:]
    slice(None, None, None)
    >>> s[1:2]
    slice(1, 2, None)
    >>> s[1:2:3]
    slice(1, 2, 3)
    >>> s[1:2:3:4]
    Traceback (most recent call last):
      ...
    SyntaxError: invalid syntax

N-dimensional indexing:

    >>> s[1, 2]
    (1, 2)

N-dimensional slicing:

    >>> s[1:3, 2]
    (slice(1, 3, None), 2)
    >>> s[1, :2:]
    (1, slice(None, 2, None))
    >>> s[:, :]
    (slice(None, None, None), slice(None, None, None))

"""


class SliceViewer:

	def __getitem__(self, position):
		return position
