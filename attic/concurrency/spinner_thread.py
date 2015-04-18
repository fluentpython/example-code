# spinner_thread.py
# adapted from spinner_proc.py to use threads

import sys
import time
import threading

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
    spinner = threading.Thread(
        None, spinner_func, args=('Please wait...', 'thinking!'))
    spinner.daemon = True
    spinner.start()

    long_computation()
    print('\nComputation done')
