"""
Wikipedia Picture of the Day (POTD) download example
"""

import sys
from concurrent import futures

from daypicts import main, get_picture_url, NoPictureForDate

GLOBAL_TIMEOUT = 300  # seconds
MAX_CONCURRENT_REQUESTS = 30


def get_picture_urls(dates, verbose=False):
    pool = futures.ThreadPoolExecutor(MAX_CONCURRENT_REQUESTS)

    pending = {}
    for date in dates:
        job = pool.submit(get_picture_url, date)
        pending[job] = date

    urls = []
    count = 0

    # get results as jobs are done
    for job in futures.as_completed(pending, timeout=GLOBAL_TIMEOUT):
        try:
            url = job.result()
        except NoPictureForDate as exc:
            if verbose:
                print('*** {!r} ***'.format(exc))
            continue
        count += 1
        if verbose:
            print(format(count, '3d'), end=' ')
            print(url.split('/')[-1])
        else:
            print(url)
        urls.append(url)
    return urls


if __name__ == '__main__':
    main(sys.argv[1:], get_picture_urls)
