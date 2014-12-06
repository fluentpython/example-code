"""
Accumulator generator examples

http://www.paulgraham.com/accgen.html

    >>> f3 = foo(3)
    >>> f3(2)
    5
    >>> f3(2)
    7
    >>> f3(2)
    9


"""

class foo0:
    def __init__(self, n):
        self.n = n
    def __call__(self, i):
        self.n += i
        return self.n

def foo0(n):
    def bar(i):
        bar.s += i
        return bar.s
    bar.s = n
    return bar

def foo(n):
    def bar(i):
        nonlocal n
        n += i
        return n
    return bar
