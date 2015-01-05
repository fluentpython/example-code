
"""

>>> f = Foo()
>>> f.bar = 77
>>> f.bar
77
>>> Foo.bar.__doc__
'The "bar" attribute'
>>> import pydoc
>>> pydoc.getdoc(Foo.bazz)
'The "bazz" attribute'

"""


def doc_descriptor_wrapper_factory(descriptor):
    wrapper_cls_name = 'DocDescriptorWrapper'
    wrapper_cls_attrs = descriptor.__dict__.copy()
    wrapper_cls_attrs['__slots__'] = ['_wrapped']

    def wrapped_getter(self):
        "the wrapped descriptor instance"
        return self._wrapped

    def wrapper_repr(self):
        return '<{} {!r}>'.format(wrapper_cls_name, self.__doc__)

    wrapper_cls_attrs['wrapped'] = property(wrapped_getter)
    wrapper_cls_attrs['__repr__'] = wrapper_repr
    wrapper_cls = type(wrapper_cls_name, (), wrapper_cls_attrs)
    wrapper = wrapper_cls()
    wrapper._wrapped = descriptor
    return wrapper


class DocDescriptor:
    """A documented descriptor"""

    def __init__(self, documentation):
        self.__doc__ = documentation
        cls_name = self.__class__.__name__
        self.storage_name = '_{}_{:x}'.format(cls_name, id(self))

    def __get__(self, instance, owner):
        """The __get__ method"""
        if instance is None:
            return doc_descriptor_wrapper_factory(self)
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)


class Foo:
    """The "Foo" class"""

    bar = DocDescriptor('The "bar" attribute')
    bazz = DocDescriptor('The "bazz" attribute')
