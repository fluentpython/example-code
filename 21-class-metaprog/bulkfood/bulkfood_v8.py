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
    ValueError: value must be > 0

No change was made::

    >>> raisins.weight
    10

    >>> raisins = LineItem('Golden raisins', 10, 6.95)
    >>> dir(raisins)[:3]
    ['_NonBlank#description', '_Quantity#price', '_Quantity#weight']
    >>> LineItem.description.storage_name
    '_NonBlank#description'
    >>> raisins.description
    'Golden raisins'
    >>> getattr(raisins, '_NonBlank#description')
    'Golden raisins'

If the descriptor is accessed in the class, the descriptor object is
returned:

    >>> LineItem.weight  # doctest: +ELLIPSIS
    <model_v8.Quantity object at 0x...>
    >>> LineItem.weight.storage_name
    '_Quantity#weight'


The `NonBlank` descriptor prevents empty or blank strings to be used
for the description:

    >>> br_nuts = LineItem('Brazil Nuts', 10, 34.95)
    >>> br_nuts.description = ' '
    Traceback (most recent call last):
        ...
    ValueError: value cannot be empty or blank
    >>> void = LineItem('', 1, 1)
    Traceback (most recent call last):
        ...
    ValueError: value cannot be empty or blank


Fields can be retrieved in the order they were declared:

# BEGIN LINEITEM_V8_DEMO
    >>> for name in LineItem.field_names():
    ...     print(name)
    ...
    description
    weight
    price

# END LINEITEM_V8_DEMO

"""

import model_v8 as model

class LineItem(model.Entity):
    description = model.NonBlank()
    weight = model.Quantity()
    price = model.Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price
