#!/usr/bin/env python3

# Inspired by
# https://snarky.ca/how-the-heck-does-async-await-work-in-python-3-5/

import asyncio
import time


async def countdown(label, delay):
    tabs = (ord(label) - ord('A')) * '\t'
    n = 3
    while n > 0:
        await asyncio.sleep(delay)  # <----
        dt = time.perf_counter() - t0
        print('━' * 50)
        print(f'{dt:7.4f}s \t{tabs}{label} = {n}')
        n -= 1

loop = asyncio.get_event_loop()
tasks = [
    loop.create_task(countdown('A', .7)),
    loop.create_task(countdown('B', 2)),
    loop.create_task(countdown('C', .3)),
    loop.create_task(countdown('D', 1)),
]
t0 = time.perf_counter()
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
print('━' * 50)
