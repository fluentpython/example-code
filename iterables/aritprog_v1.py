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
        return ArithmeticProgressionIterator(self._numbers)


class ArithmeticProgressionIterator(abc.Iterator):

    def __init__(self, series):
        self._series = series
        self._index = 0

    def __next__(self):
        if self._index < len(self._series):
            item = self._series[self._index]
            self._index += 1
            return item
        else:
            raise StopIteration



