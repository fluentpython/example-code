import asyncio

def show_remaining(loop):
    if not hasattr(show_remaining, 'remaining'):
        show_remaining.remaining = 5

    print('Remaining: ', show_remaining.remaining)
    show_remaining.remaining -= 1
    if show_remaining.remaining:
        loop.call_later(1, show_remaining, loop)
    else:
        loop.stop()

def main():
    loop = asyncio.get_event_loop()
    try:
        loop.call_soon(show_remaining, loop)
        loop.run_forever()
    finally:
        loop.close()

if __name__ == '__main__':
    main()
