# adaptado de:
# https://github.com/feihong/tulip-talk/blob/master/examples/2-tulip-download.py

import asyncio
import aiohttp

@asyncio.coroutine
def download(url):
    response = yield from aiohttp.request('GET', url)
    for k, v in response.items():
        print('{}: {}'.format(k, v[:80]))

    data = yield from response.read()
    print('\nReceived {} bytes.\n'.format(len(data)))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    url = 'https://www.cia.gov/library/publications/the-world-factbook/geos/br.html'
    coroutine = download(url)
    loop.run_until_complete(coroutine)
