# clockdec2o_demo.py

"""
>>> pythagoras(3, 4)        # doctest: +ELLIPSIS
[0.0...s] pythagoras(3, 4) -> 5.0
5.0
>>> pythagoras(9, h=15)     # doctest: +ELLIPSIS
[0.0...s] pythagoras(9, h=15) -> 12.0
12.0

"""
import time
import math
from clockdeco2 import clock


@clock
def pythagoras(a, b=None, h=None):
    if b is None and h is None:
        raise TypeError('must provide second leg (b) or hypotenuse (h)')
    if h is None:
        return math.sqrt(a*a + b*b)
    else:
        return math.sqrt(h*h - a*a)


if __name__=='__main__':
    print('*' * 40, 'Calling pythagoras(3, 4)')
    pythagoras(3, 4)
    print('*' * 40, 'Calling pythagoras(9, h=15)')
    pythagoras(9, h=15)
