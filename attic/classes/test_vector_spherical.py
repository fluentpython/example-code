"""
Test spherical coordinates in ``Vector`` class
"""

import sys
from vector_v5 import Vector

FIXTURE = 'spherical-coordinates.txt'
EPSILON = 10**-8

def parse_float_cells(cells):
    floats = []
    for cell in cells:
        try:
            floats.append(float(cell))
        except ValueError:
            continue
    return floats

def load_fixture(verbose=False):
    with open(FIXTURE, encoding='utf8') as text:
        for line in text:
            if line.startswith('#'):  # comment line
                continue
            cells = line.split('\t')
            cartesian = parse_float_cells(cells[:5])
            spherical = parse_float_cells(cells[5:])
            v = Vector(cartesian)
            if verbose:
                print(repr(v), '\t->', spherical)
            diff = abs(abs(v) - spherical[0])
            assert diff < EPSILON, 'expected {}, got {}'.format(spherical[0], abs(v))
            assert all(abs(av - af) < EPSILON for av, af in zip(v.angles(), spherical[1:])), (
                'expected {}, got {}'.format(spherical[1:], list(v.angles())))

if __name__=='__main__':
    load_fixture('-v' in sys.argv)
