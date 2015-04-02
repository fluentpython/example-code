
"""
    >>> bisect_in([], 1)
    False
    >>> import array
    >>> import random
    >>> SIZE = 10
    >>> my_array = array.array('l', range(0, SIZE, 2))
    >>> random.seed(42)
    >>> for i in range(SIZE):
    ...     print(i, bisect_in(my_array, i))
    0 True
    1 False
    2 True
    3 False
    4 True
    5 False
    6 True
    7 False
    8 True
    9 False
"""

from bisect import bisect

def bisect_in(seq, item):
    pos = bisect(seq, item)
    return seq[pos-1] == item if seq else False

