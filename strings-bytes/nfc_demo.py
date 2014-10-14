import sys
from unicodedata import name, normalize

for i in range(sys.maxunicode):
    char = chr(i)
    char_name = name(char, None)
    if char_name is None:
        continue
    nfc = normalize('NFC', char)
    if nfc == char:
        continue
    if len(nfc) > 1:
        nfc_display = ' '.join(nfc)
        print('U+%04x' % i, char, nfc_display, char_name, sep='\t')
