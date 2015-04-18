"""
Wikipedia Picture of the Day (POTD) download example

Inspired by example at:
https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor-example
"""

from concurrent import futures

import potd

def save_month(year_month, verbose):
    year, month = [int(s) for s in year_month.split('-')]
    total_size = 0
    img_count = 0
    dates = potd.list_days_of_month(year, month)

    with futures.ThreadPoolExecutor(max_workers=100) as executor:
        downloads = dict((executor.submit(potd.save_one, date, verbose), date)
                             for date in dates)

        for future in futures.as_completed(downloads):
            date = downloads[future]
            if future.exception() is not None:
                print('%r generated an exception: %s' % (date,
                                                         future.exception()))
            else:
                img_size = future.result()
                total_size += img_size
                img_count += 1
                print('%r OK: %r' % (date, img_size))

    return img_count, total_size

if __name__ == '__main__':
    potd.main(save_month=save_month)
