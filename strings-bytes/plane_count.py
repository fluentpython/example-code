import sys
from unicodedata import name, normalize

total_count = 0
bmp_count = 0

for i in range(sys.maxunicode):
    char = chr(i)
    char_name = name(char, None)
    if char_name is None:
        continue
    total_count += 1
    if i <= 0xffff:
        bmp_count += 1

print(total_count, bmp_count, bmp_count/total_count, bmp_count/total_count*100)
