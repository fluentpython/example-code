"""
Experiment with ``ThreadPoolExecutor.map``
"""
# BEGIN EXECUTOR_MAP
from time import sleep, strftime
from concurrent import futures


def display(*args):  # <1>
    print(strftime('[%H:%M:%S]'), end=' ')
    print(*args)


def loiter(n):  # <2>
    msg = '{}loiter({}): doing nothing for {}s...'
    display(msg.format('\t'*n, n, n))
    sleep(n)
    msg = '{}loiter({}): done.'
    display(msg.format('\t'*n, n))
    return n * 10  # <3>


def main():
    display('Script starting.')
    executor = futures.ThreadPoolExecutor(max_workers=3)  # <4>
    results = executor.map(loiter, range(5))  # <5>
    display('results:', results)  # <6>.
    display('Waiting for individual results:')
    for i, result in enumerate(results):  # <7>
        display('result {}: {}'.format(i, result))


main()
# END EXECUTOR_MAP
