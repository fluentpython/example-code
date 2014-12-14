===========================================
Tests for arithmetic progression generators
===========================================

Tests with built-in numeric types::

    >>> ap = aritprog_gen(1, .5, 3)
    >>> list(ap)
    [1.0, 1.5, 2.0, 2.5]
    >>> ap = aritprog_gen(0, 1/3, 1)
    >>> list(ap)
    [0.0, 0.3333333333333333, 0.6666666666666666]


Tests with standard library numeric types::

    >>> from fractions import Fraction
    >>> ap = aritprog_gen(0, Fraction(1, 3), 1)
    >>> list(ap)
    [Fraction(0, 1), Fraction(1, 3), Fraction(2, 3)]
    >>> from decimal import Decimal
    >>> ap = aritprog_gen(0, Decimal('.1'), .3)
    >>> list(ap)
    [Decimal('0'), Decimal('0.1'), Decimal('0.2')]


Test producing an empty series::

    >>> ap = aritprog_gen(0, 1, 0)
    >>> list(ap)
    []
