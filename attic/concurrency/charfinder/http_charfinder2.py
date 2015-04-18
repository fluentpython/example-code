#!/usr/bin/env python3

import sys
import asyncio
import urllib
import json
from aiohttp import web

from charfinder import UnicodeNameIndex

PAGE_TPL = '''
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Charserver</title>
    <script type="text/javascript">
    function onclick() {
      var table = document.getElementById("results");
      for (var char in "ABCDE") {
        code = char.charCodeAt(0);
        var tr = document.createElement('tr');
        tr.appendChild(document.createElement('td'));
        tr.appendChild(document.createElement('th'));
        var code_str = 'U+'+code.toString(16);
        tr.cells[0].appendChild(document.createTextNode(code_str));
        tr.cells[1].appendChild(document.createTextNode(char));
      }
    }
    </script>
  </head>
  <body>
    <p>
        <form action="/">
          <input type="search" name="query" value="">
          <input type="submit" value="find" onclick="fillTable()">
        Examples: {links}
        </form>
    </p>
    <p>{message}</p>
    <hr>
  <table id="results">
  </table>
  </body>
</html>
'''

EXAMPLE_WORDS = ('bismillah chess cat circled Malayalam digit Roman face Ethiopic'
                 ' black mark symbol dot operator Braille hexagram').split()

LINK_TPL = '<a href="/?query={0}" title="find &quot;{0}&quot;">{0}</a>'

LINKS_HTML =  ', '.join(LINK_TPL.format(word)
                        for word in sorted(EXAMPLE_WORDS, key=str.upper))

ROW_TPL = '<tr id="{code_str}"><td>{code_str}</td><th>{char}</th><td>{name}</td></tr>'

HTML_TYPE = 'text/html; charset=UTF-8'
TEXT_TYPE = 'text/plain; charset=UTF-8'

RESULTS_PER_REQUEST = 15

index = None  # a UnicodeNameIndex instance


@asyncio.coroutine
def form(request):
    peername = request.transport.get_extra_info('peername')
    print('Request from: {}, query: {!r}'.format(peername, request.path_qs))
    msg = 'Type words describing characters.'
    text = PAGE_TPL.format(message=msg, links=LINKS_HTML)
    return web.Response(content_type=HTML_TYPE, text=text)


@asyncio.coroutine
def get_chars(request):
    peername = request.transport.get_extra_info('peername')
    print('Request from: {}, GET data: {!r}'.format(peername, dict(request.GET)))
    query = request.GET.get('query', '')
    if query:
        try:
            start = int(request.GET.get('start', 0))
            stop = int(request.GET.get('stop', sys.maxsize))
        except ValueError:
            raise web.HTTPBadRequest()
        stop = min(stop, start+RESULTS_PER_REQUEST)
        num_results, chars = index.find_chars(query, start, stop)
    else:
        raise web.HTTPBadRequest()
    text = ''.join(char if n % 64 else char+'\n'
            for n, char in enumerate(chars, 1))
    response_data = {'total': num_results, 'start': start, 'stop': stop}
    print('Response to query: {query!r}, start: {start}, stop: {stop}'.format(
          query=query, **response_data))
    response_data['chars'] = text
    json_obj = json.dumps(response_data)
    print('Sending {} characters'.format(len(text)))
    headers = {'Access-Control-Allow-Origin': '*'}
    return web.Response(content_type=TEXT_TYPE, headers=headers, text=json_obj)


@asyncio.coroutine
def init(loop, address, port):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/chars', get_chars)
    app.router.add_route('GET', '/', form)

    server = yield from loop.create_server(app.make_handler(),
                                           address, port)
    host = server.sockets[0].getsockname()
    print('Serving on {}. Hit CTRL-C to stop.'.format(host))


def main(address="127.0.0.1", port=8888):
    port = int(port)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop, address, port))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Stopped.')


if __name__ == '__main__':
    index = UnicodeNameIndex()
    main(*sys.argv[1:])
