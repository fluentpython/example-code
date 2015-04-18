import sys
import argparse
import os
import urllib

import requests

from daypicts import get_picture_url, get_picture_urls
from daypicts import validate_date, gen_dates, picture_type
from daypicts import NoPictureForDate
from daypicts import REMOTE_PICT_BASE_URL, PICT_EXCEPTIONS

FIXTURE_DOC_DIR = 'fixture/docroot/'
FIXTURE_TEMPLATE_POTD_DIR = FIXTURE_DOC_DIR + 'Template-POTD/'

def parse_args(argv):
    parser = argparse.ArgumentParser(description=main.__doc__)
    date_help = 'YYYY-MM-DD or YYYY-MM or YYYY: year, month and day'
    parser.add_argument('date', help=date_help)
    parser.add_argument('-u', '--url_only', action='store_true',
                        help='get picture URLS only')

    args = parser.parse_args(argv)

    try:
        iso_parts = validate_date(args.date)
    except ValueError as exc:
        print('error:', exc.args[0])
        parser.print_usage()
        sys.exit(2)

    dates = list(gen_dates(iso_parts))
    if len(dates) == 1:
        print('-> Date: ', dates[0])
    else:
        fmt = '-> {} days: {}...{}'
        print(fmt.format(len(dates), dates[0], dates[-1]))

    return dates, args


def save_picture_urls(dates, save_path):
    for date in dates:
        try:
            url = get_picture_url(date)
        except NoPictureForDate as exc:
            snippet = repr(exc)
        else:
            snippet = url.replace('http://', 'src="//') + '"'
        print(date, end=' ')
        print(snippet)
        with open(os.path.join(save_path, date), 'w') as fp:
            fp.write(snippet)


def save_pictures(dates, save_path, verbose=False):
    urls_ok = []
    for date, url in get_picture_urls(dates, verbose):
        response = requests.get(url)
        file_path = os.path.join(save_path,
                                 url.replace(REMOTE_PICT_BASE_URL, ''))
        file_path = urllib.parse.unquote(file_path)
        octets = response.content
        # http://en.wikipedia.org/wiki/Template:POTD/2013-06-15

        if date not in PICT_EXCEPTIONS:
            assert picture_type(octets) is not None, url

        try:
            os.makedirs(os.path.dirname(file_path))
        except FileExistsError:
            pass
        with open(file_path, 'wb') as fp:
            fp.write(octets)

        print(file_path)
    return urls_ok


def main(argv):
    """Build test fixture from Wikipedia "POTD" data"""

    try:
        os.makedirs(FIXTURE_TEMPLATE_POTD_DIR)
    except FileExistsError:
        pass

    dates, args = parse_args(argv)

    if args.url_only:
        save_picture_urls(dates, FIXTURE_TEMPLATE_POTD_DIR)
    else:
        save_pictures(dates, FIXTURE_DOC_DIR)


if __name__ == '__main__':
    main(sys.argv[1:])
