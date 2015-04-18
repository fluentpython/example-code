import os
from time import sleep, time

from parallelize import parallelize, per_item

DELAY = .2

def loiter(serial, delay):
    pid = os.getpid()
    print('%2d pid = %d' % (serial, pid))
    sleep(delay)
    return pid

t0 = time()

results = []
for i in parallelize(range(15), fork=per_item):
    res = loiter(i, DELAY)
    results.append(res)

print('Processes used: ', list(set(results)))

print('### Elapsed time: %0.2f' % (time() - t0))
