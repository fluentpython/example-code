"""
Wikipedia Picture of the Day (POTD) download example

Note:
The earliest Pictures of the Day I've found are in this page:

http://en.wikipedia.org/wiki/Wikipedia:Picture_of_the_day/May_2004

However, I have not found Template:POTD/YYYY-MM-DD pages earlier
than this:

http://en.wikipedia.org/wiki/Template:POTD/2007-01-01

For simplicity, this script only retrieves pictures starting
from 2007-01-01.

"""
import sys
import argparse
import re
import imghdr
import time
import datetime

import requests

SAVE_DIR = 'pictures/'
POTD_BASE_URL = 'http://en.wikipedia.org/wiki/Template:POTD/'
POTD_IMAGE_RE = re.compile(r'src="(//upload\..*?)"')
PODT_EARLIEST_TEMPLATE = '2007-01-01'

RE_YEAR = r'([12]\d{3})'
RE_MONTH = RE_YEAR + r'-([01]\d)'
RE_DATE = RE_MONTH + r'-([0-3]\d)'
ISO_DATE_FMT = '%Y-%m-%d'

DATEFORMS = [
    ('date', re.compile('^' + RE_DATE + '$')),
    ('month', re.compile('^' + RE_MONTH + '$')),
    ('year', re.compile('^' + RE_YEAR + '$'))
]


class NoPictureForDate(Exception):
    '''No Picture of the Day found for {iso_date}'''


class NoPictureTemplateBefore(ValueError):
    '''Template:POTD did not exist before PODT_EARLIEST_TEMPLATE'''


def get_picture_url(iso_date):
    page_url = POTD_BASE_URL+iso_date
    response = requests.get(page_url)
    pict_url = POTD_IMAGE_RE.search(response.text)
    if pict_url is None:
        raise NoPictureForDate(iso_date)
    return 'http:' + pict_url.group(1)


def get_picture(iso_date):
    pict_url = get_picture_url(iso_date)
    response = requests.get(pict_url)
    octets = response.content
    return octets


def get_picture_type(octets):
    pict_type = imghdr.what(None, octets)
    if pict_type is None:
        if (octets.startswith(b'<') and
                b'<svg' in octets[:200] and
                octets.rstrip().endswith(b'</svg>')):
            pict_type = 'svg'
    return pict_type


def validate_date(text):
    try:
        parts = [int(part) for part in text.split('-')]
    except ValueError:
        raise ValueError('date must use YYYY, YYYY-MM or YYYY-MM-DD format')

    test_parts = parts[:]
    while len(test_parts) < 3:
        test_parts.append(1)
    date = datetime.datetime(*(int(part) for part in test_parts))
    iso_date = date.strftime(ISO_DATE_FMT)
    iso_date = iso_date[:1+len(parts)*3]
    if iso_date < PODT_EARLIEST_TEMPLATE:
        raise NoPictureTemplateBefore(PODT_EARLIEST_TEMPLATE)
    return iso_date


def gen_month_dates(iso_month):
    first = datetime.datetime.strptime(iso_month+'-01', ISO_DATE_FMT)
    one_day = datetime.timedelta(days=1)
    date = first
    while date.month == first.month:
        yield date.strftime(ISO_DATE_FMT)
        date += one_day


def gen_year_dates(iso_year):
    for i in range(1, 13):
        yield from gen_month_dates(iso_year + '-{:02d}'.format(i))


def gen_dates(iso_parts):
    if len(iso_parts) == 4:
        yield from gen_year_dates(iso_parts)
    elif len(iso_parts) == 7:
        yield from gen_month_dates(iso_parts)
    else:
        yield iso_parts


def parse_args(argv):
    parser = argparse.ArgumentParser(description=main.__doc__)
    date_help = 'YYYY-MM-DD or YYYY-MM or YYYY: year, month and day'
    parser.add_argument('date', help=date_help)
    parser.add_argument('-q', '--max_qty', type=int,
                        help='maximum number of items to fetch')
    parser.add_argument('-u', '--url_only', action='store_true',
                        help='get picture URLS only')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='display progress information')
    args = parser.parse_args(argv)

    try:
        iso_parts = validate_date(args.date)
    except ValueError as exc:
        print('error:', exc.args[0])
        parser.print_usage()
        sys.exit(2)

    dates = list(gen_dates(iso_parts))
    if args.verbose:
        if len(dates) == 1:
            print('-> Date: ', dates[0])
        else:
            fmt = '-> {} days: {}...{}'
            print(fmt.format(len(dates), dates[0], dates[-1]))

    return dates, args


def get_picture_urls(dates, verbose=False):
    urls = []
    count = 0
    for date in dates:
        try:
            url = get_picture_url(date)
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


def main(argv, get_picture_urls):
    """Get Wikipedia "Picture of The Day" for date, month or year"""

    dates, args = parse_args(argv)

    t0 = time.time()

    urls = get_picture_urls(dates, args.verbose)

    elapsed = time.time() - t0
    if args.verbose:
        print('-> found: {} pictures | elapsed time: {:.2f}s'
              .format(len(urls), elapsed))


if __name__ == '__main__':
    main(sys.argv[1:], get_picture_urls)
