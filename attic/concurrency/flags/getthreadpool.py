from concurrent import futures
import sys
import requests
import countryflags as cf
import time

from getsequential import fetch

DEFAULT_NUM_THREADS = 100
GLOBAL_TIMEOUT = 300  # seconds

times = {}

def main(source, num_threads):
    pool = futures.ThreadPoolExecutor(num_threads)
    pending = {}
    t0 = time.time()
    # submit all jobs
    for iso_cc in sorted(cf.cc2name):
        print('get:', iso_cc)
        times[iso_cc] = [time.time() - t0]
        job = pool.submit(fetch, iso_cc, source)
        pending[job] = iso_cc
    to_download = len(pending)
    downloaded = 0
    # get results as jobs are done
    for job in futures.as_completed(pending, timeout=GLOBAL_TIMEOUT):
        try:
            octets, file_name = job.result()
            times[pending[job]].append(time.time() - t0)
            downloaded += 1
            print('\t--> {}: {:5d} bytes'.format(file_name, octets))
        except Exception as exc:
            print('\t***', pending[job], 'generated an exception:', exc)
    ratio = downloaded / to_download
    print('{} of {} downloaded ({:.1%})'.format(downloaded, to_download, ratio))
    for iso_cc in sorted(times):
        start, end = times[iso_cc]
        print('{}\t{:.6g}\t{:.6g}'.format(iso_cc, start, end))

if __name__ == '__main__':
    import argparse

    source_names = ', '.join(sorted(cf.SOURCE_URLS))
    parser = argparse.ArgumentParser(description='Download flag images.')
    parser.add_argument('source', help='one of: ' + source_names)
    parser.add_argument('-t', '--threads', type=int, default=DEFAULT_NUM_THREADS,
                   help='number of threads (default: %s)' % DEFAULT_NUM_THREADS)

    args = parser.parse_args()
    main(args.source, args.threads)

"""
From CIA, 1 thread:
real    2m0.832s
user    0m4.685s
sys     0m0.366s



"""
