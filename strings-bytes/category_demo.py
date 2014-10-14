import sys
import unicodedata

categories = set()

for i in range(sys.maxunicode):
    char = chr(i)
    name = unicodedata.name(char, None)
    if name is None:
        continue
    cat = unicodedata.category(char)
    if cat[0] not in categories:
        print('U+%04x' % i, char.center(6),
              cat, name, sep='\t')
        categories.add(cat[0])
