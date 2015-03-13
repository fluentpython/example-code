@asyncio.coroutine
def a(future):
    print('a, future:', future, hex(id(future)))
    res = yield from future
    return res

def b():
    future = asyncio.Future()
    coro = a(future)
    prime_result = next(coro)
    print('b, prime_result:', prime_result, hex(id(future)))

loop = asyncio.get_event_loop()
future = asyncio.Future()
print('future:', future, hex(id(future)))
tasks = [asyncio.async(a(future))]

res = loop.run_until_complete(b())

