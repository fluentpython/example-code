# spinner_await.py

# credits: Example by Luciano Ramalho inspired by
# Michele Simionato's multiprocessing example in the python-list:
# https://mail.python.org/pipermail/python-list/2009-February/538048.html

# BEGIN SPINNER_AWAIT
import asyncio
import itertools
import sys


async def spin(msg):  # <1>
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            await asyncio.sleep(.1)  # <3>
        except asyncio.CancelledError:  # <4>
            break
    write(' ' * len(status) + '\x08' * len(status))


async def slow_function():  # <5>
    # pretend waiting a long time for I/O
    await asyncio.sleep(3)  # <6>
    return 42


async def supervisor():  # <7>
    spinner = asyncio.ensure_future(spin('thinking!'))  # <8>
    print('spinner object:', spinner)  # <9>
    result = await slow_function()  # <10>
    spinner.cancel()  # <11>
    return result


def main():
    loop = asyncio.get_event_loop()  # <12>
    result = loop.run_until_complete(supervisor())  # <13>
    loop.close()
    print('Answer:', result)


if __name__ == '__main__':
    main()
# END SPINNER_AWAIT
