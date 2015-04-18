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
    ['_Quantity#0', '_Quantity#1', '__class__', ...
     'description', 'price', 'subtotal', 'weight']
    >>> getattr(raisins, '_Quantity#0')
    10
    >>> getattr(raisins, '_Quantity#1')
    6.95

"""


# BEGIN LINEITEM_V4
class Quantity:
    __counter = 0  # <1>

    def __init__(self):
        cls = self.__class__  # <2>
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(prefix, index)  # <3>
        cls.__counter += 1  # <4>

    def __get__(self, instance, owner):  # <5>
        return getattr(instance, self.storage_name)  # <6>

    def __set__(self, instance, value):
        if value > 0:
            setattr(instance, self.storage_name, value)  # <7>
        else:
            raise ValueError('value must be > 0')


class LineItem:
    weight = Quantity()  # <8>
    price = Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price
# END LINEITEM_V4
