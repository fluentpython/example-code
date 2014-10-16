"""
A 2-dimensional vector class

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

Test of .frombytes() class method:

    >>> v1_clone = Vector.frombytes(bytes(v1))
    >>> v1_clone
    Vector(3.0, 4.0)
    >>> v1 == v1_clone
    True

So far, Vector instances are unhashable:

# BEGIN VECTOR_V1_UNHASHABLE_DEMO
    >>> v1 = Vector(3, 4)
    >>> hash(v1)
    Traceback (most recent call last):
      ...
    TypeError: unhashable type: 'Vector'
    >>> set([v1])
    Traceback (most recent call last):
      ...
    TypeError: unhashable type: 'Vector'

# END VECTOR_V1_UNHASHABLE_DEMO

"""

from array import array
import math


class Vector:
    typecode = 'd'

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __iter__(self):
        return (i for i in (self.x, self.y))

    def __repr__(self):
        return 'Vector({!r}, {!r})'.format(*self)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return bytes(array(Vector.typecode, self))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

# BEGIN VECTOR_V1
    @classmethod  # <1>
    def frombytes(cls, octets):  # <2>
        memv = memoryview(octets).cast(cls.typecode)  # <3>
        return cls(*memv)  # <4>
# END VECTOR_V1
