"""Download flags of top 10 countries by population

asyncio version

Sample run::

    $ python3 pop10_asyncio1.py
    CN retrieved.
    US retrieved.
    BR retrieved.
    NG retrieved.
    PK retrieved.
    RU retrieved.
    ID retrieved.
    IN retrieved.
    BD retrieved.
    JP retrieved.
    10 flags downloaded in 0.45s

"""

import asyncio
from collections import namedtuple
from enum import Enum

import aiohttp
from aiohttp import web

from flags_sequential2 import BASE_URL
from flags_sequential2 import save_flag, main, Counts

MAX_TASKS = 100 if 'localhost' in BASE_URL else 5
TIMEOUT = 120 # seconds

Status = Enum('Status', 'ok not_found error')
Result = namedtuple('Result', 'status data')


@asyncio.coroutine
def http_get(url):
    res = yield from aiohttp.request('GET', url)
    if res.status == 200:
        ctype = res.headers.get('Content-type', '').lower()

        if 'json' in ctype or url.endswith('json'):
            data = yield from res.json()
        else:
            data = yield from res.read()
        return data
    elif res.status == 404:
        raise web.HTTPNotFound()
    else:
        raise aiohttp.errors.HttpProcessingError(
                code=res.status, message=res.reason, headers=res.headers)


@asyncio.coroutine
def get_flag(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    return (yield from http_get(url))


@asyncio.coroutine
def get_country(cc):
    url = '{}/{cc}/metadata.json'.format(BASE_URL, cc=cc.lower())
    metadata = yield from http_get(url)
    return metadata['country']

@asyncio.coroutine
def download_one(cc, semaphore):
    try:
        with (yield from semaphore):
            image = yield from get_flag(cc)
        with (yield from semaphore):
            country = yield from get_country(cc)
    except web.HTTPNotFound:
        status = Status.not_found
    except aiohttp.errors.HttpProcessingError as exc:
        msg = '{} failed: {exc.code} - {exc.message}'
        print(msg.format(cc, exc=exc))
        status = Status.error
    except aiohttp.errors.ClientResponseError as exc:
        try:
            context = exc.__context__.__class__.__name__
        except AttributeError:
            context = '(unknown context)'
        msg = '{} failed: {}'
        print(msg.format(cc, context))
        status = Status.error
    else:
        print('{} retrieved.'.format(cc.upper()))
        country = country.replace(' ', '_')
        save_flag(image, '{}-{}.gif'.format(country, cc))
        status = Status.ok
    return Result(status, cc)


def download_many(cc_list):
    semaphore = asyncio.Semaphore(MAX_TASKS)
    to_do = [download_one(cc, semaphore) for cc in cc_list]
    loop = asyncio.get_event_loop()
    #loop.set_debug(True)
    try:
        done, pending = loop.run_until_complete(asyncio.wait(to_do, timeout=TIMEOUT))
    except Exception as exc:
        print('*' * 60)
        print(exc)
        print(vars(exc))
        print('*' * 60)
    counts = []
    for status in Status:
        counts.append(len([task for task in done
                            if task.result().status == status]))
    for task in pending:
        task.cancel()
    loop.close()

    return Counts(*counts)


if __name__ == '__main__':
    main(download_many)
