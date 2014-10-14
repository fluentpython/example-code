"""
Meijer, Erik - The Curse of the Excluded Middle
DOI:10.1145/2605176
CACM vol.57 no.06
"""

def less_than_30(n):
    check = n < 30
    print('%d < 30 : %s' % (n, check))
    return check

def more_than_20(n):
    check = n > 20
    print('%d > 20 : %s' % (n, check))
    return check

l = [1, 25, 40, 5, 23]
q0 = (n for n in l if less_than_30(n))
q1 = (n for n in q0 if more_than_20(n))

for n in q1:
    print('-> %d' % n)
