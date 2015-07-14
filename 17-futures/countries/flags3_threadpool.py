"""Download flags and names of countries.

ThreadPool version
"""

import collections
from concurrent import futures

import requests
import tqdm

from flags2_common import main, save_flag, HTTPStatus, Result
from flags2_sequential import get_flag

DEFAULT_CONCUR_REQ = 30
MAX_CONCUR_REQ = 1000


def get_country(base_url, cc):
    url = '{}/{cc}/metadata.json'.format(base_url, cc=cc.lower())
    res = requests.get(url)
    if res.status_code != 200:
        res.raise_for_status()
    return res.json()['country']


def download_one(cc, base_url, verbose=False):
    try:
        image = get_flag(base_url, cc)
        country = get_country(base_url, cc)
    except requests.exceptions.HTTPError as exc:
        res = exc.response
        if res.status_code == 404:
            status = HTTPStatus.not_found
            msg = 'not found'
        else:  # <4>
            raise
    else:
        country = country.replace(' ', '_')
        save_flag(image, '{}-{}.gif'.format(country, cc))
        status = HTTPStatus.ok
        msg = 'OK'

    if verbose:
        print(cc, msg)

    return Result(status, cc)


def download_many(cc_list, base_url, verbose, concur_req):
    counter = collections.Counter()
    with futures.ThreadPoolExecutor(concur_req) as executor:
        to_do_map = {}
        for cc in sorted(cc_list):
            future = executor.submit(download_one,
                            cc, base_url, verbose)
            to_do_map[future] = cc
        to_do_iter = futures.as_completed(to_do_map)
        if not verbose:
            to_do_iter = tqdm.tqdm(to_do_iter, total=len(cc_list))
        for future in to_do_iter:
            try:
                res = future.result()
            except requests.exceptions.HTTPError as exc:
                error_msg = 'HTTP {res.status_code} - {res.reason}'
                error_msg = error_msg.format(res=exc.response)
            except requests.exceptions.ConnectionError as exc:
                error_msg = 'Connection error'
            else:
                error_msg = ''
                status = res.status

            if error_msg:
                status = HTTPStatus.error
            counter[status] += 1
            if verbose and error_msg:
                cc = to_do_map[future]
                print('*** Error for {}: {}'.format(cc, error_msg))

    return counter


if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
