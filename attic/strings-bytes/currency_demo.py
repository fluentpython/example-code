import sys
import unicodedata

for i in range(sys.maxunicode):
    char = chr(i)
    if unicodedata.category(char) == 'Sc':
        name = unicodedata.name(char, None)
        print('U+%04x' % i, char.center(6),
              name, sep='\t')
