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


Tests of ``format()`` with Cartesian coordinates:

    >>> format(v1)
    '(3.0, 4.0)'
    >>> format(v1, '.2f')
    '(3.00, 4.00)'
    >>> format(v1, '.3e')
    '(3.000e+00, 4.000e+00)'


Tests of the ``angle`` method::

    >>> Vector(0, 0).angle()
    0.0
    >>> Vector(1, 0).angle()
    0.0
    >>> epsilon = 10**-8
    >>> abs(Vector(0, 1).angle() - math.pi/2) < epsilon
    True
    >>> abs(Vector(1, 1).angle() - math.pi/4) < epsilon
    True


Tests of ``format()`` with polar coordinates:

    >>> format(Vector(1, 1), 'p')  # doctest:+ELLIPSIS
    '<1.414213..., 0.785398...>'
    >>> format(Vector(1, 1), '.3ep')
    '<1.414e+00, 7.854e-01>'
    >>> format(Vector(1, 1), '0.5fp')
    '<1.41421, 0.78540>'

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

# BEGIN VECTOR_V3_SLOTS
class Vector:
    __slots__ = ('__x', '__y')

    typecode = 'd'

    # methods follow (omitted in book listing)
# END VECTOR_V3_SLOTS

    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __iter__(self):
        return (i for i in (self.x, self.y))  # <6>

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
