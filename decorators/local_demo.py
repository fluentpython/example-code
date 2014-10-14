"""
>>> f1(3)
>>> b = 8
>>> f1(3)
a = 3
b = 8
>>> f2(3)
Traceback (most recent call last):
  ...
UnboundLocalError: local variable 'b' referenced before assignment
>>> f3(3)
a = 3
b = 7
b = 6
>>> b = -5
>>> ff = f4()
>>> ff(3)
a = 3
b = 11
b = 6
>>> print('b =', b)
b = -5
"""

def f1(a):
    print('a =', a)
    print('b =', b)

def f2(a):
    print('a =', a)
    print('b =', b)
    b = a * 10
    print('b =', b)

def f3(a):
    global b
    print('a =', a)
    print('b =', b)
    b = a * 10
    print('b =', b)

def f3b(a):
    nonlocal b
    print('a =', a)
    print('b =', b)
    b = a * 10
    print('b =', b)

def f4():
    b = 11
    def f5(a):
        nonlocal b
        print('a =', a)
        print('b =', b)
        b = a * 2
        print('b =', b)
    return f5

import doctest
doctest.testmod(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)



