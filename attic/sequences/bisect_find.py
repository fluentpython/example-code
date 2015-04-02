
"""
    >>> bisect_find([], 1)
    -1
    >>> import array
    >>> import random
    >>> SIZE = 10
    >>> my_array = array.array('l', range(0, SIZE, 2))
    >>> random.seed(42)
    >>> for i in range(SIZE):
    ...     print(i, bisect_find(my_array, i))
    0 0
    1 -1
    2 1
    3 -1
    4 2
    5 -1
    6 3
    7 -1
    8 4
    9 -1
"""

from bisect import bisect

def bisect_find(seq, item):
    left_pos = bisect(seq, item) - 1
    return left_pos if seq and seq[left_pos] == item else -1

