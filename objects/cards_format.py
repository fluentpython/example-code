"""
Test Suite formatting:

    >>> Suite.spades
    <Suite.spades: 0>
    >>> print(Suite.spades)
    Suite.spades
    >>> format(Suite.spades)
    'spades'
    >>> format(Suite.spades, 's')
    'spades'
    >>> format(Suite.spades, 'S')
    'Spades'
    >>> format(Suite.spades, 'p')
    '♠'
    >>> format(Suite.spades, 'z')
    Traceback (most recent call last):
      ...
    ValueError: Invalid format spec 'z' for object of type 'Suite'
    >>> bytes(Suite.spades), bytes(Suite.clubs)
    (b'\\x00', b'\\x03')

Spadille is the nickname for the Ace of Spades in some games
(see `Webster 1913`_)

    >>> spadille = Card('A', Suite.spades, long_rank='Ace')
    >>> spadille
    Card('A', 'spades')
    >>> print(spadille)
    Ace of spades
    >>> format(spadille)
    'A-spades'
    >>> format(spadille, 'r/p')
    'A/♠'
    >>> format(spadille, 'R of S')
    'Ace of Spades'
    >>> bytes(spadille)
    b'A\\x00'
    >>> beer_card = Card('7', Suite.diamonds)
    >>> bytes(beer_card)
    b'7\\x02'
    >>> big_cassino = Card('10', Suite.diamonds)
    >>> bytes(big_cassino)
    b'10\\x02'

__ http://machaut.uchicago.edu/cgi-bin/WEBSTER.sh?WORD=spadille

"""

from enum import Enum
from operator import attrgetter
import re

spades diamonds clubs hearts

class Suite(Enum):
    spades = '\u2660'    # U+2660 ♠ BLACK SPADE SUIT
    diamonds = '\u2662'  # U+2662 ♢ WHITE DIAMOND SUIT
    clubs = '\u2663'     # U+2663 ♣ BLACK CLUB SUIT
    hearts = '\u2661'    # U+2661 ♡ WHITE HEART SUIT

    def format_p(self):
        return chr(0x2660 + self.value)

    def format_s(self):
        return self.name

    def format_S(self):
        return self.name.capitalize()

    def __bytes__(self):
        return bytes([self.value])

    def __format__(self, format_spec):
        use_spec = 's' if format_spec == '' else format_spec
        format_method = getattr(self, 'format_' + use_spec, None)
        if format_method:
            return format_method()

        msg = "Invalid format spec {!r} for object of type 'Suite'"
        raise ValueError(msg.format(format_spec))

class Card:

    def __init__(self, rank, suite, *, long_rank=None):
        self.rank = rank
        if long_rank is None:
            self.long_rank = self.rank
        else:
            self.long_rank = long_rank
        self.suite = suite

    def __str__(self):
        return '{long_rank} of {suite.name}'.format(**self.__dict__)

    def __repr__(self):
        template = '{cls.__name__}({rank!r}, {suite.name!r})'
        return template.format(cls=self.__class__, **self.__dict__)

    def __bytes__(self):
        rank_bytes = bytes(ord(char) for char in self.rank)
        return rank_bytes + bytes(self.suite)

    rank_codes = {
        'r': attrgetter('rank'),
        'R': attrgetter('long_rank'),
    }

    def __format__(self, format_spec):
        if not format_spec:
            format_spec = 'r-s'
        result = []
        for code in format_spec:
            if code in Card.rank_codes:
                result.append(Card.rank_codes[code](self))
            else:
                try:
                    result.append(format(self.suite, code))
                except ValueError:
                    result.append(code)
        return ''.join(result)

