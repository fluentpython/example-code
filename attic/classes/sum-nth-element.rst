======================================
Pythonic way to sum n-th list element?
======================================

Examples inspired by Guy Middleton's question on Python-list, Fri Apr 18 22:21:08 CEST 2003. Message: https://mail.python.org/pipermail/python-list/2003-April/218568.html

Guy Middleton::

    >>> my_list = [[1, 2, 3], [40, 50, 60], [9, 8, 7]]
    >>> import functools as ft
    >>> ft.reduce(lambda a, b: a+b, [sub[1] for sub in my_list])
    60

LR::

    >>> ft.reduce(lambda a, b: a + b[1], my_list, 0)
    60

Fernando Perez::

    >>> import numpy as np
    >>> my_array = np.array(my_list)
    >>> np.sum(my_array[:, 1])
    60

Skip Montanaro::

    >>> import operator
    >>> ft.reduce(operator.add, [sub[1] for sub in my_list], 0)
    60
    >>> ft.reduce(operator.add, [sub[1] for sub in []])
    Traceback (most recent call last):
      ...
    TypeError: reduce() of empty sequence with no initial value
    >>> ft.reduce(operator.add, [sub[1] for sub in []], 0)
    0


Evan Simpson::

    >>> total = 0
    >>> for sub in my_list:
    ...     total += sub[1]
    >>> total
    60

Alex Martelli (``sum`` was added in Python 2.3, released July 9, 2003)::

    >>> sum([sub[1] for sub in my_list])
    60

After generator expressions (added in Python 2.4, November 30, 2004)::

    >>> sum(sub[1] for sub in my_list)
    60

If you want the sum of a list of items, you should write it in a way 
that looks like "the sum of a list of items", not in a way that looks 
like "loop over these items, maintain another variable t, perform a 
sequence of additions".  Why do we have high level languages if not to 
express our intentions at a higher level and let the language worry 
about what low-level operations are needed to implement it?

David Eppstein

Alex Martelli

https://mail.python.org/pipermail/python-list/2003-April/186311.html

"The sum" is so frequently needed that I wouldn't mind at all if
Python singled it out as a built-in.  But "reduce(operator.add, ..."
just isn't a great way to express it, in my opinion (and yet as an
old APL'er, and FP-liker, I _should_ like it -- but I don't).

https://mail.python.org/pipermail/python-list/2003-April/225323.html

Four years later, having coded a lot of Python, taught it widely,
written a lot about it, and so on, I've changed my mind: I now
think that reduce is more trouble than it's worth and Python
would be better off without it, if it was being designed from
scratch today -- it would not substantially reduce (:-) Python's 
power and WOULD substantially ease the teaching/&c task.  That's
not a strong-enough argument to REMOVE a builtin, of course, and
thus that's definitely NOT what I'm arguing for.  But I do suggest
avoiding reduce in most cases -- that's all.
