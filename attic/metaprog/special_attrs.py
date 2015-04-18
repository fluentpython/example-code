
'''
4.13. Special Attributes

The implementation adds a few special read-only attributes to
several object types, where they are relevant.

Some of these are not reported by the dir() built-in function.

https://docs.python.org/3/library/stdtypes.html#special-attributes
'''


obj_attrs = {'__dict__', '__class__'}

cls_data_attrs = {'__slots__', '__bases__', '__name__', '__qualname__', '__mro__'}

cls_methods = {'mro', '__subclasses__'}

cls_attrs = cls_data_attrs | cls_methods


an_object = object()

class EmptyClass():
    pass

an_instance = EmptyClass()

class EmptySlots():
    __slots__ = ()

a_slots_instance = EmptySlots()


objs = EmptyClass, EmptySlots, an_object, an_instance, a_slots_instance

for obj in objs:
    print('-' * 60)
    print(repr(obj), ':', type(obj))
    dir_obj = set(dir(obj))
    print('obj_attrs not listed:', sorted(obj_attrs - dir_obj))
    print('all cls_attrs       :', sorted(cls_attrs))
    print('cls_attrs not listed:', sorted(cls_attrs - dir_obj))
