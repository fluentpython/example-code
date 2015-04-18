# BEGIN LOTTERY_BLOWER

import random

from tombola import Tombola


class LotteryBlower(Tombola):

    def __init__(self, iterable):
        self._balls = list(iterable)  # <1>

    def load(self, iterable):
        self._balls.extend(iterable)

    def pick(self):
        try:
            position = random.randrange(len(self._balls))  # <2>
        except ValueError:
            raise LookupError('pick from empty BingoCage')
        return self._balls.pop(position)  # <3>

    def loaded(self):  # <4>
        return bool(self._balls)

    def inspect(self):  # <5>
        return tuple(sorted(self._balls))


# END LOTTERY_BLOWER
