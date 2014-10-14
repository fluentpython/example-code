"""
A 2-dimensional vector class

# BEGIN VECTOR_V0_DEMO

    >>> v1 = Vector(3, 4)
    >>> x, y = v1  #<1>
    >>> x, y
    (3.0, 4.0)
    >>> v1  #<2>
    Vector(3.0, 4.0)
    >>> v1_clone = eval(repr(v1))  #<3>
    >>> v1 == v1_clone
    True
    >>> print(v1)  #<4>
    (3.0, 4.0)
    >>> octets = bytes(v1)  #<5>
    >>> octets
    b'\\x00\\x00\\x00\\x00\\x00\\x00\\x08@\\x00\\x00\\x00\\x00\\x00\\x00\\x10@'
    >>> abs(v1)  #<6>
    5.0
    >>> bool(v1), bool(Vector(0, 0))  #<7>
    (True, False)

# END VECTOR_V0_DEMO
"""

# BEGIN VECTOR_V0
from array import array
import math


class Vector:
    typecode = 'd'  # <1>

    def __init__(self, x, y):
        self.x = float(x)    # <2>
        self.y = float(y)

    def __iter__(self):
        return (i for i in (self.x, self.y))  # <3>

    def __repr__(self):
        return 'Vector({!r}, {!r})'.format(*self)  # <4>

    def __str__(self):
        return str(tuple(self))  # <5>

    def __bytes__(self):
        return bytes(array(Vector.typecode, self))  # <6>

    def __eq__(self, other):
        return tuple(self) == tuple(other)  # <7>

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))  # <8>
# END VECTOR_V0
