import sys
import collections

Result = collections.namedtuple('Result', 'total average')

def adder():
    total = 0
    count = 0
    while True:
        term = yield
        try:
            term = float(term)
        except (ValueError, TypeError):
            break
        else:
            total += term
            count += 1
    return Result(total, total/count)

def process_args(coro, args):
    for arg in args:
        coro.send(arg)
    try:
        next(coro)
    except StopIteration as exc:
        return exc.value


def prompt(coro):
    while True:
        term = input('+> ')
        try:
            coro.send(term)
        except StopIteration as exc:
            return exc.value


def main():
    coro = adder()
    next(coro)  # prime it
    if len(sys.argv) > 1:
        res = process_args(coro, sys.argv[1:])
    else:
        res = prompt(coro)
    print(res)

main()
