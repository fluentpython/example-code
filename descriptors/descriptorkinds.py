

"""
Data descriptor (a.k.a. overriding or enforced descriptor):

    >>> o = Model()
    >>> o.data  # doctest: +ELLIPSIS
    DataDescriptor.__get__() invoked with args:
        self     =  <descriptorkinds.DataDescriptor object at 0x...>
        instance =  <descriptorkinds.Model object at 0x...>
        owner    =  <class 'descriptorkinds.Model'>
    >>> Model.data  # doctest: +ELLIPSIS
    DataDescriptor.__get__() invoked with args:
        self     =  <descriptorkinds.DataDescriptor object at 0x...>
        instance =  None
        owner    =  <class 'descriptorkinds.Model'>


A data descriptor cannot be shadowed by assigning to an instance:

    >>> o.data = 7  # doctest: +ELLIPSIS
    DataDescriptor.__set__() invoked with args:
        self     =  <descriptorkinds.DataDescriptor object at 0x...>
        instance =  <descriptorkinds.Model object at 0x...>
        value    =  7
    >>> o.data  # doctest: +ELLIPSIS
    DataDescriptor.__get__() invoked with args:
        self     =  <descriptorkinds.DataDescriptor object at 0x...>
        instance =  <descriptorkinds.Model object at 0x...>
        owner    =  <class 'descriptorkinds.Model'>


Not even by poking the attribute into the instance ``__dict__``:

    >>> o.__dict__['data'] = 8
    >>> o.data  # doctest: +ELLIPSIS
    DataDescriptor.__get__() invoked with args:
        self     =  <descriptorkinds.DataDescriptor object at 0x...>
        instance =  <descriptorkinds.Model object at 0x...>
        owner    =  <class 'descriptorkinds.Model'>


Data descriptor without ``__get__``:

    >>> o.data_no_get  # doctest: +ELLIPSIS
    <descriptorkinds.DataDescriptorNoGet object at 0x...>
    >>> Model.data_no_get   # doctest: +ELLIPSIS
    <descriptorkinds.DataDescriptorNoGet object at 0x...>
    >>> o.data_no_get = 7  # doctest: +ELLIPSIS
    DataDescriptorNoGet.__set__() invoked with args:
        self     =  <descriptorkinds.DataDescriptorNoGet object at 0x...>
        instance =  <descriptorkinds.Model object at 0x...>
        value    =  7
    >>> o.data_no_get  # doctest: +ELLIPSIS
    <descriptorkinds.DataDescriptorNoGet object at 0x...>


Poking the attribute into the instance ``__dict__`` means you can read the new
value for the attribute, but setting it still triggers ``__set__``:

    >>> o.__dict__['data_no_get'] = 8
    >>> o.data_no_get
    8
    >>> o.data_no_get = 7  # doctest: +ELLIPSIS
    DataDescriptorNoGet.__set__() invoked with args:
        self     =  <descriptorkinds.DataDescriptorNoGet object at 0x...>
        instance =  <descriptorkinds.Model object at 0x...>
        value    =  7
    >>> o.data_no_get  # doctest: +ELLIPSIS
    8


Non-data descriptor (a.k.a. non-overriding or shadowable descriptor):

    >>> o = Model()
    >>> o.non_data  # doctest: +ELLIPSIS
    NonDataDescriptor.__get__() invoked with args:
        self     =  <descriptorkinds.NonDataDescriptor object at 0x...>
        instance =  <descriptorkinds.Model object at 0x...>
        owner    =  <class 'descriptorkinds.Model'>
    >>> Model.non_data  # doctest: +ELLIPSIS
    NonDataDescriptor.__get__() invoked with args:
        self     =  <descriptorkinds.NonDataDescriptor object at 0x...>
        instance =  None
        owner    =  <class 'descriptorkinds.Model'>


A non-data descriptor can be shadowed by assigning to an instance:

    >>> o.non_data = 7
    >>> o.non_data
    7


Methods are non-data descriptors:

    >>> o.spam  # doctest: +ELLIPSIS
    <bound method Model.spam of <descriptorkinds.Model object at 0x...>>
    >>> Model.spam  # doctest: +ELLIPSIS
    <function Model.spam at 0x...>
    >>> o.spam()  # doctest: +ELLIPSIS
    Model.spam() invoked with arg:
        self     =  <descriptorkinds.Model object at 0x...>
    >>> o.spam = 7
    >>> o.spam
    7


No descriptor type survives being overwritten on the class itself:

    >>> Model.data = 1
    >>> o.data
    1
    >>> Model.data_no_get = 2
    >>> o.data_no_get
    2
    >>> Model.non_data = 3
    >>> o.non_data
    7

"""


class DataDescriptor:
    "a.k.a. overriding or enforced descriptor"

    def __get__(self, instance, owner):
        print('DataDescriptor.__get__() invoked with args:')
        print('    self     = ', self)
        print('    instance = ', instance)
        print('    owner    = ', owner)

    def __set__(self, instance, value):
        print('DataDescriptor.__set__() invoked with args:')
        print('    self     = ', self)
        print('    instance = ', instance)
        print('    value    = ', value)


class DataDescriptorNoGet:

    def __set__(self, instance, value):
        print('DataDescriptorNoGet.__set__() invoked with args:')
        print('    self     = ', self)
        print('    instance = ', instance)
        print('    value    = ', value)


class NonDataDescriptor:
    "a.k.a. non-overriding or shadowable descriptor"

    def __get__(self, instance, owner):
        print('NonDataDescriptor.__get__() invoked with args:')
        print('    self     = ', self)
        print('    instance = ', instance)
        print('    owner    = ', owner)


class Model:
    data = DataDescriptor()
    data_no_get = DataDescriptorNoGet()
    non_data = NonDataDescriptor()

    def spam(self):
        print('Model.spam() invoked with arg:')
        print('    self     = ', self)
