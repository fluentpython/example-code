"""
A multi-dimensional ``MultiVector`` class, take 1

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
    MultiVector([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    >>> abs(v7)  # doctest:+ELLIPSIS
    9.53939201...

Test of ``.__bytes__`` and ``.frombytes()`` methods::

    >>> v1 = MultiVector([3, 4, 5])
    >>> v1_clone = MultiVector.frombytes(bytes(v1))
    >>> v1_clone
    MultiVector([3.0, 4.0, 5.0])
    >>> v1 == v1_clone
    True

Tests of hashing::

    >>> v1 = MultiVector([3, 4])
    >>> v2 = MultiVector([3.1, 4.2])
    >>> v3 = MultiVector([3, 4, 5])
    >>> v4 = MultiVector(range(10))
    >>> hash(v1), hash(v2), hash(v3), hash(v4)
    (7, 384307168202284039, 2, 1)
    >>> len(set([v1, v2, v3, v4]))
    4


"""

from array import array
import math
import functools
import operator


class MultiVector:
    typecode = 'd'

    def __init__(self, components):
        self._components = array(MultiVector.typecode, components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        components = ', '.join(repr(x) for x in self)
        return 'MultiVector([{}])'.format(components)

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

    @classmethod
    def frombytes(cls, octets):
        memv = memoryview(octets).cast(cls.typecode)
        return cls(memv)
