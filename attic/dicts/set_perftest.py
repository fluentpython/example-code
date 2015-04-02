"""
Set performance test
"""

import timeit

SETUP = '''
import array
selected = array.array('d')
with open('selected.arr', 'rb') as fp:
    selected.fromfile(fp, {size})
haystack = {type}(selected)
# print('haystack: %10d' % len(haystack), end='  ')
needles = array.array('d')
with open('not_selected.arr', 'rb') as fp:
    needles.fromfile(fp, 500)
needles.extend(selected[:500])
needles = set(needles)
# print(' needles: %10d' % len(needles), end='  ')
'''

tests = [
('FOR_LOOP_TEST', '''
found = 0
for n in needles:
    if n in haystack:
        found += 1
assert found == 500
'''),
('SET_&_TEST', '''
found = len(needles & haystack)
assert found == 500
'''
)]

MAX_EXPONENT = 7
for collection_type in 'dict.fromkeys set list'.split():
    if collection_type == 'set':
        available_tests = tests
    else:
        available_tests = tests[:1]
    for test_name, test in available_tests:
        print('*' * 25, collection_type, test_name)
        for n in range(3, MAX_EXPONENT + 1):
            size = 10**n
            setup = SETUP.format(type=collection_type, size=size)
            tt = timeit.repeat(stmt=test, setup=setup, repeat=5, number=1)
            print('|{:{}d}|{:9.6f}'.format(size, MAX_EXPONENT + 1, min(tt)))
