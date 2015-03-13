"""
An experiment showing that ``asyncio.Future`` is an iterable (it
implements `__iter__`) designed to be used with ``yield from``.

Priming the future returns itself. After the result of the future
is set, next iteration produces the result as the ``value`` attribute
of ``StopIteration``.

Sample run::

    $ python3 future_yield.py
    a, future:      <Future pending> 0x66514c
    b, prime_res:   <Future pending> 0x66514c
    b, exc.value:   42

"""

import asyncio

@asyncio.coroutine
def a(future):
    print('a, future:\t', future, hex(id(future)))
    res = yield from future
    return res

def b():
    future = asyncio.Future()
    coro = a(future)
    prime_res = next(coro)
    print('b, prime_res:\t', prime_res, hex(id(future)))
    # If next(coro) is called again before the result of
    # the future is set, we get:
    #   AssertionError: yield from wasn't used with future
    #result = next(coro)  # uncomment to see AssertionError
    future.set_result(42)
    try:
        next(coro)
    except StopIteration as exc:
        print('b, exc.value:\t', exc.value)

b()
