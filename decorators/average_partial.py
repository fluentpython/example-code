"""
>>> import functools
>>> avg = functools.partial(averager, series=[])
>>> avg(10)
10.0
>>> avg(11)
10.5
>>> avg(12)
11.0
>>> avg.args
()
>>> avg.keywords
{'series': [10, 11, 12]}
>>> avg.func            # doctest: +ELLIPSIS
<function averager at 0x...>
>>> avg.func.__code__.co_varnames
('new_value', 'series', 'total')
"""

DEMO = """
>>> avg.func
<function averager at 0x1010c5560>
>>> avg.func.__code__.co_varnames
('new_value',)
>>> avg.__code__.co_freevars
('num_items', 'total')
>>> avg.__closure__
"""

def averager(new_value, series):
    series.append(new_value)
    total = sum(series)
    return float(total)/len(series)

