"""
explore2.py: Script to download and explore the OSCON schedule feed

    >>> raw_feed = load_json()
    >>> feed = FrozenJSON(raw_feed)
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
    >>> carina = feed.Schedule.speakers[-1]
    >>> carina.twitter
    'cczona'
    >>> feed.Schedule.events[40].name
    'There *Will* Be Bugs'
    >>> feed.Schedule.events[40].speakers
    [3471, 5199]

"""

from urllib.request import urlopen
import warnings
import os
import json
from collections import abc

URL = 'http://www.oreilly.com/pub/sc/osconfeed'
JSON_NAME = 'osconfeed.json'


def load_json():
    if not os.path.exists(JSON_NAME):
        msg = 'downloading {} to {}'.format(URL, JSON_NAME)
        warnings.warn(msg)
        with urlopen(URL) as remote, open(JSON_NAME, 'wb') as local:
            local.write(remote.read())

    with open(JSON_NAME) as fp:
        return json.load(fp)


class FrozenJSON:
    """A read-only façade for navigating a JSON-like object
       using attribute notation
    """

    def __new__(cls, arg):
        if isinstance(arg, abc.Mapping):
            return super().__new__(cls)
        elif isinstance(arg, abc.MutableSequence):
            return [FrozenJSON(item) for item in arg]
        else:
            return arg

    def __init__(self, mapping):
        self._data = dict(mapping)

    def __getattr__(self, name):
        if hasattr(self._data, name):
            return getattr(self._data, name)
        else:
            return FrozenJSON(self._data[name])
