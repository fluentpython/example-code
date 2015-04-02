"""
>>> avg = make_averager()
>>> avg(10)
Traceback (most recent call last):
  ...
UnboundLocalError: local variable 'num_items' referenced before assignment

"""


def make_averager():
    num_items = 0
    total = 0

    def averager(new_value):
        num_items += 1
        total += new_value
        return total / num_items

    return averager
