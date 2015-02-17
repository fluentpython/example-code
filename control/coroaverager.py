"""
Closing a generator raises ``GeneratorExit`` at the pending ``yield``

    >>> coro_avg = averager()
    >>> next(coro_avg)
    0.0
    >>> coro_avg.send(10)
    10.0
    >>> coro_avg.send(20)
    15.0
    >>> coro_avg.send(30)
    20.0
    >>> coro_avg.close()
    -> total: 60.0  average: 20.0  terms: 3


Other exceptions propagate to the caller:

    >>> coro_avg = averager()
    >>> next(coro_avg)
    0.0
    >>> coro_avg.send(10)
    10.0
    >>> coro_avg.send('spam')
    Traceback (most recent call last):
      ...
    TypeError: unsupported operand type(s) for +=: 'float' and 'str'


"""

# BEGIN CORO_AVERAGER
def averager():
    total = average = 0.0
    count = 0
    try:
        while True:
            term = yield average
            total += term
            count += 1
            average = total/count
    except GeneratorExit:
        msg = '-> total: {}  average: {}  terms: {}'
        print(msg.format(total, average, count))
# END CORO_AVERAGER
