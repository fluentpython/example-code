import random

from tombola import Tombola


class BingoCage(Tombola):  # <1>

    def __init__(self, items):
        self._balls = list(items)  # <2>

    def load(self, items):
        self._balls.extend(items)

    def pick(self):
        try:
            position = random.randrange(len(self._balls))  # <3>
        except ValueError:
            raise LookupError('pop from empty BingoCage')
        return self._balls.pop(position)  # <4>
