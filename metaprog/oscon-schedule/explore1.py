"""
explore1.py: Script to explore the OSCON schedule feed

# BEGIN EXPLORE1_DEMO
    >>> from osconfeed import load
    >>> raw_feed = load()
    >>> feed = FrozenJSON(raw_feed)  # <1>
    >>> len(feed.Schedule.speakers)  # <2>
    357
    >>> sorted(feed.Schedule.keys())  # <3>
    ['conferences', 'events', 'speakers', 'venues']
    >>> feed.Schedule.speakers[-1].name  # <4>
    'Carina C. Zona'
    >>> talk = feed.Schedule.events[40]  # <5>
    >>> talk.name
    'There *Will* Be Bugs'
    >>> talk.speakers  # <6>
    [3471, 5199]
    >>> talk.flavor  # <7>
    Traceback (most recent call last):
      ...
    KeyError: 'flavor'

# END EXPLORE1_DEMO
"""

# BEGIN EXPLORE1
from collections import abc


class FrozenJSON:
    """A read-only façade for navigating a JSON-like object
       using attribute notation
    """

    def __init__(self, mapping):
        self._data = dict(mapping)  # <1>

    def __getattr__(self, name):  # <2>
        if hasattr(self._data, name):
            return getattr(self._data, name)  # <3>
        else:
            return FrozenJSON.build(self._data[name])  # <4>

    @classmethod
    def build(cls, obj):  # <5>
        if isinstance(obj, abc.Mapping):  # <6>
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):  # <7>
            return [cls.build(item) for item in obj]
        else:  # <8>
            return obj
# END EXPLORE1
