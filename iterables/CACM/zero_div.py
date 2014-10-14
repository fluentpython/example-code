"""
Erik Meijer. 2014. The curse of the excluded middle.
Commun. ACM 57, 6 (June 2014), 50-55. DOI=10.1145/2605176
http://doi.acm.org/10.1145/2605176
"""

l = range(10, -1, -1)
try:
    res = (1/x for x in l)
except ZeroDivisionError:
    res = []

for z in res:
    print(z)
