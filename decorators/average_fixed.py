"""
>>> avg = make_averager()
>>> other_avg = make_averager()
>>> avg(10)
10.0
>>> avg(11)
10.5
>>> avg(12)
11.0
>>> avg.__code__.co_varnames
('new_value',)
>>> avg.__code__.co_freevars
('num_items', 'total')
>>> avg.__closure__  # doctest: +ELLIPSIS
(<cell at 0x...: int object at 0x...>, <cell at 0x...: int object at 0x...>)
>>> avg.__closure__[0].cell_contents
3
>>> avg.__closure__[1].cell_contents
33
>>> other_avg(5)
5.0
>>> other_avg(10)
7.5
>>> other_avg(15)
10.0
"""

DEMO = """
>>> avg.__closure__
(<cell at 0x10fd24f78: int object at 0x10f6d3db0>,
 <cell at 0x10fd24d38: int object at 0x10f6d4170>)
"""


def make_averager():
    num_items = 0
    total = 0

    def averager(new_value):
        nonlocal num_items, total
        num_items += 1
        total += new_value
        return total / num_items

    return averager
