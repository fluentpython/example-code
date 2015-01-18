

"""
Overriding descriptor (a.k.a. data descriptor or enforced descriptor):

    >>> obj = Model()
    >>> obj.over  # doctest: +ELLIPSIS
    Overriding.__get__() invoked with args:
        self     = <descriptorkinds.Overriding object at 0x...>
        instance = <descriptorkinds.Model object at 0x...>
        owner    = <class 'descriptorkinds.Model'>
    >>> Model.over  # doctest: +ELLIPSIS
    Overriding.__get__() invoked with args:
        self     = <descriptorkinds.Overriding object at 0x...>
        instance = None
        owner    = <class 'descriptorkinds.Model'>


An overriding descriptor cannot be shadowed by assigning to an instance:

    >>> obj = Model()
    >>> obj.over = 7  # doctest: +ELLIPSIS
    Overriding.__set__() invoked with args:
        self     = <descriptorkinds.Overriding object at 0x...>
        instance = <descriptorkinds.Model object at 0x...>
        value    = 7
    >>> obj.over  # doctest: +ELLIPSIS
    Overriding.__get__() invoked with args:
        self     = <descriptorkinds.Overriding object at 0x...>
        instance = <descriptorkinds.Model object at 0x...>
        owner    = <class 'descriptorkinds.Model'>


Not even by poking the attribute into the instance ``__dict__``:

    >>> obj.__dict__['over'] = 8
    >>> obj.over  # doctest: +ELLIPSIS
    Overriding.__get__() invoked with args:
        self     = <descriptorkinds.Overriding object at 0x...>
        instance = <descriptorkinds.Model object at 0x...>
        owner    = <class 'descriptorkinds.Model'>
    >>> vars(obj)
    {'over': 8}

Overriding descriptor without ``__get__``:

    >>> obj.over_no_get  # doctest: +ELLIPSIS
    <descriptorkinds.OverridingNoGet object at 0x...>
    >>> Model.over_no_get   # doctest: +ELLIPSIS
    <descriptorkinds.OverridingNoGet object at 0x...>
    >>> obj.over_no_get = 7  # doctest: +ELLIPSIS
    OverridingNoGet.__set__() invoked with args:
        self     = <descriptorkinds.OverridingNoGet object at 0x...>
        instance = <descriptorkinds.Model object at 0x...>
        value    = 7
    >>> obj.over_no_get  # doctest: +ELLIPSIS
    <descriptorkinds.OverridingNoGet object at 0x...>


Poking the attribute into the instance ``__dict__`` means you can read the new
value for the attribute, but setting it still triggers ``__set__``:

    >>> obj.__dict__['over_no_get'] = 9
    >>> obj.over_no_get
    9
    >>> obj.over_no_get = 7  # doctest: +ELLIPSIS
    OverridingNoGet.__set__() invoked with args:
        self     = <descriptorkinds.OverridingNoGet object at 0x...>
        instance = <descriptorkinds.Model object at 0x...>
        value    = 7
    >>> obj.over_no_get
    9


Non-overriding descriptor (a.k.a. non-data descriptor or shadowable descriptor):

    >>> obj = Model()
    >>> obj.non_over  # doctest: +ELLIPSIS
    NonOverriding.__get__() invoked with args:
        self     = <descriptorkinds.NonOverriding object at 0x...>
        instance = <descriptorkinds.Model object at 0x...>
        owner    = <class 'descriptorkinds.Model'>
    >>> Model.non_over  # doctest: +ELLIPSIS
    NonOverriding.__get__() invoked with args:
        self     = <descriptorkinds.NonOverriding object at 0x...>
        instance = None
        owner    = <class 'descriptorkinds.Model'>


A non-overriding descriptor can be shadowed by assigning to an instance:

    >>> obj.non_over = 7
    >>> obj.non_over
    7


Methods are non-over descriptors:

    >>> obj.spam  # doctest: +ELLIPSIS
    <bound method Model.spam of <descriptorkinds.Model object at 0x...>>
    >>> Model.spam  # doctest: +ELLIPSIS
    <function Model.spam at 0x...>
    >>> obj.spam()  # doctest: +ELLIPSIS
    Model.spam() invoked with arg:
        self = <descriptorkinds.Model object at 0x...>
    >>> obj.spam = 7
    >>> obj.spam
    7


No descriptor type survives being overwritten on the class itself:

    >>> Model.over = 1
    >>> obj.over
    1
    >>> Model.over_no_get = 2
    >>> obj.over_no_get
    2
    >>> Model.non_over = 3
    >>> obj.non_over
    7

"""

# BEGIN DESCRIPTORKINDS
def print_args(name, *args):  # <1>
    cls_name = args[0].__class__.__name__
    arg_names = ['self', 'instance', 'owner']
    if name == 'set':
        arg_names[-1] = 'value'
    print('{}.__{}__() invoked with args:'.format(cls_name, name))
    for arg_name, value in zip(arg_names, args):
        print('    {:8} = {}'.format(arg_name, value))


class Overriding:  # <2>
    """a.k.a. data descriptor or enforced descriptor"""

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)  # <3>

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class OverridingNoGet:  # <4>
    """an overriding descriptor without ``__get__``"""

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class NonOverriding:  # <5>
    """a.k.a. non-data or shadowable descriptor"""

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)


class Model:  # <6>
    over = Overriding()
    over_no_get = OverridingNoGet()
    non_over = NonOverriding()

    def spam(self):  # <7>
        print('Model.spam() invoked with arg:')
        print('    self =', self)

#END DESCRIPTORKINDS
