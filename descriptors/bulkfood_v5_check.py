"""

A line item for a bulk food order has description, weight and price fields::

    >>> raisins = LineItem('Golden raisins', 10, 6.95)
    >>> raisins.weight, raisins.description, raisins.price
    (10, 'Golden raisins', 6.95)

A ``subtotal`` method gives the total price for that line item::

    >>> raisins.subtotal()
    69.5

The weight of a ``LineItem`` must be greater than 0::

    >>> raisins.weight = -20
    Traceback (most recent call last):
        ...
    ValueError: value must be > 0; -20 is not valid.

No change was made::

    >>> raisins.weight
    10

The value of the attributes managed by the descriptors are stored in
alternate attributes, created by the descriptors in each ``LineItem``
instance::

    >>> raisins = LineItem('Golden raisins', 10, 6.95)
    >>> dir(raisins)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    ['_Check#0', '_Check#1', '_Check#2', '__class__', ...
     'description', 'price', 'subtotal', 'weight']
    >>> [getattr(raisins, name) for name in dir(raisins) if name.startswith('_Check#')]
    ['Golden raisins', 10, 6.95]

If the descriptor is accessed in the class, the descriptor object is
returned:

    >>> LineItem.weight  # doctest: +ELLIPSIS
    <model_v5_check.Check object at 0x...>
    >>> LineItem.weight.storage_name
    '_Check#1'

The `NonBlank` descriptor prevents empty or blank strings to be used
for the description:

    >>> br_nuts = LineItem('Brazil Nuts', 10, 34.95)
    >>> br_nuts.description = ' '
    Traceback (most recent call last):
        ...
    ValueError: ' ' is not valid.
    >>> void = LineItem('', 1, 1)
    Traceback (most recent call last):
        ...
    ValueError: '' is not valid.



"""

import model_v5_check as model

def gt_zero(x):
    '''value must be > 0'''
    return x if x > 0 else model.INVALID

def non_blank(txt):
    txt = txt.strip()
    return txt if txt else model.INVALID


class LineItem:
    description = model.Check(non_blank)
    weight = model.Check(gt_zero)
    price = model.Check(gt_zero)

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

