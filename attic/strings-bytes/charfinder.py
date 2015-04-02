#!/usr/bin/env python
from unicodedata import name
import sys

if len(sys.argv) > 1:
    query = sys.argv[1:]
else:
    query = input('search words: ').split()

query = [s.upper() for s in query]

count = 0
for i in range(20, sys.maxunicode):
    car = chr(i)
    descr = name(car, None)
    if descr is None:
        continue
    words = descr.split()
    if all(word in words for word in query):
        print('{i:5d} {i:04x} {car:^5} {descr}'.format(**locals()))
        count += 1

print('{0} character(s) found'.format(count))
