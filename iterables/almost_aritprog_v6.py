"""
Arithmetic progression generator function.

This is almost correct. The only problem is that the first
item in the series may not be of the same type as the rest,
an this may be important to the user::

    >>> ap = aritprog_gen(1, .5, 3)
    >>> list(ap)
    [1, 1.5, 2.0, 2.5]
    >>> ap = aritprog_gen(0, 1/3, 1)
    >>> list(ap)
    [0, 0.3333333333333333, 0.6666666666666666]
    >>> from fractions import Fraction
    >>> ap = aritprog_gen(0, Fraction(1, 3), 1)
    >>> list(ap)
    [0, Fraction(1, 3), Fraction(2, 3)]
    >>> from decimal import Decimal
    >>> ap = aritprog_gen(0, Decimal('.1'), .3)
    >>> list(ap)
    [0, Decimal('0.1'), Decimal('0.2')]


"""

# BEGIN ALMOST_ARITPROG_ITERTOOLS
import itertools


def aritprog_gen(begin, step, end=None):
    ap_gen = itertools.count(begin, step)
    if end is not None:
        ap_gen = itertools.takewhile(lambda n: n < end, ap_gen)
    return ap_gen
# END ALMOST_ARITPROG_ITERTOOLS
