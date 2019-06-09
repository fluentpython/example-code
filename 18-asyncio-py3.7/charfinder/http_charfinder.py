import asyncio
from aiohttp import web
import sys

from charfinder import UnicodeNameIndex

TEMPATE_NAME = 'http_charfinder.html'

CONTENT_TYPE = 'text/html'
SAMPLE_WORDS = ('bismillah chess cat circled Malayalam digit'
                ' Roman face Ethiopic black mark symbol dot'
                ' operator Braille hexagram').split()

ROW_TPL = '<tr><td>{code_str}</td><th>{char}</th><td>{name}</td></tr>'
LINK_TPL = '<a href="/?query={0}" title="find &quot;{0}&quot;">{0}</a>'
LINKS_HTML = ', '.join(LINK_TPL.format(word) for word in
                       sorted(SAMPLE_WORDS, key=str.upper))

index = UnicodeNameIndex()

with open(TEMPATE_NAME) as tpl:
    template = tpl.read()
template = template.replace('{links}', LINKS_HTML)

def home(request):
    query = request.path_qs[8:].strip()
    print('Query: {!r}'.format(query))
    if query:
        descriptions = list(index.find_descriptions(query))
        res = ''
        for r in [desc for desc in descriptions]: res += ROW_TPL.format(code_str=r.code_str, char=r.char, name=r.name) + '\n'
        msg = index.status(query, len(descriptions))
    else:
        descriptions = []
        res = ''
        msg = 'Enter words describing characters.'

    html = template.format(query=query, result=res, message=msg)
    print('Sending {} results'.format(len(descriptions)))
    return web.Response(content_type=CONTENT_TYPE, text=html)

async def init(loop, address, port):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', home)
    handler = app.make_handler()
    server = await loop.create_server(handler, address, port)
    return server.sockets[0].getsockname()

def main(address='127.0.0.1', port=8888):
    port = int(port)
    loop = asyncio.get_event_loop()
    host = loop.run_until_complete(init(loop, address, port))
    print('Serving on {}. Hit CRTL-C to stop.'.format(host))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    print('Server shutting down.')
    loop.close()

if __name__ == "__main__":
    main(*sys.argv[1:])
