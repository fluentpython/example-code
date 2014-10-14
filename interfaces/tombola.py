from abc import ABCMeta, abstractmethod


class Tombola(metaclass=ABCMeta):  # <1>

    @abstractmethod
    def __init__(self, iterable):  # <2>
        raise NotImplementedError

    @abstractmethod
    def load(self):
        raise NotImplementedError

    @abstractmethod
    def pop(self):
        raise NotImplementedError

    def loaded(self):  # <3>
        try:
            item = self.pop()
        except LookupError:
            return False
        else:
            self.load([item])  # put it back
            return True
