import unicodedata

encodings = 'ascii latin1 cp1252 cp437 gb2312 utf-8 utf-16le'.split()

widths = {encoding:1 for encoding in encodings[:-3]}
widths.update(zip(encodings[-3:], (2, 4, 4)))

chars = sorted([
    'A',  # \u0041 : LATIN CAPITAL LETTER A
    '¿',  # \u00bf : INVERTED QUESTION MARK
    'Ã',  # \u00c3 : LATIN CAPITAL LETTER A WITH TILDE
    'á',  # \u00e1 : LATIN SMALL LETTER A WITH ACUTE
    'Ω',  # \u03a9 : GREEK CAPITAL LETTER OMEGA
    'µ',
    'Ц',
    '€',  # \u20ac : EURO SIGN
    '“',
    '┌',
    '气',
    '氣', # \u6c23 : CJK UNIFIED IDEOGRAPH-6C23
    '𝄞',  # \u1d11e : MUSICAL SYMBOL G CLEF
])

callout1_code = 0x278a  # ➊   DINGBAT NEGATIVE CIRCLED SANS-SERIF DIGIT ONE

missing_mark = '*'

def list_chars():
    for char in chars:
        print('%r,  # \\u%04x : %s' % (char, ord(char), unicodedata.name(char)))

def show_encodings():
    print(end='\t\t')
    for encoding in encodings:
        print(encoding.ljust(widths[encoding] * 2), end='\t')
    print()

    for lineno, char in enumerate(chars):
        codepoint = 'U+{:04X}'.format(ord(char))
        print(char, codepoint, sep='\t', end='\t')
        for encoding in encodings:
            try:
                bytes = char.encode(encoding)
                dump = ' '.join('%02X' % byte for byte in bytes)
            except UnicodeEncodeError:
                dump = missing_mark
            dump = dump.ljust(widths[encoding] * 2)
            print(dump, end='\t')
        # print(chr(callout1_code + lineno))
        print(unicodedata.name(char))
        # print()

#list_chars()
show_encodings()
