"""
A coroutine to compute a running average

    >>> coro_avg = averager()  # <1>
    >>> from inspect import getgeneratorstate
    >>> getgeneratorstate(coro_avg)  # <2>
    'GEN_SUSPENDED'
    >>> coro_avg.send(10)  # <3>
    10.0
    >>> coro_avg.send(30)
    20.0
    >>> coro_avg.send(5)
    15.0

"""

from collections import namedtuple

Result = namedtuple('Result', 'count total average')

def averager():  # <6>
    total = average = 0.0
    count = 0
    try:
        while True:
            term = yield average
            total += term
            count += 1
            average = total/count
    finally:
        return Result(count, total, average)
