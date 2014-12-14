"""
Arithmetic progression class

    >>> ap = ArithmeticProgression(1, .5, 3)
    >>> list(ap)
    [1.0, 1.5, 2.0, 2.5]


"""

from collections import abc


class ArithmeticProgression:

    def __init__(self, begin, step, end):
        self.begin = begin
        self.step = step
        self.end = end

    def __iter__(self):
        return ArithmeticProgressionIterator(self)


class ArithmeticProgressionIterator(abc.Iterator):

    def __init__(self, arithmetic_progression):
        self._ap = arithmetic_progression
        self._index = 0

    def __next__(self):
        first = type(self._ap.begin + self._ap.step)(self._ap.begin)
        result = first + self._ap.step * self._index
        if result < self._ap.end:
            self._index += 1
            return result
        else:
            raise StopIteration
