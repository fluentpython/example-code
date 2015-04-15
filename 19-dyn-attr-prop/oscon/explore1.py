"""
explore1.py: Script to explore the OSCON schedule feed

    >>> from osconfeed import load
    >>> raw_feed = load()
    >>> feed = FrozenJSON(raw_feed)
    >>> len(feed.Schedule.speakers)
    357
    >>> sorted(feed.Schedule.keys())
    ['conferences', 'events', 'speakers', 'venues']
    >>> for key, value in sorted(feed.Schedule.items()):
    ...     print('{:3} {}'.format(len(value), key))
    ...
      1 conferences
    484 events
    357 speakers
     53 venues
    >>> feed.Schedule.speakers[-1].name
    'Carina C. Zona'
    >>> talk = feed.Schedule.events[40]
    >>> type(talk)
    <class 'explore1.FrozenJSON'>
    >>> talk.name
    'There *Will* Be Bugs'
    >>> talk.speakers
    [3471, 5199]
    >>> talk.flavor
    Traceback (most recent call last):
      ...
    KeyError: 'flavor'

Handle keywords by appending a `_`.

# BEGIN EXPLORE1_DEMO

    >>> grad = FrozenJSON({'name': 'Jim Bo', 'class': 1982})
    >>> grad.name
    'Jim Bo'
    >>> grad.class_
    1991

# END EXPLORE1_DEMO

"""

from collections import abc
import keyword


class FrozenJSON:
    """A read-only façade for navigating a JSON-like object
       using attribute notation
    """

# BEGIN EXPLORE1
    def __init__(self, mapping):
        self.__data = {}
        for key, value in mapping.items():
            if keyword.iskeyword(key):  # <1>
                key += '_'
            self.__data[key] = value
# END EXPLORE1

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return FrozenJSON.build(self.__data[name])

    @classmethod
    def build(cls, obj):
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
        else:  # <8>
            return obj

