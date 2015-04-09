# BEGIN ARITPROG_ITERTOOLS
import itertools


def aritprog_gen(begin, step, end=None):
    if end is not None and begin >= end:
        return
    yield type(begin + step)(begin)
    tail_gen = itertools.count(begin+step, step)
    if end is not None:
        tail_gen = itertools.takewhile(lambda n: n < end, tail_gen)
    for x in tail_gen:
        yield x
# END ARITPROG_ITERTOOLS
