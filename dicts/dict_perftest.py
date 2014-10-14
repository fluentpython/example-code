"""
Dict performance test
"""

import timeit

SETUP = '''
import array
selected = array.array('d')
with open('selected.arr', 'rb') as fp:
    selected.fromfile(fp, {size})
haystack = dict((n, n.as_integer_ratio()) for n in selected)
print('haystack: %10d' % len(haystack), end='  ')
needles = array.array('d')
with open('not_selected.arr', 'rb') as fp:
    needles.fromfile(fp, 500)
needles.extend(selected[:500])
# print(' needles: %10d' % len(needles), end='  ')
'''

TEST = '''
found = 0
for n in needles:
    if n in haystack:
        found += 1
# print('  found: %10d' % found)
'''

MAX_EXPONENT = 7
for n in range(3, MAX_EXPONENT + 1):
    size = 10**n
    setup = SETUP.format(size=size)
    tt = timeit.repeat(stmt=TEST, setup=setup, repeat=5, number=1)
    print('|{:{}d}|{:f}'.format(size, MAX_EXPONENT + 1, min(tt)))
