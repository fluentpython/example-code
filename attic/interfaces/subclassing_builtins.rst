====================================
Subclassing built-in caveats
====================================

::

    >>> class D1(dict):
    ...     def __getitem__(self, key):
    ...         return 42
    ...
    >>> d1 = D1(a='foo')
    >>> d1
    {'a': 'foo'}
    >>> d1['a']
    42
    >>> d1.get('a')
    'foo'

::

    >>> class D2(dict):
    ...     def get(self, key):
    ...         return 42
    ...
    >>> d2 = D2(a='foo')
    >>> d2
    {'a': 'foo'}
    >>> d2['a']
    'foo'
    >>> d2.get('a')
    42
