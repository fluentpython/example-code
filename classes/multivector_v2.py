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

# BEGIN MULTIVECTOR_V2_DEMO

    >>> v7 = MultiVector(range(7))
    >>> v7[-1]  # <1>
    6.0
    >>> v7[1:4]  # <2>
    MultiVector([1.0, 2.0, 3.0])
    >>> v7[-1:]  # <3>
    MultiVector([6.0])
    >>> v7[1,2]  # <4>
    Traceback (most recent call last):
      ...
    TypeError: MultiVector indices must be integers

# END MULTIVECTOR_V2_DEMO

"""

from array import array
import reprlib
import math


class MultiVector:
    typecode = 'd'

    def __init__(self, components):
        self._components = array(MultiVector.typecode, components)

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

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))

    def __bool__(self):
        return bool(abs(self))

# BEGIN MULTIVECTOR_V2
    def __len__(self):
        return len(self._components)

    def __getitem__(self, index):
        cls = type(self)  # <1>
        if isinstance(index, slice):
            return cls(self._components[index])  # <2>
        elif isinstance(index, int):
            return self._components[index]  # <3>
        else:
            msg = '{cls.__name__} indices must be integers'
            raise TypeError(msg.format(cls=cls))  # <4>
# END MULTIVECTOR_V2

    @classmethod
    def frombytes(cls, octets):
        memv = memoryview(octets).cast(cls.typecode)
        return cls(memv)
