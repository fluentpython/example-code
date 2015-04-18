#!/usr/bin/env python3

import sys
import asyncio

from charfinder import UnicodeNameIndex

CRLF = b'\r\n'
PROMPT = b'?> '

index = None  # a UnicodeNameIndex instance


@asyncio.coroutine
def handle_queries(reader, writer):
    while True:
        writer.write(PROMPT)  # can't yield from!
        yield from writer.drain()  # must yield from!
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
            lines = list(index.find_description_strs(query))
            if lines:
                writer.writelines(line.encode() + CRLF for line in lines)
            writer.write(index.status(query, len(lines)).encode() + CRLF)

            yield from writer.drain()
            print('Sent {} results'.format(len(lines)))

    print('Close the client socket')
    writer.close()


def main(address='127.0.0.1', port=8888):
    port = int(port)
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_queries, address, port, loop=loop)
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
    main(*sys.argv[1:])
