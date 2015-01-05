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


"""


# BEGIN LINEITEM_V2_PROP
def quantity(storage_name):  # <1>

    @property  # <2>
    def new_prop(self):
        return self.__dict__[storage_name]  # <3>

    @new_prop.setter
    def new_prop(self, value):
        if value > 0:
            self.__dict__[storage_name] = value  # <4>
        else:
            raise ValueError('value must be > 0')

    return new_prop  # <5>


class LineItem:
    weight = quantity('weight')  # <6>
    price = quantity('price')  # <7>

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price
# END LINEITEM_V2_PROP
