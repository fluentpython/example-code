"""
record_factory: create simple classes just for holding data fields

# BEGIN RECORD_FACTORY_DEMO
    >>> Dog = record_factory('Dog', 'name weight owner')  # <1>
    >>> rex = Dog('Rex', 30, 'Bob')
    >>> rex  # <2>
    Dog(name='Rex', weight=30, owner='Bob')
    >>> name, weight, _ = rex  # <3>
    >>> name, weight
    ('Rex', 30)
    >>> "{2}'s dog weights {1}kg".format(*rex)
    "Bob's dog weights 30kg"
    >>> rex.weight = 32  # <4>
    >>> rex
    Dog(name='Rex', weight=32, owner='Bob')
    >>> Dog.__mro__  # <5>
    (<class 'factories.Dog'>, <class 'object'>)

# END RECORD_FACTORY_DEMO
"""

# BEGIN RECORD_FACTORY
def record_factory(cls_name, field_names):
    if isinstance(field_names, str):  # <1>
        field_names = field_names.replace(',', ' ').split()
    __slots__ = tuple(field_names)

    def __init__(self, *args, **kwargs):
        attrs = dict(zip(self.__slots__, args))
        attrs.update(kwargs)
        for name, value in attrs.items():
            setattr(self, name, value)

    def __iter__(self):
        for name in self.__slots__:
            yield getattr(self, name)

    def __repr__(self):
        values = ', '.join('{}={!r}'.format(*i) for i
                           in zip(self.__slots__, self))
        return '{}({})'.format(self.__class__.__name__, values)

    cls_attrs = dict(__slots__ = __slots__,
                     __init__ = __init__,
                     __iter__ = __iter__,
                     __repr__ = __repr__)

    return type(cls_name, (object,), cls_attrs)
# END RECORD_FACTORY
