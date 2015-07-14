"""Download flags of countries (with error handling).

asyncio async/await version

"""
# BEGIN FLAGS2_ASYNCIO_TOP
import asyncio
import collections
from contextlib import closing

import aiohttp
from aiohttp import web
import tqdm

from flags2_common import main, HTTPStatus, Result, save_flag

# default set low to avoid errors from remote site, such as
# 503 - Service Temporarily Unavailable
DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000


class FetchError(Exception):  # <1>
    def __init__(self, country_code):
        self.country_code = country_code


async def get_flag(base_url, cc): # <2>
    url = '{}/{cc}/{cc}.gif'.format(base_url, cc=cc.lower())
    with closing(await aiohttp.request('GET', url)) as resp:
        if resp.status == 200:
            image = await resp.read()
            return image
        elif resp.status == 404:
            raise web.HTTPNotFound()
        else:
            raise aiohttp.HttpProcessingError(
                code=resp.status, message=resp.reason,
                headers=resp.headers)


async def download_one(cc, base_url, semaphore, verbose):  # <3>
    try:
        with (await semaphore):  # <4>
            image = await get_flag(base_url, cc)  # <5>
    except web.HTTPNotFound:  # <6>
        status = HTTPStatus.not_found
        msg = 'not found'
    except Exception as exc:
        raise FetchError(cc) from exc  # <7>
    else:
        save_flag(image, cc.lower() + '.gif')  # <8>
        status = HTTPStatus.ok
        msg = 'OK'

    if verbose and msg:
        print(cc, msg)

    return Result(status, cc)
# END FLAGS2_ASYNCIO_TOP

# BEGIN FLAGS2_ASYNCIO_DOWNLOAD_MANY
async def downloader_coro(cc_list, base_url, verbose, concur_req):  # <1>
    counter = collections.Counter()
    semaphore = asyncio.Semaphore(concur_req)  # <2>
    to_do = [download_one(cc, base_url, semaphore, verbose)
             for cc in sorted(cc_list)]  # <3>

    to_do_iter = asyncio.as_completed(to_do)  # <4>
    if not verbose:
        to_do_iter = tqdm.tqdm(to_do_iter, total=len(cc_list))  # <5>
    for future in to_do_iter:  # <6>
        try:
            res = await future  # <7>
        except FetchError as exc:  # <8>
            country_code = exc.country_code  # <9>
            try:
                error_msg = exc.__cause__.args[0]  # <10>
            except IndexError:
                error_msg = exc.__cause__.__class__.__name__  # <11>
            if verbose and error_msg:
                msg = '*** Error for {}: {}'
                print(msg.format(country_code, error_msg))
            status = HTTPStatus.error
        else:
            status = res.status

        counter[status] += 1  # <12>

    return counter  # <13>


def download_many(cc_list, base_url, verbose, concur_req):
    loop = asyncio.get_event_loop()
    coro = downloader_coro(cc_list, base_url, verbose, concur_req)
    counts = loop.run_until_complete(coro)  # <14>
    loop.close()  # <15>

    return counts


if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
# END FLAGS2_ASYNCIO_DOWNLOAD_MANY
