==============================
Tests for a ``Sentence`` class
==============================

A ``Sentence`` is built from a ``str`` and allows iteration
word-by-word.

::
    >>> s = Sentence('The time has come')
    >>> s
    Sentence('The time has come')
    >>> list(s)
    ['The', 'time', 'has', 'come']
    >>> it = iter(s)
    >>> next(it)
    'The'
    >>> next(it)
    'time'
    >>> next(it)
    'has'
    >>> next(it)
    'come'
    >>> next(it)
    Traceback (most recent call last):
      ...
    StopIteration


Any punctuation is skipped while iterating::

    >>> s = Sentence('"The time has come," the Walrus said,')
    >>> s
    Sentence('"The time ha... Walrus said,')
    >>> list(s)
    ['The', 'time', 'has', 'come', 'the', 'Walrus', 'said']


White space including line breaks are also ignored::

    >>> s = Sentence('''"The time has come," the Walrus said,
    ...                 "To talk of many things:"''')
    >>> s
    Sentence('"The time ha...many things:"')
    >>> list(s)
    ['The', 'time', 'has', 'come', 'the', 'Walrus', 'said', 'To', 'talk', 'of', 'many', 'things']


Accented Latin characters are also recognized as word characters::

    >>> s = Sentence('Agora vou-me. Ou me vão?')
    >>> s
    Sentence('Agora vou-me. Ou me vão?')
    >>> list(s)
    ['Agora', 'vou', 'me', 'Ou', 'me', 'vão']
