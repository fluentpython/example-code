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
    [... '_quantity:0', '_quantity:1', 'description',
    'price', 'subtotal', 'weight']
    >>> getattr(raisins, '_quantity:0')
    10
    >>> getattr(raisins, '_quantity:1')
    6.95

"""


# BEGIN LINEITEM_V4_PROP
def quantity():  # <1>
    try:
        quantity.counter += 1  # <2>
    except AttributeError:
        quantity.counter = 0  # <3>

    storage_name = '_{}:{}'.format('quantity', quantity.counter)  # <4>

    def qty_getter(instance):  # <5>
        return getattr(instance, storage_name)

    def qty_setter(instance, value):
        if value > 0:
            setattr(instance, storage_name, value)
        else:
            raise ValueError('value must be > 0')

    return property(qty_getter, qty_setter)
# END LINEITEM_V4_PROP

class LineItem:
    weight = quantity()
    price = quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

