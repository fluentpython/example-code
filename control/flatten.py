"""

    >>> items = [1, 2, [3, 4, [5, 6], 7], 8]
    >>> flatten(items)
    <generator object flatten at 0x73bd9c>
    >>> list(flatten(items))
    [1, 2, 3, 4, 5, 6, 7, 8]
    >>> mixed_bag = [1, 'spam', 2, [3, 'eggs', 4], {'x': 1, 'y': 2}]
    >>> list(flatten(mixed_bag))
    [1, 'spam', 2, 3, 'eggs', 4, 'y', 'x']
"""


from collections import Iterable

def flatten(items):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            yield from flatten(x)
        else:
            yield x
