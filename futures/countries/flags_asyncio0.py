"""Download flags of top 20 countries by population

asyncio+aiottp version

Sample run::

    $ python3 flags_asyncio0.py
    EG retrieved.
    BD retrieved.
    JP retrieved.
    ...
    CD retrieved.
    PH retrieved.
    ET retrieved.
    20 flags downloaded in 1.05s

"""

import asyncio

import aiohttp

from flags import BASE_URL, save_flag, main


@asyncio.coroutine
def download_one(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    res = yield from aiohttp.request('GET', url)
    image = yield from res.read()
    print('{} retrieved.'.format(cc))
    save_flag(image, cc.lower() + '.gif')
    return cc


def download_many(cc_list):
    loop = asyncio.get_event_loop()
    to_do = [download_one(cc) for cc in cc_list]
    res, _ = loop.run_until_complete(asyncio.wait(to_do))
    loop.close()
    return len(res)


if __name__ == '__main__':
    main(download_many)
