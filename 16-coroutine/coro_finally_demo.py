"""
Second coroutine closing demonstration::

    >>> fin_coro = demo_finally()
    >>> next(fin_coro)
    -> coroutine started
    >>> fin_coro.send(11)
    -> coroutine received: 11
    >>> fin_coro.send(22)
    -> coroutine received: 22
    >>> fin_coro.close()
    -> coroutine ending


Second coroutine not handling exception::

    >>> fin_coro = demo_finally()
    >>> next(fin_coro)
    -> coroutine started
    >>> fin_coro.send(11)
    -> coroutine received: 11
    >>> fin_coro.throw(ZeroDivisionError)  # doctest: +SKIP
    -> coroutine ending
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "coro_exception_demos.py", line 109, in demo_finally
        print('-> coroutine received: {!r}'.format(x))
    ZeroDivisionError


The last test above must be skipped because the output '-> coroutine ending'
is not detected by doctest, which raises a false error. However, if you
run this file as shown below, you'll see that output "leak" into standard
output::


    $ python3 -m doctest coro_exception_demos.py
    -> coroutine ending

"""


# BEGIN EX_CORO_FINALLY
class DemoException(Exception):
    """An exception type for the demonstration."""


def demo_finally():
    print('-> coroutine started')
    try:
        while True:
            try:
                x = yield
            except DemoException:
                print('*** DemoException handled. Continuing...')
            else:
                print('-> coroutine received: {!r}'.format(x))
    finally:
        print('-> coroutine ending')

# END EX_CORO_FINALLY
