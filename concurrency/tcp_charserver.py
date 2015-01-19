#!/usr/bin/env python3

import asyncio

from charfinder import UnicodeNameIndex

CRLF = b'\r\n'
PROMPT = b'?> '

index = None  # a UnicodeNameIndex instance


@asyncio.coroutine
def handle_queries(reader, writer):
    while True:
        writer.write(PROMPT)
        yield from writer.drain()
        data = yield from reader.readline()
        try:
            query = data.decode().strip()
        except UnicodeDecodeError:
            query = '\x00'
        client = writer.get_extra_info('peername')
        print('Received from {}: {!r}'.format(client, query))
        if query:
            if ord(query[:1]) < 32:
                break
            lines = list(index.find_descriptions(query))
            if lines:
                writer.writelines(line.encode() + CRLF for line in lines)
            writer.write(index.status(query, len(lines)).encode() + CRLF)
            yield from writer.drain()

    print('Close the client socket')
    writer.close()


def main():
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_queries, '127.0.0.1', 8888, loop=loop)
    server = loop.run_until_complete(coro)

    host = server.sockets[0].getsockname()
    print('Serving on {}. Hit CTRL-C to stop.'.format(host))
    try:
        loop.run_forever()
    except KeyboardInterrupt:  # CTRL+C pressed
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    index = UnicodeNameIndex()
    main()
