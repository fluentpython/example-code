"""
A multi-dimensional ``MultiVector`` class, take 2

A ``MultiVector`` is built from an iterable of numbers::

    >>> MultiVector([3.1, 4.2])
    MultiVector([3.1, 4.2])
    >>> MultiVector((3, 4, 5))
    MultiVector([3.0, 4.0, 5.0])
    >>> MultiVector(range(10))
    MultiVector([0.0, 1.0, 2.0, 3.0, 4.0, ...])


Tests with 2-dimensions (same results as ``vector_v1.py``)::

    >>> v1 = MultiVector([3, 4])
    >>> x, y = v1
    >>> x, y
    (3.0, 4.0)
    >>> v1
    MultiVector([3.0, 4.0])
    >>> v1_clone = eval(repr(v1))
    >>> v1 == v1_clone
    True
    >>> print(v1)
    (3.0, 4.0)
    >>> octets = bytes(v1)
    >>> octets
    b'\\x00\\x00\\x00\\x00\\x00\\x00\\x08@\\x00\\x00\\x00\\x00\\x00\\x00\\x10@'
    >>> abs(v1)
    5.0
    >>> bool(v1), bool(MultiVector([0, 0]))
    (True, False)


Test of ``.frombytes()`` class method:

    >>> v1_clone = MultiVector.frombytes(bytes(v1))
    >>> v1_clone
    MultiVector([3.0, 4.0])
    >>> v1 == v1_clone
    True


Tests with 3-dimensions::

    >>> v1 = MultiVector([3, 4, 5])
    >>> x, y, z = v1
    >>> x, y, z
    (3.0, 4.0, 5.0)
    >>> v1
    MultiVector([3.0, 4.0, 5.0])
    >>> v1_clone = eval(repr(v1))
    >>> v1 == v1_clone
    True
    >>> print(v1)
    (3.0, 4.0, 5.0)
    >>> abs(v1)  # doctest:+ELLIPSIS
    7.071067811...
    >>> bool(v1), bool(MultiVector([0, 0, 0]))
    (True, False)


Tests with many dimensions::

    >>> v7 = MultiVector(range(7))
    >>> v7
    MultiVector([0.0, 1.0, 2.0, 3.0, 4.0, ...])
    >>> abs(v7)  # doctest:+ELLIPSIS
    9.53939201...


Test of ``.__bytes__`` and ``.frombytes()`` methods::

    >>> v1 = MultiVector([3, 4, 5])
    >>> v1_clone = MultiVector.frombytes(bytes(v1))
    >>> v1_clone
    MultiVector([3.0, 4.0, 5.0])
    >>> v1 == v1_clone
    True


Tests of sequence behavior::

    >>> v1 = MultiVector([3, 4, 5])
    >>> len(v1)
    3
    >>> v1[0], v1[len(v1)-1], v1[-1]
    (3.0, 5.0, 5.0)


Test of slicing::

    >>> v7 = MultiVector(range(7))
    >>> v7[-1]
    6.0
    >>> v7[1:4]
    MultiVector([1.0, 2.0, 3.0])
    >>> v7[-1:]
    MultiVector([6.0])
    >>> v7[1,2]
    Traceback (most recent call last):
      ...
    TypeError: MultiVector indices must be integers


Tests of dynamic attribute access::

    >>> v7 = MultiVector(range(10))
    >>> v7.x
    0.0
    >>> v7.y, v7.z, v7.t, v7.u, v7.v, v7.w
    (1.0, 2.0, 3.0, 4.0, 5.0, 6.0)

Dynamic attribute lookup failures::

    >>> v7.k
    Traceback (most recent call last):
      ...
    AttributeError: 'MultiVector' object has no attribute 'k'
    >>> v3 = MultiVector(range(3))
    >>> v3.t
    Traceback (most recent call last):
      ...
    AttributeError: 'MultiVector' object has no attribute 't'
    >>> v3.spam
    Traceback (most recent call last):
      ...
    AttributeError: 'MultiVector' object has no attribute 'spam'


Tests of hashing::

    >>> v1 = MultiVector([3, 4])
    >>> v2 = MultiVector([3.1, 4.2])
    >>> v3 = MultiVector([3, 4, 5])
    >>> v6 = MultiVector(range(6))
    >>> hash(v1), hash(v2), hash(v3), hash(v6)
    (7, 384307168202284039, 2, 1)
    >>> len(set([v1, v2, v3, v6]))
    4


Tests of ``format()`` with Cartesian coordinates in 2D:

    >>> v1 = MultiVector([3, 4])
    >>> format(v1)
    '(3.0, 4.0)'
    >>> format(v1, '.2f')
    '(3.00, 4.00)'
    >>> format(v1, '.3e')
    '(3.000e+00, 4.000e+00)'


Tests of ``format()`` with Cartesian coordinates in 3D and 7D:

    >>> v3 = MultiVector([3, 4, 5])
    >>> format(v3)
    '(3.0, 4.0, 5.0)'
    >>> format(MultiVector(range(7)))
    '(0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0)'


Tests of the ``angle`` method::

    >>> MultiVector([0, 0]).angle()
    0.0
    >>> MultiVector([1, 0]).angle()
    0.0
    >>> epsilon = 10**-8
    >>> abs(MultiVector([0, 1]).angle() - math.pi/2) < epsilon
    True
    >>> abs(MultiVector([1, 1]).angle() - math.pi/4) < epsilon
    True


Tests of ``format()`` with polar coordinates:

    >>> format(MultiVector([1, 1]), 'p')  # doctest:+ELLIPSIS
    '<1.414213..., 0.785398...>'
    >>> format(MultiVector([1, 1]), '.3ep')
    '<1.414e+00, 7.854e-01>'
    >>> format(MultiVector([1, 1]), '0.5fp')
    '<1.41421, 0.78540>'


"""

from array import array
import reprlib
import math
import functools
import operator


class MultiVector:
    typecode = 'd'

    def __init__(self, components):
        self._components = array(self.typecode, components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return 'MultiVector({})'.format(components)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return bytes(self._components)

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __hash__(self):
        hashes = (hash(x) for x in self)
        return functools.reduce(operator.xor, hashes)

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))

    def __bool__(self):
        return bool(abs(self))

    def __len__(self):
        return len(self._components)

    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._components[index])
        elif isinstance(index, int):
            return self._components[index]
        else:
            msg = '{.__name__} indices must be integers'
            raise TypeError(msg.format(cls))

    shortcut_names = 'xyztuvw'

    def __getattr__(self, name):
        cls = type(self)
        if len(name) == 1:
            pos = cls.shortcut_names.find(name)
            if 0 <= pos < len(self._components):
                return self._components[pos]
        msg = '{.__name__!r} object has no attribute {!r}'
        raise AttributeError(msg.format(cls, name))

    def angle(self):
        return math.atan2(self.y, self.x)  # <1>

    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('p'):
            fmt_spec = fmt_spec[:-1]
            coords = (abs(self), self.angle())
            outer_fmt = '<{}>'  # <2>
        else:
            coords = self
            outer_fmt = '({})'  # <3>
        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(', '.join(components))  # <4>

    @classmethod
    def frombytes(cls, octets):
        memv = memoryview(octets).cast(cls.typecode)
        return cls(memv)
