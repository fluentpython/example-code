"""
Arithmetic progression class

    >>> ap = ArithmeticProgression(1, .5, 3)
    >>> list(ap)
    [1.0, 1.5, 2.0, 2.5]


"""

import array
from collections import abc

class ArithmeticProgression:

    def __init__(self, begin, step, end):
        self.begin = begin
        self.step = step
        self.end = end
        self._build()

    def _build(self):
        self._numbers = array.array('d')
        n = self.begin
        while n < self.end:
            self._numbers.append(n)
            n += self.step

    def __iter__(self):
        for item in self._numbers:
            yield item
        return StopIteration
