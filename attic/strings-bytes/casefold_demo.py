import sys
from unicodedata import name, normalize

changed = 0
assigned = 0
for i in range(sys.maxunicode):
    char = chr(i)
    char_name = name(char, None)
    if char_name is None:
        continue
    cf = char.casefold()
    assigned += 1
    if cf != char.lower():
        cf_display = ' '.join(cf)
        cf_names = ';'.join(name(c) for c in cf)
        changed += 1
        print('%4d U+%04x' % (changed, i), char, cf_display, char_name + ' -> ' + cf_names, sep='\t')

print(changed, '/', assigned, '=', changed/assigned*100)
