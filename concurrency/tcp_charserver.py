#!/usr/bin/env python3

import asyncio

from charfinder import UnicodeNameIndex

CRLF = b'\r\n'
PROMPT = b'?> '

index = None  # a UnicodeNameIndex instance


def writeln(writer, arg):
    if isinstance(arg, str):
        lines = [arg]
    else:
        lines = arg
    writer.writelines(line.encode() + CRLF for line in lines)


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
        if ord(query[:1]) < 32:
            break
        client = writer.get_extra_info('peername')
        print('Received from {}: {}'.format(client, query))
        lines = list(index.find_descriptions(query))
        if lines:
            writeln(writer, lines)
            plural = 'es' if len(lines) > 1 else ''
            msg = '({} match{} for {!r})'.format(len(lines), plural, query)
            writeln(writer, msg)
            print('Sent: {} lines + total'.format(len(lines)))
        else:
            writeln(writer, '(No match for {!r})'.format(query))
            print('Sent: 1 line, no match')
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
