"""Download flags of top 20 countries by population

asyncio + aiottp version

Sample run::

    $ python3 flags_asyncio.py
    EG VN IN TR RU ID US DE CN MX JP BD NG ET FR BR PH PK CD IR
    20 flags downloaded in 1.07s

"""
# BEGIN FLAGS_ASYNCIO
import asyncio

import aiohttp  # <1>

from flags import BASE_URL, save_flag, show, main  # <2>


async def get_flag(cc):  # <3>
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    resp = await aiohttp.request('GET', url)  # <4>
    image = await resp.read()  # <5>
    return image


async def download_one(cc):  # <6>
    image = await get_flag(cc)  # <7>
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc


def download_many(cc_list):
    loop = asyncio.get_event_loop()  # <8>
    to_do = [download_one(cc) for cc in sorted(cc_list)]  # <9>
    wait_coro = asyncio.wait(to_do)  # <10>
    res, _ = loop.run_until_complete(wait_coro)  # <11>
    loop.close() # <12>

    return len(res)


if __name__ == '__main__':
    main(download_many)
# END FLAGS_ASYNCIO
