"""
A coroutine to compute a running average.

Testing ``averager`` by itself::

# BEGIN RETURNING_AVERAGER_DEMO1

    >>> coro_avg = averager()
    >>> next(coro_avg)
    >>> coro_avg.send(10)  # <1>
    >>> coro_avg.send(30)
    >>> coro_avg.send(6.5)
    >>> coro_avg.send(None)  # <2>
    Traceback (most recent call last):
       ...
    StopIteration: Result(count=3, average=15.5)

# END RETURNING_AVERAGER_DEMO1

Catching `StopIteration` to extract the value returned by
the coroutine::

# BEGIN RETURNING_AVERAGER_DEMO2

    >>> coro_avg = averager()
    >>> next(coro_avg)
    >>> coro_avg.send(10)
    >>> coro_avg.send(30)
    >>> coro_avg.send(6.5)
    >>> try:
    ...     coro_avg.send(None)
    ... except StopIteration as exc:
    ...     result = exc.value
    ...
    >>> result
    Result(count=3, average=15.5)

# END RETURNING_AVERAGER_DEMO2


"""

# BEGIN RETURNING_AVERAGER
from collections import namedtuple

Result = namedtuple('Result', 'count average')


def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break  # <1>
        total += term
        count += 1
        average = total/count
    return Result(count, average)  # <2>
# END RETURNING_AVERAGER
