
====================================
Differences between PyPy and CPython
====================================

Note: this is an excerpt from the `PyPy`_ documentation. On Nov. 19, 2014 I ran this test on PyPy 2.4.0 and PyPy3 2.4.0 and the result was not as described, but was the same as with CPython: 'foo'.

.. _PyPy: http://pypy.readthedocs.org/en/latest/cpython_differences.html#subclasses-of-built-in-types

Subclasses of built-in types
----------------------------

Officially, CPython has no rule at all for when exactly
overridden method of subclasses of built-in types get
implicitly called or not.  As an approximation, these methods
are never called by other built-in methods of the same object.
For example, an overridden ``__getitem__()`` in a subclass of
``dict`` will not be called by e.g. the built-in ``get()``
method.

The above is true both in CPython and in PyPy.  Differences
can occur about whether a built-in function or method will
call an overridden method of *another* object than ``self``.
In PyPy, they are generally always called, whereas not in
CPython.  For example, in PyPy, ``dict1.update(dict2)``
considers that ``dict2`` is just a general mapping object, and
will thus call overridden ``keys()``  and ``__getitem__()``
methods on it.  So the following code prints ``42`` on PyPy
but ``foo`` on CPython::

    >>> class D(dict):
    ...     def __getitem__(self, key):
    ...         return 42
    ...
    >>>
    >>> d1 = {}
    >>> d2 = D(a='foo')
    >>> d1.update(d2)
    >>> print(d1['a'])
    42
