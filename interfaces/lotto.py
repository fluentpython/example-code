import random

from tombola import Tombola


class LotteryBlower(Tombola):

    def __init__(self, iterable):
        self.randomizer = random.SystemRandom()  # <1>
        self.clear()
        self.load(iterable)

    def clear(self):
        self._balls = []

    def load(self, iterable):
        self._balls.extend(iterable)
        self.randomizer.shuffle(self._balls)  # <2>

    def pop(self):
        return self._balls.pop()  # <3>

    def loaded(self):  # <4>
        return len(self._balls) > 0
