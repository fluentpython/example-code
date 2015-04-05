"""
======================
AddableBingoCage tests
======================


Tests for __add__ and __iadd__:

    >>> vowels = 'AEIOU'
    >>> globe = AddableBingoCage(vowels)
    >>> len(globe)
    5
    >>> globe.pop() in vowels
    True
    >>> len(globe)
    4
    >>> globe2 = AddableBingoCage('XYZ')
    >>> globe3 = globe + globe2
    >>> len(globe3)
    7
    >>> void = globe + [10, 20]
    Traceback (most recent call last):
      ...
    TypeError: unsupported operand type(s) for +: 'AddableBingoCage' and 'list'


Tests for __add__ and __iadd__:

    >>> globe_orig = globe
    >>> len(globe)
    4
    >>> globe += globe2
    >>> len(globe)
    7
    >>> globe += [10, 20]
    >>> len(globe)
    9
    >>> globe is globe_orig
    True

"""

# BEGIN ADDABLE_BINGO
import itertools  # <1>
from bingobase import BingoCage


class AddableBingoCage(BingoCage):  # <2>

    def __add__(self, other):
        if isinstance(other, AddableBingoCage):  # <3>
            return AddableBingoCage(itertools.chain(self, other))  # <4>
        else:
            return NotImplemented

    def __iadd__(self, other):
        self.load(other)  # <5>
        return self  # <6>
# END ADDABLE_BINGO
