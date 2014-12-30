"""
Spreadsheet example adapted from Raymond Hettinger's `recipe`__

__ http://code.activestate.com/recipes/355045-spreadsheet/

Demonstration::

    >>> from math import sin, pi
    >>> ss = Spreadsheet(sin=sin, pi=pi)
    >>> ss['a1'] = '-5'
    >>> ss['a2'] = 'a1*6'
    >>> ss['a3'] = 'a2*7'
    >>> ss['a3']
    -210
    >>> ss['b1'] = 'sin(pi/4)'
    >>> ss['b1']  # doctest:+ELLIPSIS
    0.707106781186...
    >>> ss.getformula('b1')
    'sin(pi/4)'
    >>> ss['c1'] = 'abs(a2)'
    >>> ss['c1']
    30
    >>> ss['d1'] = '3*'
    >>> ss['d1']
    Traceback (most recent call last):
      ...
    SyntaxError: unexpected EOF while parsing
"""


class Spreadsheet:

    def __init__(self, **tools):
        self._cells = {}
        self._tools = tools

    def __setitem__(self, key, formula):
        self._cells[key] = formula

    def getformula(self, key):
        return self._cells[key]

    def __getitem__(self, key):
        return eval(self._cells[key], self._tools, self)
