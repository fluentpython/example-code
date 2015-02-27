"""Download flags of countries (with error handling).

Sequential version

Sample run::

    $

"""

import requests
import tqdm

from flag_utils import main, save_flag, Counts, Status, Result


DEFAULT_CONCUR_REQ = 1
MAX_CONCUR_REQ = 1


def get_flag(base_url, cc):
    url = '{}/{cc}/{cc}.gif'.format(base_url, cc=cc.lower())
    res = requests.get(url)
    if res.status_code != 200:
        res.raise_for_status()
    return res.content


def download_one(cc, base_url, verbose=False):
    try:
        image = get_flag(base_url, cc)
    except requests.exceptions.HTTPError as exc:
        res = exc.response
        if res.status_code == 404:
            status = Status.not_found
            msg = ''
        else:
            status = Status.error
            msg = 'error {res.status_code} - {res.reason}'
            msg = msg.format(res=exc.response)
    except requests.exceptions.ConnectionError as exc:
        status = Status.error
        msg = 'failed: {}'.format(cc, exc.args)
    else:
        save_flag(image, cc.lower() + '.gif')
        status = Status.ok
        msg = 'OK'

    if verbose and msg:
        print(cc, msg)

    return Result(status, cc)


def download_many(cc_list, base_url, verbose, max_req):
    counts = [0, 0, 0]
    if not verbose:
        cc_iter = tqdm.tqdm(sorted(cc_list))
    else:
        cc_iter = sorted(cc_list)
    for cc in cc_iter:
        try:
            res = download_one(cc, base_url, verbose)
        except Exception as exc:
            msg = 'Unexpected exception for {}: {!r}'
            print(msg.format(cc, exc))
        else:
            counts[res.status.value-1] += 1

    return Counts(*counts)


if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
