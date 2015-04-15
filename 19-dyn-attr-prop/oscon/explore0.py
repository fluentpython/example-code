"""
explore0.py: Script to explore the OSCON schedule feed

# BEGIN EXPLORE0_DEMO
    >>> from osconfeed import load
    >>> raw_feed = load()
    >>> feed = FrozenJSON(raw_feed)  # <1>
    >>> len(feed.Schedule.speakers)  # <2>
    357
    >>> sorted(feed.Schedule.keys())  # <3>
    ['conferences', 'events', 'speakers', 'venues']
    >>> for key, value in sorted(feed.Schedule.items()): # <4>
    ...     print('{:3} {}'.format(len(value), key))
    ...
      1 conferences
    484 events
    357 speakers
     53 venues
    >>> feed.Schedule.speakers[-1].name  # <5>
    'Carina C. Zona'
    >>> talk = feed.Schedule.events[40]
    >>> type(talk)  # <6>
    <class 'explore0.FrozenJSON'>
    >>> talk.name
    'There *Will* Be Bugs'
    >>> talk.speakers  # <7>
    [3471, 5199]
    >>> talk.flavor  # <8>
    Traceback (most recent call last):
      ...
    KeyError: 'flavor'

# END EXPLORE0_DEMO

"""

# BEGIN EXPLORE0
from collections import abc


class FrozenJSON:
    """A read-only façade for navigating a JSON-like object
       using attribute notation
    """

    def __init__(self, mapping):
        self.__data = dict(mapping)  # <1>

    def __getattr__(self, name):  # <2>
        if hasattr(self.__data, name):
            return getattr(self.__data, name)  # <3>
        else:
            return FrozenJSON.build(self.__data[name])  # <4>

    @classmethod
    def build(cls, obj):  # <5>
        if isinstance(obj, abc.Mapping):  # <6>
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):  # <7>
            return [cls.build(item) for item in obj]
        else:  # <8>
            return obj
# END EXPLORE0
