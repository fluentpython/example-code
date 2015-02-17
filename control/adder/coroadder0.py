"""
Closing a generator raises ``GeneratorExit`` at the pending ``yield``

    >>> adder = adder_coro()
    >>> next(adder)
    0
    >>> adder.send(10)
    10
    >>> adder.send(20)
    30
    >>> adder.send(30)
    60
    >>> adder.close()
    -> total: 60  terms: 3  average: 20.0


Other exceptions propagate to the caller:

    >>> adder = adder_coro()
    >>> next(adder)
    0
    >>> adder.send(10)
    10
    >>> adder.send('spam')
    Traceback (most recent call last):
      ...
    TypeError: unsupported operand type(s) for +=: 'int' and 'str'


"""

def adder_coro(initial=0):
    total = initial
    count = 0
    try:
        while True:
            term = yield total
            total += term
            count += 1
    except GeneratorExit:
        average = total / count
        msg = '-> total: {}  terms: {}  average: {}'
        print(msg.format(total, count, average))
