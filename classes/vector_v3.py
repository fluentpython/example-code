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

# BEGIN VECTOR_V3_DEMO
Test of `x` and `y` read-only properties:

    >>> v1.x, v1.y
    (3.0, 4.0)
    >>> v1.x = 123
    Traceback (most recent call last):
      ...
    AttributeError: can't set attribute

# END VECTOR_V3_HASH_DEMO

# BEGIN VECTOR_V3_HASH_DEMO

    >>> v1 = Vector(3, 4)
    >>> v2 = Vector(3.1, 4.2)
    >>> hash(v1), hash(v2)
    (7, 384307168202284039)
    >>> len(set([v1, v2]))
    2


# END VECTOR_V3_DEMO


"""

from array import array
import math

# BEGIN VECTOR_V3
class Vector:
    typecode = 'd'

    def __init__(self, x, y):
        self.__x = float(x)  # <1>
        self.__y = float(y)

    @property  # <2>
    def x(self):  # <3>
        return self.__x  # <4>

    @property  # <5>
    def y(self):
        return self.__y

    def __iter__(self):
        return (i for i in (self.x, self.y))  # <6>

    # remaining methods follow (omitted in book listing)
# END VECTOR_V3

    def __repr__(self):
        return 'Vector({!r}, {!r})'.format(*self)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return bytes(array(Vector.typecode, self))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

# BEGIN VECTOR_V3_HASH
    def __hash__(self):
        return hash(self.x) ^ hash(self.y)
# END VECTOR_V3_HASH

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def angle(self):
        return math.atan2(self.y, self.x)

    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('p'):
            fmt_spec = fmt_spec[:-1]
            coords = (abs(self), self.angle())
            outer_fmt = '<{}, {}>'
        else:
            coords = self
            outer_fmt = '({}, {})'
        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(*components)

    @classmethod
    def frombytes(cls, octets):
        memv = memoryview(octets).cast(cls.typecode)
        return cls(*memv)
