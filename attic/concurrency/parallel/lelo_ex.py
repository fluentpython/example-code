import os
from time import sleep, time

from lelo import parallel

DELAY = .2

@parallel
def loiter(serial, delay):
    pid = os.getpid()
    print('%2d pid = %d' % (serial, pid))
    sleep(delay)
    return pid

t0 = time()

results = []
for i in range(15):
    res = loiter(i, DELAY)
    results.append(res)

print('Processes used: ', list(set(results)))

print('### Elapsed time: %0.2f' % (time() - t0))
