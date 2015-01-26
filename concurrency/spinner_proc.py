# spinner_proc.py
# credit: Example by Michele Simionato in comp lang python.
# source:
# http://python-3-patterns-idioms-test.readthedocs.org/en/latest/CoroutinesAndConcurrency.html

import sys
import time
import multiprocessing

DELAY = 0.1
DISPLAY = '|/-\\'


def spinner_func(before='', after=''):
    write, flush = sys.stdout.write, sys.stdout.flush
    while True:
        for char in DISPLAY:
            msg = '{} {} {}'.format(before, char, after)
            write(msg)
            flush()
            write('\x08' * len(msg))
            time.sleep(DELAY)


def long_computation():
    # emulate a long computation
    time.sleep(3)

if __name__ == '__main__':
    spinner = multiprocessing.Process(
        None, spinner_func, args=('Please wait ... ', ' thinking!'))
    spinner.start()

    try:
        long_computation()
        print('\nComputation done')
    finally:
        spinner.terminate()
