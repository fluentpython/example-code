import requests
import countryflags as cf
import time


times = {}

def fetch(iso_cc, source):
    resp = requests.get(cf.flag_url(iso_cc, source))
    if resp.status_code != 200:
        resp.raise_for_status()
    file_name = cf.iso_file_name(iso_cc)
    with open(file_name, 'wb') as img:
        written = img.write(resp.content)
    return written, file_name

def main(source):
    pending = sorted(cf.cc2name)
    to_download = len(pending)
    downloaded = 0
    t0 = time.time()
    for iso_cc in pending:
        print('get:', iso_cc)
        try:
            times[iso_cc] = [time.time() - t0]
            octets, file_name = fetch(iso_cc, source)
            times[iso_cc].append(time.time() - t0)
            downloaded += 1
            print('\t--> {}: {:5d} bytes'.format(file_name, octets))
        except Exception as exc:
            print('\t***', iso_cc, 'generated an exception:', exc)
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

    args = parser.parse_args()
    main(args.source)

"""
From cia.gov:
real    3m26.679s
user    0m5.212s
sys     0m0.383s

From localhost nginx:
real    0m1.193s
user    0m0.858s
sys     0m0.179s

From localhost nginx via Vaurien with .5s delay
real    1m40.519s
user    0m1.103s
sys     0m0.243s
"""
