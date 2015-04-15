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

The check is also performed on instantiation::

    >>> walnuts = LineItem('walnuts', 0, 10.00)
    Traceback (most recent call last):
        ...
    ValueError: value must be > 0

The proteced attribute can still be accessed if needed for some reason, such as
white box testing)::

    >>> raisins._LineItem__weight
    10

"""


# BEGIN LINEITEM_V2B
class LineItem:

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    def get_weight(self):  # <1>
        return self.__weight

    def set_weight(self, value):  # <2>
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('value must be > 0')

    weight = property(get_weight, set_weight)  # <3>

# END LINEITEM_V2B
