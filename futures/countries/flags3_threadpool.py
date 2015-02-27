"""Download flags of top 10 countries by population

ThreadPool version

Sample run::

    $ python3 pop10_threadpool1.py
    BR retrieved.
    PK retrieved.
    BD retrieved.
    JP retrieved.
    CN retrieved.
    IN retrieved.
    RU retrieved.
    NG retrieved.
    US retrieved.
    ID retrieved.
    10 flags downloaded in 0.63s

"""

from concurrent import futures
from collections import namedtuple
from enum import Enum

import requests

from flags_sequential2 import BASE_URL
from flags_sequential2 import save_flag, get_flag, main, Counts

MAX_WORKERS = 200

Status = Enum('Status', 'ok not_found error')
Result = namedtuple('Result', 'status data')


def get_country(cc):
    url = '{}/{cc}/metadata.json'.format(BASE_URL, cc=cc.lower())
    res = requests.get(url)
    if res.status_code != 200:
        res.raise_for_status()
    return res.json()['country']


def download_one(cc):
    try:
        image = get_flag(cc)
        country = get_country(cc)
    except requests.exceptions.HTTPError as exc:
        res = exc.response
        if res.status_code == 404:
            status = Status.not_found
        else:
            msg = '{} failed: {res.status_code} - {res.reason}'
            print(msg.format(cc, res=exc.response))
            status = Status.error
    else:
        print('{} retrieved.'.format(cc))
        country = country.replace(' ', '_')
        save_flag(image, '{}-{}.gif'.format(country, cc))
        status = Status.ok
    return Result(status, cc)


def download_many(cc_list):
    workers = min(len(cc_list), MAX_WORKERS)
    with futures.ThreadPoolExecutor(workers) as executor:
        res = executor.map(download_one, sorted(cc_list))
    res = list(res)
    counts = []
    for status in Status:
        counts.append(len([r for r in res if r.status == status]))
    return Counts(*counts)


if __name__ == '__main__':
    main(download_many)
