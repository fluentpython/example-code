# BEGIN NUMERICS_DEMO
import unicodedata
import re

re_digit = re.compile(r'\d')

sample = '1\xbc\xb2\u0969\u136b\u216b\u2466\u2480\u3285'

for char in sample:
    print('U+%04x' % ord(char),                       # <1>
          char.center(6),                             # <2>
          're_dig' if re_digit.match(char) else '-',  # <3>
          'isdig' if char.isdigit() else '-',         # <4>
          'isnum' if char.isnumeric() else '-',       # <5>
          format(unicodedata.numeric(char), '5.2f'),  # <6>
          unicodedata.name(char),                     # <7>
          sep='\t')
# END NUMERICS_DEMO
