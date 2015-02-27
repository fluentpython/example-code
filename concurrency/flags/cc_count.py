
from collections import Counter
from operator import itemgetter
from string import ascii_uppercase

with open('country-codes.tab') as fp:
    ct = Counter()
    for line in fp:
        if line.startswith('#'):
            continue
        cc, _, _ = line.split('\t')
        ct[cc[0]] += 1
        print(cc, end=' ')

for key, value in sorted(ct.items(), key=itemgetter(1), reverse=True):
    print(key, value)

print('Total:', sum(ct.values()))
print('Missing:', ', '.join(set(ascii_uppercase) - ct.keys()))
