"""
Demonstrate difference between Arithmetic Progression calculated
as a series of increments accumulating errors versus one addition
and one multiplication.
"""

from fractions import Fraction
from aritprog_v0 import ArithmeticProgression as APv0
from aritprog_v1 import ArithmeticProgression as APv1

if __name__ == '__main__':

    ap0 = iter(APv0(1, .1))
    ap1 = iter(APv1(1, .1))
    ap_frac = iter(APv1(Fraction(1, 1), Fraction(1, 10)))
    epsilon = 10**-10
    iteration = 0
    delta = next(ap0) - next(ap1)
    frac = next(ap_frac)
    while abs(delta) <= epsilon:
        delta = next(ap0) - next(ap1)
        frac = next(ap_frac)
        iteration +=1

    print('iteration: {}\tfraction: {}\tepsilon: {}\tdelta: {}'.
          format(iteration, frac, epsilon, delta))
