"""
Wikipedia Picture of the Day (POTD) download example

Baseline synchronous example for comparison: downloads metadata and
images in the simple but slow synchronous way i.e. one after the other.
"""

import calendar
import datetime
import re
import os
import io
import time

import requests

import argparse

SAVE_DIR = 'pictures/'
POTD_BASE_URL = 'http://en.wikipedia.org/wiki/Template:POTD/'

class NoPictureForDate(Exception):
    '''No Picture of the Day found for {day}'''

def build_page_url(iso_date):
    return POTD_BASE_URL + iso_date

def fetch(url):
    response = requests.get(url)
    return response

def extract_image_url(html):
    re_image = r'src="(//upload\..*?)"'
    image_url = re.search(re_image, html)
    return 'http:' + image_url.group(1)

def format_date(year, month, day):
    return '{year}-{month:02d}-{day:02d}'.format(**locals())

def list_days_of_month(year, month):
    lastday = calendar.monthrange(year, month)[1]
    days = [format_date(year, month, day) for day in range(1, lastday + 1)]
    return days

def build_save_path(iso_date, url):
    head, filename = os.path.split(url)
    return os.path.join(SAVE_DIR, iso_date+'_'+filename)

def save_one(iso_date, verbose):
    page_url = build_page_url(iso_date)
    response = fetch(page_url)
    if response.status_code != 200:
        msg = NoPictureForDate.__doc__.format(day=iso_date)
        raise NoPictureForDate(msg)
    img_url = extract_image_url(response.text)
    response = fetch(img_url)
    path = build_save_path(iso_date, img_url)
    if verbose:
        print('saving: '+path)
    with io.open(path, 'wb') as fp:
        fp.write(response.content)
    return len(response.content)

def save_month(year_month, verbose):
    year, month = [int(s) for s in year_month.split('-')]
    total_size = 0
    img_count = 0
    dates = list_days_of_month(year, month)

    for date in dates:
        try:
            total_size += save_one(date, verbose)
            img_count += 1
        except NoPictureForDate:
            continue
    return img_count, total_size

def main(save_one=save_one, save_month=save_month):
    """Get "Picture of The Day" from English Wikipedia for a given date or month"""
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('date', help='year, month and (optional) day in YYYY-MM-DD format')
    parser.add_argument('-q', '--max_qty', type=int,
                        help='maximum number of files to download')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='display progress information')
    args = parser.parse_args()

    t0 = time.time()
    if len(args.date) == len('YYYY-MM-DD'):
        img_count = 1
        total_size = save_one(args.date, args.verbose)
    else:
        img_count, total_size = save_month(args.date, args.verbose)
    elapsed = time.time() - t0
    print("images: %3d |  total size: %6.1f Kbytes  |  elapsed time: %3ds" %
          (img_count, total_size/1024.0, elapsed))


if __name__ == '__main__':
    main()
