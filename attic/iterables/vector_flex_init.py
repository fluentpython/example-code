"""
A more flexible `__init__` for the Vector class

A Vector can be built from an iterable:

    >>> Vector([10, 20, 30])
    Vector(10, 20, 30)
    >>> Vector(range(1, 5))
    Vector(1, 2, 3, 4)

Or from two more arguments:

    >>> Vector(100, 200)
    Vector(100, 200)
    >>> Vector(1, 2, 3, 4, 5)
    Vector(1, 2, 3, 4, 5)

One-dimensional vectors are not supported:

    >>> Vector(99)
    Traceback (most recent call last):
       ...
    TypeError: Vector() takes one iterable argument or at least 2 scalar arguments

"""

import reprlib


class Vector:
    """An n-dimensional vector"""

    def __init__(self, first, *rest):  # <1>
        if rest:
            self._components = (first,) + tuple(rest)  # <3>
        else:
            try:
                self._components = tuple(first)  # <2>
            except TypeError:
                raise TypeError('Vector() takes one iterable argument or at least 2 scalar arguments')

    def __repr__(self):
        return 'Vector' + reprlib.repr(self._components)
