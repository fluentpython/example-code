import asyncio
from aiohttp import web

from charfinder import UnicodeNameIndex

TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>title</title>
  </head>
  <body>
    <form action="/">
      <input type="search" name="query" value="{query}">
      <input type="submit" value="find">
    </form>
    <p>{message}</p>
    <hr>
  <pre>
{result}
  </pre>
  </body>
</html>
'''

CONTENT_TYPE = 'text/html; charset=UTF-8'

index = None  # a UnicodeNameIndex instance


@asyncio.coroutine
def handle(request):
    query = request.GET.get('query', '')
    print('Query: {!r}'.format(query))
    if query:
        lines = list(index.find_descriptions(query))
        res = '\n'.join(lines)
        plural = 'es' if len(lines) > 1 else ''
        msg = '{} match{} for {!r}'.format(len(lines), plural, query)
    else:
        lines = []
        res = ''
        msg = 'Type words describing characters, e.g. chess.'

    text = TEMPLATE.format(query=query, result=res, message=msg)
    return web.Response(content_type=CONTENT_TYPE, text=text)


@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', handle)

    server = yield from loop.create_server(app.make_handler(),
                                           '127.0.0.1', 8080)
    host = server.sockets[0].getsockname()
    print('Serving on {}. Hit CTRL-C to stop.'.format(host))


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()


if __name__ == '__main__':
    index = UnicodeNameIndex()
    main()
