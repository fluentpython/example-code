# BEGIN CORO_AVERAGER
"""
A coroutine to compute a running average

    >>> coro_avg = averager()  # <1>
    >>> next(coro_avg)  # <2>
    0.0
    >>> coro_avg.send(10)  # <3>
    10.0
    >>> coro_avg.send(30)
    20.0
    >>> coro_avg.send(5)
    15.0

"""

def averager():
    total = average = 0.0
    count = 0
    while True:
        term = yield average  # <4>
        total += term
        count += 1
        average = total/count
# END CORO_AVERAGER
