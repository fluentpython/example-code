"""
>>> avg = make_averager()
>>> avg(10)
10.0
>>> avg(11)
10.5
>>> avg(12)
11.0
>>> avg.__code__.co_varnames
('new_value',)
>>> avg.__code__.co_freevars
('ns',)
>>> avg.__closure__  # doctest: +ELLIPSIS
(<cell at 0x...: Namespace object at 0x...>,)
>>> avg.__closure__[0].cell_contents.__dict__
{'total': 33, 'num_items': 3}
"""

DEMO = """
>>> avg.__closure__
(<cell at 0x108df5980: Namespace object at 0x108e06790>,)
"""


class Namespace(object):
    pass


def make_averager():
    ns = Namespace()
    ns.num_items = 0
    ns.total = 0

    def averager(new_value):
        ns.num_items += 1
        ns.total += new_value
        return float(ns.total) / ns.num_items

    return averager
