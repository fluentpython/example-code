>>> def coroutine():
...     print('coroutine started')
...     x = yield
...     print('coroutine received: {!r}'.format(x))
...
>>> coro = coroutine()
>>> next(coro)
coroutine started
>>> coro.send(42)
coroutine received: 42
Traceback (most recent call last):
  ...
StopIteration
