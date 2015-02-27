"""Download flags of top 20 countries by population

ThreadPool version

Sample run::

    $ python3 flags_threadpool.py
    BD retrieved.
    EG retrieved.
    CN retrieved.
    ...
    PH retrieved.
    US retrieved.
    IR retrieved.
    20 flags downloaded in 0.93s

"""

from concurrent import futures

from flags import save_flag, get_flag, main

MAX_WORKERS = 100


def download_one(cc):
    image = get_flag(cc)
    print('{} retrieved.'.format(cc.upper()))
    save_flag(image, cc.lower() + '.gif')
    return cc


def download_many(cc_list):
    workers = min(len(cc_list), MAX_WORKERS)
    with futures.ThreadPoolExecutor(workers) as executor:
        res = executor.map(download_one, sorted(cc_list))

    return len(list(res))


if __name__ == '__main__':
    main(download_many)
