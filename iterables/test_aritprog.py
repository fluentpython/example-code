"""
Demonstrate difference between Arithmetic Progression calculated
as a series of increments accumulating errors versus one addition
and one multiplication.
"""

from fractions import Fraction
from aritprog_v3 import ArithmeticProgression as APv3
from aritprog_v4 import ArithmeticProgression as APv4

ap3 = iter(APv3(1, .1))
ap4 = iter(APv4(1, .1))
ap_frac = iter(APv4(Fraction(1, 1), Fraction(1, 10)))
epsilon = 10**-10
iteration = 0
delta = next(ap3) - next(ap4)
frac = next(ap_frac)
while abs(delta) <= epsilon:
    delta = next(ap3) - next(ap4)
    frac = next(ap_frac)
    iteration +=1

print('iteration: {}\tfraction: {}\tepsilon: {}\tdelta: {}'.
      format(iteration, frac, epsilon, delta))
