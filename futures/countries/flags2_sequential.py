"""Download flags of countries (with error handling).

Sequential version

Sample run::

    $ python3 flags2_sequential.py -s DELAY b
    DELAY site: http://localhost:8002/flags
    Searching for 26 flags: from BA to BZ
    1 concurrent connection will be used.
    --------------------
    17 flags downloaded.
    9 not found.
    Elapsed time: 13.36s

"""

import collections

import requests
import tqdm

from flags2_common import main, save_flag, HTTPStatus, Result


DEFAULT_CONCUR_REQ = 1
MAX_CONCUR_REQ = 1

# BEGIN FLAGS2_BASIC_HTTP_FUNCTIONS
def get_flag(base_url, cc):
    url = '{}/{cc}/{cc}.gif'.format(base_url, cc=cc.lower())
    resp = requests.get(url)
    if resp.status_code != 200:  # <1>
        resp.raise_for_status()
    return resp.content


def download_one(cc, base_url, verbose=False):
    try:
        image = get_flag(base_url, cc)
    except requests.exceptions.HTTPError as exc:  # <2>
        res = exc.response
        if res.status_code == 404:
            status = HTTPStatus.not_found  # <3>
            msg = 'not found'
        else:  # <4>
            raise
    else:
        save_flag(image, cc.lower() + '.gif')
        status = HTTPStatus.ok
        msg = 'OK'

    if verbose:  # <5>
        print(cc, msg)

    return Result(status, cc)  # <6>
# END FLAGS2_BASIC_HTTP_FUNCTIONS

# BEGIN FLAGS2_DOWNLOAD_MANY_SEQUENTIAL
def download_many(cc_list, base_url, verbose, max_req):
    counter = collections.Counter()  # <1>
    cc_iter = sorted(cc_list)  # <2>
    if not verbose:
        cc_iter = tqdm.tqdm(cc_iter)  # <3>
    for cc in cc_iter:  # <4>
        try:
            res = download_one(cc, base_url, verbose)  # <5>
        except requests.exceptions.HTTPError as exc:  # <6>
            error_msg = 'HTTP error {res.status_code} - {res.reason}'
            error_msg = error_msg.format(res=exc.response)
        except requests.exceptions.ConnectionError as exc:  # <7>
            error_msg = 'Connection error'
        else:  # <8>
            error_msg = ''
            status = res.status

        if error_msg:
            status = HTTPStatus.error  # <9>
        counter[status] += 1  # <10>
        if verbose and error_msg: # <11>
            print('*** Error for {}: {}'.format(cc, error_msg))

    return counter  # <12>
# END FLAGS2_DOWNLOAD_MANY_SEQUENTIAL

if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
