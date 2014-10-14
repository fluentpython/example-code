import sys
from unicodedata import name

for i in range(sys.maxunicode):
    char = chr(i)
    try:
        char_name = name(char)
    except ValueError: # no such name
        continue
    flags = []
    flags.append('D' if char.isdigit() else '')
    flags.append('N' if char.isnumeric() else '')
    if any(flags):
        flags = '\t'.join(flags)
        print('U+%04x' % i, char, flags, char_name, sep='\t')
