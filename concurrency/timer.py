import asyncio

@asyncio.coroutine
def show_remaining():
    for remaining in range(5, 0, -1):
        print('Remaining: ', remaining)
        yield from asyncio.sleep(1)

def main():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(show_remaining())
    finally:
        loop.close()

if __name__ == '__main__':
    main()
