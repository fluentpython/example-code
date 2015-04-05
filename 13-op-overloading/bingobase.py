"""
===============
BingoCage tests
===============


Create and load instance from iterable::

    >>> balls = list(range(3))
    >>> globe = BingoCage(balls)
    >>> len(globe)
    3


Pop and collect balls::

    >>> picks = []
    >>> picks.append(globe.pop())
    >>> picks.append(globe.pop())
    >>> picks.append(globe.pop())


Check state and results::

    >>> len(globe)
    0
    >>> sorted(picks) == balls
    True


Reload::

    >>> globe.load(balls)
    >>> len(globe)
    3
    >>> picks = [globe.pop() for i in balls]
    >>> len(globe)
    0


Load and pop 20 balls to verify that the order has changed::

    >>> balls = list(range(20))
    >>> globe = BingoCage(balls)
    >>> picks = []
    >>> while globe:
    ...     picks.append(globe.pop())
    >>> len(picks) == len(balls)
    True
    >>> picks != balls
    True


Also check that the order is not simply reversed either::

    >>> picks[::-1] != balls
    True

Note: last 2 tests above each have 1 chance in 20! (factorial) of
failing even if the implementation is OK. 1/20!, or approximately
4.11e-19, is the probability of the 20 balls coming out, by chance,
in the exact order the were loaded.

Check that `LookupError` (or a subclass) is the exception thrown
when the device is empty::

    >>> globe = BingoCage([])
    >>> try:
    ...     globe.pop()
    ... except LookupError as exc:
    ...     print('OK')
    OK

"""

import random


class BingoCage():

    def __init__(self, iterable):
        self._balls = []
        self.load(iterable)

    def load(self, iterable):
        self._balls.extend(iterable)
        random.shuffle(self._balls)

    def __len__(self):
        return len(self._balls)

    def pop(self):
        return self._balls.pop()

    def __iter__(self):
        return reversed(self._balls)
