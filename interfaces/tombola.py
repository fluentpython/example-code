from abc import ABC, abstractmethod


class Tombola(ABC):  # <1>

    @abstractmethod
    def __init__(self, iterable):  # <2>
        """New instance is loaded from an iterable."""

    @abstractmethod
    def load(self, iterable):
        """Add items from an iterable."""

    @abstractmethod
    def pick(self):  # <3>
        """Remove item at random, returning it.

        This method should raise `LookupError` when the instance is empty.
        """

    def loaded(self):  # <4>
        try:
            item = self.pick()
        except LookupError:
            return False
        else:
            self.load([item])  # put it back
            return True
