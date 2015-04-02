# adapted from Alex Martelli's example in "Re-learning Python"
# http://www.aleax.it/Python/accu04_Relearn_Python_alex.pdf
# (slide 41) Ex: lines-by-word file index


"""Build a map word -> list-of-line-numbers"""

import sys
import re

NONWORD_RE = re.compile('\W+')

idx = {}
with open(sys.argv[1], encoding='utf-8') as fp:
    for n, line in enumerate(fp, 1):
        for word in NONWORD_RE.split(line):
            if word.strip():
                idx.setdefault(word, []).append(n)

# print in alphabetical order
for word in sorted(idx, key=str.upper):
    print(word, idx[word])
