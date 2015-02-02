"""
Wikipedia Picture of the Day (POTD) download example
"""

import sys
import asyncio
import aiohttp

from daypicts import main, NoPictureForDate
from daypicts import POTD_BASE_URL, POTD_IMAGE_RE

GLOBAL_TIMEOUT = 300  # seconds
MAX_CONCURRENT_REQUESTS = 30


@asyncio.coroutine
def get_picture_url(iso_date, semaphore):
    page_url = POTD_BASE_URL+iso_date
    with (yield from semaphore):
        response = yield from aiohttp.request('GET', page_url)
        text = yield from response.text()
    pict_url = POTD_IMAGE_RE.search(text)
    if pict_url is None:
        raise NoPictureForDate(iso_date)
    return 'http:' + pict_url.group(1)


@asyncio.coroutine
def get_picture_urls(dates, verbose=False):
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    tasks = [get_picture_url(date, semaphore) for date in dates]
    urls = []
    count = 0
    # get results as jobs are done
    for job in asyncio.as_completed(tasks, timeout=GLOBAL_TIMEOUT):
        try:
            url = yield from job
        except NoPictureForDate as exc:
            if verbose:
                print('*** {!r} ***'.format(exc))
            continue
        except aiohttp.ClientResponseError as exc:
            print('****** {!r} ******'.format(exc))
            continue
        count += 1
        if verbose:
            print(format(count, '3d'), end=' ')
            print(url.split('/')[-1])
        else:
            print(url)
        urls.append(url)
    return urls


def run_loop(dates, verbose=False):

    loop = asyncio.get_event_loop()
    return loop.run_until_complete(get_picture_urls(dates, verbose))


if __name__ == '__main__':
    main(sys.argv[1:], run_loop)
