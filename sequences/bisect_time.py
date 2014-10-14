"""
bisect_time.py
"""

import timeit

SETUP = '''
SIZE = 10**6
import array
import random
from bisect_find import bisect_find
random.seed(42)
haystack = [random.randrange(SIZE)*2 for i in range(SIZE)]
needles = [random.choice(haystack) + i % 2 for i in range(20)]
'''

BISECT = '''
print('bisect:', end=' ')
for n in needles:
    print(bisect_find(haystack, n), end=' ')
print()
'''

SORT = '''
print('    in:', end=' ')
for n in needles:
    print(int(n in haystack), end=' ')
print()
'''

print(min(timeit.Timer(BISECT, SETUP).repeat(7, 1)))
print(min(timeit.Timer(SORT, SETUP).repeat(7, 1)))
