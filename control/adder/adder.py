import sys


def ask():
    prompt = '>'
    while True:
        response = input(prompt)
        if not response:
            return 0
        yield response


def parse_args():
    yield from iter(sys.argv[1:])


def fetch(producer):
    gen = producer()
    next(gen)
    yield from gen


def main(args):
    if args:
        producer = parse_args
    else:
        producer = ask

    total = 0
    count = 0
    gen = fetch(producer())
    while True:
        term = yield from gen
        term = float(term)
        total += term
        count += 1
        average = total / count
        print('total: {}  average: {}'.format(total, average))


if __name__ == '__main__':
    main(sys.argv[1:])
