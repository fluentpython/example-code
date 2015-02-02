>>> def coro():
...     print 'iniciando corotina...'
...     while True:
...         x = yield
...         print 'recebido: ', x
...         if x == -1: break
...     print 'terminando corotina.'
...
>>> c = coro()
>>> next(c)
iniciando corotina...
>>> c.send(7)
recebido:  7
>>> c.send(3)
recebido:  3
>>> c.send(10)
recebido:  10
>>> c.send(-1)
recebido:  -1
terminando corotina.
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
>>>
