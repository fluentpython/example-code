"""Download flags of top 10 countries by population

ThreadPool version

Sample run::

    $

"""

from concurrent import futures

import tqdm

from flag_utils import main, Counts
from flags2_sequential import get_flag, download_one

DEFAULT_CONCUR_REQ = 30
MAX_CONCUR_REQ = 1000


def download_many(cc_list, base_url, verbose, concur_req):
    with futures.ThreadPoolExecutor(concur_req) as executor:
        to_do = [executor.submit(download_one, cc, base_url, verbose)
                 for cc in sorted(cc_list)]
        counts = [0, 0, 0]
        to_do_iter = futures.as_completed(to_do)
        if not verbose:
            to_do_iter = tqdm.tqdm(to_do_iter, total=len(cc_list))
        for future in to_do_iter:
            try:
                res = future.result()
            except Exception as exc:
                print('*** Unexpected exception:', exc)
            else:
                counts[res.status.value-1] += 1

    return Counts(*counts)


if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
