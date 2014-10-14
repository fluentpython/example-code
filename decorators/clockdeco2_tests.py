"""
>>> f_empty()
[0.0...s] f_empty() -> None
>>> f_args('spam', 3)
[0.0...s] f_args('spam', 3) -> 'spamspamspam'
'spamspamspam'
>>> snooze(1234)
[1...s] snooze(1234) -> None
>>> average(1, 2, 3)
[0.0...s] average(1, 2, 3) -> 2.0
2.0
>>> average(*range(10**3))
[0.0...s] average(0, 1, ..., 999) -> 499.5
499.5
>>> factorial(10)
[0.000...s] factorial(1) -> 1
[0.000...s] factorial(2) -> 2
[0.000...s] factorial(3) -> 6
[0.000...s] factorial(4) -> 24
[0.000...s] factorial(5) -> 120
[0.000...s] factorial(6) -> 720
[0.000...s] factorial(7) -> 5040
[0.000...s] factorial(8) -> 40320
[0.000...s] factorial(9) -> 362880
[0.000...s] factorial(10) -> 3628800
3628800
>>> fibonacci(1)
[0.000...s] fibonacci(1) -> 1
1
>>> fibonacci(5)
[0.000...s] fibonacci(1) -> 1
[0.000...s] fibonacci(0) -> 0
[0.000...s] fibonacci(1) -> 1
[0.000...s] fibonacci(2) -> 1
[0.000...s] fibonacci(3) -> 2
[0.000...s] fibonacci(0) -> 0
[0.000...s] fibonacci(1) -> 1
[0.000...s] fibonacci(2) -> 1
[0.000...s] fibonacci(1) -> 1
[0.000...s] fibonacci(0) -> 0
[0.000...s] fibonacci(1) -> 1
[0.000...s] fibonacci(2) -> 1
[0.000...s] fibonacci(3) -> 2
[0.000...s] fibonacci(4) -> 3
[0.000...s] fibonacci(5) -> 5
5
>>> f_kwargs(3, 5, d='spam', c='eggs')
[0.0...s] f_kwargs(3, 5, c='eggs', d='spam') -> 15
15
>>> f_args.__name__
'f_args'
>>> f_kwargs.__name__
'f_kwargs'
"""

import time

from clockdeco2 import clock

@clock
def f_empty():
    pass

@clock
def f_args(a, b):
    return a*b

@clock
def snooze(milis):
    time.sleep(milis/1000)

@clock
def average(*args):
    return sum(args) / len(args)

@clock
def factorial(n):
    return 1 if n < 2 else n*factorial(n-1)

@clock
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)

@clock
def f_kwargs(a, b, c=1, d='eggs'):
    from time import sleep
    sleep(0.001)
    return a*b



import doctest
doctest.testmod(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
