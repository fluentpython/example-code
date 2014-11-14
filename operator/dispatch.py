"""
Experiments with infix operator dispatch

    >>> kadd = KnowsAdd()
    >>> kadd + 1
    (<KnowsAdd object>, 1)
    >>> kadd * 1

"""


class KnowsAdd:
    def __add__(self, other):
        return self, other
    def __repr__(self):
        return '<{} object>'.format(type(self).__name__)

