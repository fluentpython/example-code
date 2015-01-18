import asyncio

@asyncio.coroutine
def show_remaining():
    remaining = 5
    while remaining:
        print('Remaining: ', remaining)
        yield from asyncio.sleep(1)
        remaining -= 1

def main():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(show_remaining())
    finally:
        loop.close()

if __name__ == '__main__':
    main()
