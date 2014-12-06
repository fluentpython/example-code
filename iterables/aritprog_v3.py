"""
Arithmetic progression class

    >>> ap = ArithmeticProgression(1, .5, 3)
    >>> list(ap)
    [1.0, 1.5, 2.0, 2.5]


"""

import array
from collections import abc

class ArithmeticProgression:

    def __init__(self, begin, step, end=None):
        self.begin = float(begin)
        self.step = float(step)
        self.end = end  # None -> "infinite" series

    def __iter__(self):
        result = self.begin
        forever = self.end is None
        while forever or result < self.end:
            yield result
            result += self.step
        raise StopIteration
