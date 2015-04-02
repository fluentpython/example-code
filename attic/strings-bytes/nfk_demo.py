import sys
from unicodedata import name, normalize

for i in range(sys.maxunicode):
    char = chr(i)
    char_name = name(char, None)
    if char_name is None:
        continue
    kc = normalize('NFKC', char)
    if kc == char:
        continue
    kd = normalize('NFKD', char)
    if kc != kd:
        kc_display = ' '.join(kc)
        kd_display = ' '.join(kd)
        print('U+%04x' % i, char, kc_display, kd_display, char_name, sep='\t')
