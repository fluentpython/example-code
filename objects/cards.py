"""

Spadille is the nickname for the Ace of Spades in some games
(see `Webster 1913`_)

    >>> beer_card = Card('7', Suite.diamonds)
    >>> beer_card
    Card('7', Suite.diamonds)
    >>> spadille = Card('A', Suite.spades, long_rank='Ace')
    >>> spadille
    Card('A', Suite.spades)
    >>> print(spadille)
    Ace of spades
    >>> bytes(spadille)
    b'A\\x01'
    >>> charles = Card('K', Suite.hearts)
    >>> bytes(charles)
    b'K\\x04'
    >>> big_cassino = Card('10', Suite.diamonds)
    >>> bytes(big_cassino)
    b'T\\x02'

__ http://machaut.uchicago.edu/cgi-bin/WEBSTER.sh?WORD=spadille

"""

from enum import Enum

Suite = Enum('Suite', 'spades diamonds clubs hearts')

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
        constructor = '{cls.__name__}({args})'
        args = '{0.rank!r}, Suite.{0.suite.name}'.format(self)
        return constructor.format(cls=self.__class__, args=args)

    def __bytes__(self):
        if self.rank == '10':
            rank_byte = b'T'
        else:
            rank_byte = bytes([ord(self.rank)])
        return rank_byte + bytes([self.suite.value])
