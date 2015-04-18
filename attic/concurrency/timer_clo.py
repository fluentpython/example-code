import sys
import asyncio

def make_show_remaining(seconds):
    remaining = seconds

    def show_remaining(loop):
        nonlocal remaining
        print('Remaining: ', remaining)
        remaining -= 1
        if remaining:
            loop.call_later(1, show_remaining, loop)
        else:
            loop.stop()

    return show_remaining
    
    
def main(seconds=5):
    seconds = int(seconds)
    loop = asyncio.get_event_loop()
    try:
        loop.call_soon(make_show_remaining(seconds), loop)
        loop.run_forever()
    finally:
        loop.close()

if __name__ == '__main__':
    main(*sys.argv[1:])
