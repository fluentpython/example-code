import sys
import argparse
import os

from daypicts import get_picture_url, validate_date, gen_dates
from daypicts import NoPictureForDate
from daypicts import POTD_PATH

FIXTURE_DIR = 'fixture/'


def parse_args(argv):
    parser = argparse.ArgumentParser(description=main.__doc__)
    date_help = 'YYYY-MM-DD or YYYY-MM or YYYY: year, month and day'
    parser.add_argument('date', help=date_help)

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


def main(argv):
    """Build test fixture from Wikipedia "POTD" data"""

    save_path = os.path.join(FIXTURE_DIR,POTD_PATH)
    try:
        os.makedirs(save_path)
    except FileExistsError:
        pass

    dates, args = parse_args(argv)

    save_picture_urls(dates, save_path)

if __name__ == '__main__':
    main(sys.argv[1:])
