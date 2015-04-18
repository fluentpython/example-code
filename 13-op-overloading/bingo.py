# BEGIN TOMBOLA_BINGO

import random

from tombola import Tombola


class BingoCage(Tombola):  # <1>

    def __init__(self, items):
        self._randomizer = random.SystemRandom()  # <2>
        self._items = []
        self.load(items)  # <3>

    def load(self, items):
        self._items.extend(items)
        self._randomizer.shuffle(self._items)  # <4>

    def pick(self):  # <5>
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')

    def __call__(self):  # <7>
        self.pick()

# END TOMBOLA_BINGO
