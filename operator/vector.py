"""

The `+` operator produces a `Vector` result.

    >>> v1 = Vector(2, 4)
    >>> v2 = Vector(2, 1)
    >>> v1 + v2
    Vector(4, 5)

We can also implemement the `*` operator to perform scalar multiplication
or elementwise multiplication.

    >>> v = Vector(3, 4)
    >>> abs(v)
    5.0
    >>> v * 3
    Vector(9, 12)
    >>> abs(v * 3)
    15.0
    >>> v25 = Vector(2, 5)
    >>> v71 = Vector(7, 1)
    >>> v71 * v25
    Vector(14, 5)

A vector can be used in a boolean context, where it will be considered
_falsy_ if it has magnitude zero, otherwise it is _truthy_::

    >>> bool(v)
    True
    >>> bool(Vector(0, 0))
    False

Vectors can have n-dimensions::

    >>> v3 = Vector(1, 2, 3)
    >>> len(v3)
    3
    >>> v3
    Vector(1, 2, 3)
    >>> abs(v3)  # doctest:+ELLIPSIS
    3.74165738...
    >>> v3 + Vector(4, 5, 6)
    Vector(5, 7, 9)
    >>> v3 * 5
    Vector(5, 10, 15)
    >>> v2 + v3
    Traceback (most recent call last):
      ...
    ValueError: Addition applies only to vectors of equal dimensions.


The `repr` of a Vector is produced with the help of the `reprlib.repr`
function, limiting the size of the output string:

    >>> Vector(*range(100))
    Vector(0, 1, 2, 3, 4, 5, ...)


Dot product is a scalar: the sum of the products of the corresponding
components of two vectors.

    >>> v25 = Vector(2, 5)
    >>> v71 = Vector(7, 1)
    >>> v25.dot(v71)
    19
    >>> Vector(1, 2, 3).dot(Vector(4, 5, 6))
    32
    >>> Vector(1, 2, 3).dot(Vector(-2, 0, 5))
    13


As described in PEP 465, starting with Python 3.5, `__matmul__` is
the special method for the new ``@`` operator, to be used the dot
product of vectors or matrix multiplication (as opposed to ``*``
which is intended for scalar or elementwise multiplication):

    >>> # skip these tests on Python < 3.5
    >>> v25 @ v71  # doctest:+SKIP
    19
    >>> v71 * v25
    Vector(14, 5)
    >>> Vector(1, 2, 3) @ Vector(-2, 0, 5)    # doctest:+SKIP
    13

"""

# BEGIN VECTOR_OPS
import math
import numbers
import reprlib

EQ_DIMENSIONS_MSG = '%s applies only to vectors of equal dimensions.'

class Vector:
    """An n-dimensional vector"""

    def __init__(self, *components):  # <1>
        self._components = tuple(components)  # <2>

    def __repr__(self):
        return 'Vector' + (reprlib.repr(self._components))  # <3>

    def __iter__(self):
        return iter(self._components)  # <4>

    def __abs__(self):
        return math.sqrt(sum(comp*comp for comp in self)) # <5>

    def __len__(self):
        return len(self._components)  # <6>

    def __add__(self, other):
        if len(self) != len(other):
            raise ValueError(EQ_DIMENSIONS_MSG % 'Addition')
        return Vector(*(a+b for a, b in zip(self, other)))  # <7>

    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            return Vector(*(comp*other for comp in self))  # <8>
        else:
            return self.elementwise_mul(other)  # <9>

    def elementwise_mul(self, other):
        if len(self) != len(other):
            raise ValueError(EQ_DIMENSIONS_MSG %
                             'Elementwise multiplication')
        return Vector(*(a*b for a, b in zip(self, other)))  # <10>

    def __bool__(self):
        return any(self)  # <11>

    def dot(self, other):
        if len(self) != len(other):
            raise ValueError(EQ_DIMENSIONS_MSG %
                             'Dot product')
        return sum(a*b for a, b in zip(self, other))  # <12>

    __matmul__ = dot  # support @ operator in Python 3.5

# END VECTOR_OPS
