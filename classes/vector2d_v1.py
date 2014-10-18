"""
A 2-dimensional vector class

    >>> v1 = Vector2d(3, 4)
    >>> x, y = v1  #<1>
    >>> x, y
    (3.0, 4.0)
    >>> v1  #<2>
    Vector2d(3.0, 4.0)
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
    >>> bool(v1), bool(Vector2d(0, 0))  #<7>
    (True, False)

Test of .frombytes() class method:

    >>> v1_clone = Vector2d.frombytes(bytes(v1))
    >>> v1_clone
    Vector2d(3.0, 4.0)
    >>> v1 == v1_clone
    True

So far, Vector2d instances are unhashable:

# BEGIN VECTOR2D_V1_UNHASHABLE_DEMO
    >>> v1 = Vector2d(3, 4)
    >>> hash(v1)
    Traceback (most recent call last):
      ...
    TypeError: unhashable type: 'Vector2d'
    >>> set([v1])
    Traceback (most recent call last):
      ...
    TypeError: unhashable type: 'Vector2d'

# END VECTOR2D_V1_UNHASHABLE_DEMO

"""

from array import array
import math


class Vector2d:
    typecode = 'd'

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __iter__(self):
        return (i for i in (self.x, self.y))

    def __repr__(self):
        return 'Vector2d({!r}, {!r})'.format(*self)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return bytes(array(Vector2d.typecode, self))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

# BEGIN VECTOR2D_V1
    @classmethod  # <1>
    def frombytes(cls, octets):  # <2>
        memv = memoryview(octets).cast(cls.typecode)  # <3>
        return cls(*memv)  # <4>
# END VECTOR2D_V1
