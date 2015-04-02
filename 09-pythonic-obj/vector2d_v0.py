"""
A 2-dimensional vector class

# BEGIN VECTOR2D_V0_DEMO

    >>> v1 = Vector2d(3, 4)
    >>> print(v1.x, v1.y)  # <1>
    3.0 4.0
    >>> x, y = v1  # <2>
    >>> x, y
    (3.0, 4.0)
    >>> v1  # <3>
    Vector2d(3.0, 4.0)
    >>> v1_clone = eval(repr(v1))  # <4>
    >>> v1 == v1_clone  # <5>
    True
    >>> print(v1)  # <6>
    (3.0, 4.0)
    >>> octets = bytes(v1)  # <7>
    >>> octets
    b'd\\x00\\x00\\x00\\x00\\x00\\x00\\x08@\\x00\\x00\\x00\\x00\\x00\\x00\\x10@'
    >>> abs(v1)  # <8>
    5.0
    >>> bool(v1), bool(Vector2d(0, 0))  # <9>
    (True, False)

# END VECTOR2D_V0_DEMO
"""

# BEGIN VECTOR2D_V0
from array import array
import math


class Vector2d:
    typecode = 'd'  # <1>

    def __init__(self, x, y):
        self.x = float(x)    # <2>
        self.y = float(y)

    def __iter__(self):
        return (i for i in (self.x, self.y))  # <3>

    def __repr__(self):
        class_name = type(self).__name__
        return '{}({!r}, {!r})'.format(class_name, *self)  # <4>

    def __str__(self):
        return str(tuple(self))  # <5>

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) +  # <6>
                bytes(array(self.typecode, self)))  # <7>

    def __eq__(self, other):
        return tuple(self) == tuple(other)  # <8>

    def __abs__(self):
        return math.hypot(self.x, self.y)  # <9>

    def __bool__(self):
        return bool(abs(self))  # <10>
# END VECTOR2D_V0
