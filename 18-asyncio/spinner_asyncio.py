# spinner_asyncio.py

# credits: Example by Luciano Ramalho inspired by
# Michele Simionato's multiprocessing example in the python-list:
# https://mail.python.org/pipermail/python-list/2009-February/538048.html

# BEGIN SPINNER_ASYNCIO
import asyncio
import itertools
import sys


@asyncio.coroutine
def spin(msg):  # <1>
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            yield from asyncio.sleep(.1)  # <2>
        except asyncio.CancelledError:  # <3>
            break
    write(' ' * len(status) + '\x08' * len(status))


@asyncio.coroutine
def slow_computation():  # <4>
    # fake computation waiting a long time for I/O
    yield from asyncio.sleep(3)  # <5>
    return 42


@asyncio.coroutine
def supervisor():  # <6>
    spinner = asyncio.async(spin('thinking!'))  # <7>
    print('spinner object:', spinner)  # <8>
    result = yield from slow_computation()  # <9>
    spinner.cancel()  # <10>
    return result


def main():
    loop = asyncio.get_event_loop()  # <11>
    result = loop.run_until_complete(supervisor())  # <12>
    loop.close()
    print('Answer:', result)


if __name__ == '__main__':
    main()
# END SPINNER_ASYNCIO
