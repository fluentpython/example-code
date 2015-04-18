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

The value of the attributes managed by the descriptors are stored in
alternate attributes, created by the descriptors in each ``LineItem``
instance::

    >>> raisins = LineItem('Golden raisins', 10, 6.95)
    >>> dir(raisins)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    ['_NonBlank#0', '_Quantity#0', '_Quantity#1', '__class__', ...
     'description', 'price', 'subtotal', 'weight']
    >>> getattr(raisins, '_Quantity#0')
    10
    >>> getattr(raisins, '_NonBlank#0')
    'Golden raisins'

If the descriptor is accessed in the class, the descriptor object is
returned:

    >>> LineItem.weight  # doctest: +ELLIPSIS
    <model_v5.Quantity object at 0x...>
    >>> LineItem.weight.storage_name
    '_Quantity#0'

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


"""

# BEGIN LINEITEM_V5
import model_v5 as model  # <1>


class LineItem:
    description = model.NonBlank()  # <2>
    weight = model.Quantity()
    price = model.Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price
# END LINEITEM_V5
