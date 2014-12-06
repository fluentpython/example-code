"""
Variation of ``tombola.Tombola`` implementing ``__subclasshook__``.

Tests with simple classes::

    >>> Tombola.__subclasshook__(object)
    NotImplemented
    >>> class Complete:
    ...     def __init__(): pass
    ...     def load(): pass
    ...     def pick(): pass
    ...     def loaded(): pass
    ...
    >>> Tombola.__subclasshook__(Complete)
    True
    >>> issubclass(Complete, Tombola)

"""


from abc import ABC, abstractmethod
from inspect import getmembers, isfunction


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

    @classmethod
    def __subclasshook__(cls, other_cls):
        if cls is Tombola:
            interface_names = function_names(cls)
            found_names = set()
            for a_cls in other_cls.__mro__:
                found_names |= function_names(a_cls)
            if found_names >= interface_names:
                return True
        return NotImplemented


def function_names(obj):
    return {name for name, _ in getmembers(obj, isfunction)}
