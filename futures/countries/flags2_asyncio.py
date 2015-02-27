"""Download flags of top 10 countries by population

asyncio version

Sample run::

    $

"""

import asyncio
from collections import namedtuple
from enum import Enum

import aiohttp
from aiohttp import web
import tqdm

from flag_utils import main, save_flag, Counts

# default set low to avoid errors from remote site:
# 503 - Service Temporarily Unavailable
DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000

TIMEOUT = 120 # seconds

Status = Enum('Status', 'ok not_found error')
Result = namedtuple('Result', 'status data')


@asyncio.coroutine
def get_flag(base_url, cc):
    url = '{}/{cc}/{cc}.gif'.format(base_url, cc=cc.lower())
    res = yield from aiohttp.request('GET', url)
    if res.status == 200:
        image = yield from res.read()
        return image
    elif res.status == 404:
        raise web.HTTPNotFound()
    else:
        raise aiohttp.errors.HttpProcessingError(
                code=res.status, message=res.reason, headers=res.headers)


@asyncio.coroutine
def download_one(cc, base_url, semaphore, verbose):
    try:
        with (yield from semaphore):
            image = yield from get_flag(base_url, cc)
    except web.HTTPNotFound:
        status = Status.not_found
        msg = ''
    except aiohttp.errors.HttpProcessingError as exc:
        status = Status.error
        msg = '{} failed: {exc.code} - {exc.message}'
        msg = msg.format(cc, exc=exc)
    except aiohttp.errors.ClientError as exc:
        try:
            context = exc.__context__.__class__.__name__
        except AttributeError:
            # we chain all exceptions, you should get original exception from __cause__
            context = '(unknown context)'
        msg = '{} failed: {}'.format(cc, context)
        status = Status.error
    else:
        save_flag(image, cc.lower() + '.gif')
        status = Status.ok
        msg = 'OK'

    if verbose and msg:
        print(cc, msg)

    return Result(status, cc)


@asyncio.coroutine
def downloader_coro(cc_list, base_url, verbose, max_req):
    semaphore = asyncio.Semaphore(max_req)
    to_do = [download_one(cc, base_url, semaphore, verbose) for cc in cc_list]
    results = []
    to_do_iter = asyncio.as_completed(to_do)
    if not verbose:
        to_do_iter = tqdm.tqdm(to_do_iter, total=len(cc_list))
    for future in to_do_iter:
        result = yield from future
        results.append(result)
    return results


def download_many(cc_list, base_url, verbose, max_req):
    loop = asyncio.get_event_loop()
    #loop.set_debug(True)
    try:
        coro = downloader_coro(cc_list, base_url, verbose, max_req)
        done = loop.run_until_complete(coro)
    except Exception as exc:
        print('*' * 60)
        print(exc)
        print(vars(exc))
        print('*' * 60)
    counts = []
    for status in Status:
        counts.append(len([res for res in done
                            if res.status == status]))
    loop.close()

    return Counts(*counts)


if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
