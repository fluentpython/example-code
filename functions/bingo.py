"""
# BEGIN BINGO_DEMO

>>> bingo = BingoCage(range(3))
>>> bingo()
2
>>> bingo()
0
>>> callable(bingo)
True
# END BINGO_DEMO

"""

# BEGIN BINGO

import random

class BingoCage:

    def __init__(self, items):
        self._items = list(items)  # <1>
        random.shuffle(self._items)  # <2>

    def __call__(self):
        if not self._items:  # <3>
            raise IndexError('pop from empty BingoCage')
        return self._items.pop()

# END BINGO
