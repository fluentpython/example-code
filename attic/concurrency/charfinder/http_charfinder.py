#!/usr/bin/env python3

import sys
import asyncio
from aiohttp import web

from charfinder import UnicodeNameIndex

PAGE_TPL = '''
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Charserver</title>
  </head>
  <body>
    <p>
        <form action="/">
          <input type="search" name="query" value="{query}">
          <input type="submit" value="find">
        Examples: {links}
        </form>
    </p>
    <p>{message}</p>
    <hr>
  <table>
{result}
  </table>
  </body>
</html>
'''

EXAMPLE_WORDS = ('bismillah chess cat circled Malayalam digit Roman face Ethiopic'
                 ' black mark symbol dot operator Braille hexagram').split()

LINK_TPL = '<a href="/?query={0}" title="find &quot;{0}&quot;">{0}</a>'

LINKS_HTML =  ', '.join(LINK_TPL.format(word)
                        for word in sorted(EXAMPLE_WORDS, key=str.upper))

ROW_TPL = '<tr><td>{code_str}</td><th>{char}</th><td>{name}</td></tr>'

CONTENT_TYPE = 'text/html; charset=UTF-8'

index = None  # a UnicodeNameIndex instance


@asyncio.coroutine
def handle(request):
    query = request.GET.get('query', '')
    print('Query: {!r}'.format(query))
    if query:
        descriptions = list(index.find_descriptions(query))
        res = '\n'.join(ROW_TPL.format(**vars(descr))
                        for descr in descriptions)
        msg = index.status(query, len(descriptions))
    else:
        descriptions = []
        res = ''
        msg = 'Type words describing characters.'

    text = PAGE_TPL.format(query=query, result=res,
                           message=msg, links=LINKS_HTML)
    print('Sending {} results'.format(len(descriptions)))
    return web.Response(content_type=CONTENT_TYPE, text=text)


@asyncio.coroutine
def init(loop, address, port):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', handle)

    server = yield from loop.create_server(app.make_handler(),
                                           address, port)
    host = server.sockets[0].getsockname()
    print('Serving on {}. Hit CTRL-C to stop.'.format(host))


def main(address="127.0.0.1", port=8888):
    port = int(port)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop, address, port))
    loop.run_forever()


if __name__ == '__main__':
    index = UnicodeNameIndex()
    main(*sys.argv[1:])
