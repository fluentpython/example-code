"""
Experiments with futures
"""

from time import sleep, strftime
from concurrent import futures

def display(*args):
    print(strftime('[%H:%M:%S]'), end=' ')
    print(*args)


def loiter(n):
    msg = '{}loiter({}): doing nothing for {}s...'
    display(msg.format('\t'*n, n, n))
    sleep(n)
    msg = '{}loiter({}): done.'
    display(msg.format('\t'*n, n))
    return n * 10


def demo_submit():
    executor = futures.ThreadPoolExecutor(3)
    future_list = [executor.submit(loiter, n) for n in range(5)]
    display('done?', [future.done() for future in future_list])
    display('Waiting for results...')
    for i, result in enumerate(future.result() for future in future_list):
        display('result[{}]: {}'.format(i, result))


demo_submit()
