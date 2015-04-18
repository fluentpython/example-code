import asyncio
import sys
import contextlib

@asyncio.coroutine
def show_remaining(dots_task):
    remaining = 5
    while remaining:
        print('Remaining: ', remaining)
        sys.stdout.flush()
        yield from asyncio.sleep(1)
        remaining -= 1
    dots_task.cancel()
    print()

@asyncio.coroutine
def dots():
    while True:
        print('.', sep='', end='')
        sys.stdout.flush()
        yield from asyncio.sleep(.1)

def main():
    with contextlib.closing(asyncio.get_event_loop()) as loop:
        dots_task = asyncio.Task(dots())
        coros = [show_remaining(dots_task), dots_task]
        loop.run_until_complete(asyncio.wait(coros))

if __name__ == '__main__':
    main()
