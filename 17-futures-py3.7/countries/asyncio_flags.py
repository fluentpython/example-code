"""Download flags of top 20 countries by population

asyncio + aiottp version

Sample run::

    $ python3 flags_asyncio.py 
    CN EG BR IN ID RU NG VN JP DE TR PK FR ET MX PH US IR CD BD 
    20 flags downloaded in 0.35s

"""
# BEGIN FLAGS_ASYNCIO
import os
import time
import sys
import asyncio  # <1>

import aiohttp  # <2>


POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()

BASE_URL = 'http://flupy.org/data/flags'

DEST_DIR = 'downloads/'


def save_flag(img, filename):
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)


async def get_flag(session, cc):  # <3>
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    async with session.get(url) as resp:        # <4>
        return await resp.read()  # <5>


def show(text):
    print(text, end=' ')
    sys.stdout.flush()


async def download_one(session, cc):  # <6>
    image = await get_flag(session, cc)  # <7>
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc


async def download_many(cc_list):
    async with aiohttp.ClientSession() as session:  # <8>
        res = await asyncio.gather(                 # <9>
            *[asyncio.create_task(download_one(session, cc))
                for cc in sorted(cc_list)])

    return len(res)


def main():  # <10>
    t0 = time.time()
    count = asyncio.run(download_many(POP20_CC))
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


if __name__ == '__main__':
    main()
# END FLAGS_ASYNCIO
