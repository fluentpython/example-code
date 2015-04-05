import os
from parallelize import parallelize
from time import sleep, time

print('one process:')
t0 = time()
for i in range(12):
    print('%2d pid = %d' % (i, os.getpid()))
    sleep(.2)
print('elapsed time: %0.2f' % (time() - t0))

print()

print('several processes:')
t0 = time()
for i in parallelize(range(12)):
    print('%2d pid = %d' % (i, os.getpid()))
    sleep(.2)
print('elapsed time: %0.2f' % (time() - t0))
