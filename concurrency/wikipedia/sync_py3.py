"""
Wikipedia Picture of the Day (POTD) download example

Baseline synchronous example for comparison: downloads images and metadata
in the simple but slow synchronous way i.e. one after the other.
"""

import sys
import os
import io
import re
import argparse
import datetime
import urllib.request
import urllib.error
import contextlib
import time

POTD_BASE_URL = 'http://en.wikipedia.org/wiki/Template:POTD/'

THUMB_BASE_URL = 'http://upload.wikimedia.org/wikipedia/commons/thumb/'
THUMB_SRC_RE = re.compile(r'src=".*?/thumb/(.*?/\d+px-[^"]+)')

LOCAL_IMG_PATH = 'pictures/'

verbose = True


class ParsingException(ValueError):
    """Raised if unable to parse POTD MediaWiki source"""


def gen_month_dates(year, month):
    """Produce all dates in a given year, month"""
    a_date = datetime.date(year, month, 1)
    one_day = datetime.timedelta(1)
    while a_date.month == month:
        yield '{:%Y-%m-%d}'.format(a_date)
        a_date += one_day


def fetch_potd_url(iso_date):
    """Fetch POTD thumbnail URL for iso_date ('YYYY-MM-DD' format)"""
    if verbose:
        print(iso_date)
    potd_url = POTD_BASE_URL + iso_date
    try:
        with urllib.request.urlopen(potd_url) as fp:
            html = fp.read().decode('utf-8')
            thumb_src = THUMB_SRC_RE.search(html)
            if not thumb_src:
                msg = 'cannot find thumbnail source for ' + potd_url
                raise ParsingException(msg)
            thumb_url = THUMB_BASE_URL+thumb_src.group(1)
    except urllib.error.HTTPError:
        return None
    return thumb_url


def gen_img_names(iso_month):
    """Produce picture names by fetching POTD metadata"""
    year, month = (int(part) for part in iso_month.split('-'))
    for iso_date in gen_month_dates(year, month):
        img_url = fetch_potd_url(iso_date)
        if img_url is None:
            break
        yield (iso_date, img_url)


def fetch_image(iso_date, img_url):
    """Fetch and save image data for date and url"""
    if verbose:
        print('\t' + img_url)
    with contextlib.closing(urllib.request.urlopen(img_url)) as fp:
        img = fp.read()
    img_filename = iso_date + '__' + img_url.split('/')[-1]
    if verbose:
        print('\t\twriting %0.1f Kbytes' % (len(img)/1024.0))
    img_path = os.path.join(LOCAL_IMG_PATH, img_filename)
    with io.open(img_path, 'wb') as fp:
        fp.write(img)
    return len(img)


def get_images(iso_month, max_count=0):
    """Download up to max_count images for a given month"""
    if max_count is 0:
        max_count = sys.maxsize
    img_count = 0
    total_size = 0
    for iso_date, img_url in gen_img_names(iso_month):
        total_size += fetch_image(iso_date, img_url)
        img_count += 1
        if img_count == max_count:
            break

    return (img_count, total_size)


def main():
    """Get "Pictures of The Day" from English Wikipedia for a given month"""
    global verbose
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('year_month', help='year and month in YYYY-MM format')
    parser.add_argument('-q', '--max_qty', type=int,
                        help='maximum number of files to download')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='display progress information')
    args = parser.parse_args()
    verbose = args.verbose
    t0 = time.time()
    img_count, total_size = get_images(args.year_month, args.max_qty)
    elapsed = time.time() - t0
    print("images: %3d |  total size: %6.1f Kbytes  |  elapsed time: %3ds" %
          (img_count, total_size/1024.0, elapsed))

if __name__ == '__main__':
    main()
