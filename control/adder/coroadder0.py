"""
Closing a generator raises ``GeneratorExit`` at the pending ``yield``

    >>> adder = adder_coro()
    >>> next(adder)
    >>> adder.send(10)
    >>> adder.send(20)
    >>> adder.send(30)
    >>> adder.close()
    -> total: 60  terms: 3  average: 20.0


Other exceptions propagate to the caller:

    >>> adder = adder_coro()
    >>> next(adder)
    >>> adder.send(10)
    >>> adder.send('spam')
    Traceback (most recent call last):
      ...
    TypeError: unsupported operand type(s) for +=: 'int' and 'str'


"""

def adder_coro(initial=0):
    total = initial
    num_terms = 0
    try:
        while True:
            term = yield
            total += term
            num_terms += 1
    except GeneratorExit:
        average = total / num_terms
        msg = '-> total: {}  terms: {}  average: {}'
        print(msg.format(total, num_terms, average))
