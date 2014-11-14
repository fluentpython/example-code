from concurrent import futures
import sys
import requests
import countryflags as cf
import time

from getsequential import fetch

DEFAULT_NUM_THREADS = 100
GLOBAL_TIMEOUT = 300  # seconds

times = {}

def main(num_threads):
    pool = futures.ThreadPoolExecutor(num_threads)
    pending = {}
    t0 = time.time()
    # submit all jobs
    for iso_cc in sorted(cf.cc2name):
        print('get:', iso_cc)
        times[iso_cc] = [time.time() - t0]
        job = pool.submit(fetch, iso_cc)
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
    if len(sys.argv) == 2:
        num_threads = int(sys.argv[1])
    else:
        num_threads = DEFAULT_NUM_THREADS
    main(num_threads)

"""
From localhost nginx:
real    0m1.163s
user    0m1.001s
sys     0m0.289s



"""