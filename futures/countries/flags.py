"""Download flags of top 20 countries by population

Sequential version

Sample run::

    $ python3 flags.py
    BD retrieved.
    BR retrieved.
    CD retrieved.
    ...
    TR retrieved.
    US retrieved.
    VN retrieved.
    20 flags downloaded in 10.16s

"""

import os
import time

import requests

POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()

BASE_URL = 'http://python.pro.br/fluent/data/flags'

DEST_DIR = 'downloads/'


def save_flag(img, filename):
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)


def get_flag(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    res = requests.get(url)
    return res.content


def download_many(cc_list):
    for cc in sorted(cc_list):
        image = get_flag(cc)
        print('{} retrieved.'.format(cc))
        save_flag(image, cc.lower() + '.gif')

    return len(cc_list)


def main(download_many):
    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


if __name__ == '__main__':
    main(download_many)
