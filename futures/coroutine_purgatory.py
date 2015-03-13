@asyncio.coroutine
def three_phases():
    response1 = yield from fetch1(request1)
    # phase 1
    request2 = step1(response1)
    response2 = yield from fetch2(request2)
    # phase 2
    request3 = step2(response2)
    response3 = yield from fetch3(request3)
    # phase 3
    step3(response3)


loop.create_task(three_phases)
