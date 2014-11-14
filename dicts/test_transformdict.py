"""Unit tests for transformdict.py."""

import unittest
from test import support
from test import mapping_tests
import pickle
import copy
from functools import partial

from transformdict import TransformDict


def str_lower(s):
    return s.lower()


class TransformDictTestBase(unittest.TestCase):

    def check_underlying_dict(self, d, expected):
        """
        Check for implementation details.
        """
        self.assertEqual(d._data, expected)
        self.assertEqual(set(d._original), set(expected))
        self.assertEqual([d._transform(v) for v in d._original.values()],
                         list(d._original.keys()))


class TestTransformDict(TransformDictTestBase):

    def test_init(self):
        with self.assertRaises(TypeError):
            TransformDict()
        with self.assertRaises(TypeError):
            # Too many positional args
            TransformDict(str.lower, {}, {})
        with self.assertRaises(TypeError):
            # Not a callable
            TransformDict(object())
        d = TransformDict(str.lower)
        self.check_underlying_dict(d, {})
        pairs = [('Bar', 1), ('Foo', 2)]
        d = TransformDict(str.lower, pairs)
        self.assertEqual(sorted(d.items()), pairs)
        self.check_underlying_dict(d, {'bar': 1, 'foo': 2})
        d = TransformDict(str.lower, dict(pairs))
        self.assertEqual(sorted(d.items()), pairs)
        self.check_underlying_dict(d, {'bar': 1, 'foo': 2})
        d = TransformDict(str.lower, **dict(pairs))
        self.assertEqual(sorted(d.items()), pairs)
        self.check_underlying_dict(d, {'bar': 1, 'foo': 2})
        d = TransformDict(str.lower, {'Bar': 1}, Foo=2)
        self.assertEqual(sorted(d.items()), pairs)
        self.check_underlying_dict(d, {'bar': 1, 'foo': 2})

    def test_transform_func(self):
        # Test the `transform_func` attribute
        d = TransformDict(str.lower)
        self.assertIs(d.transform_func, str.lower)
        # The attribute is read-only
        with self.assertRaises(AttributeError):
            d.transform_func = str.upper

    def test_various_transforms(self):
        d = TransformDict(lambda s: s.encode('utf-8'))
        d['Foo'] = 5
        self.assertEqual(d['Foo'], 5)
        self.check_underlying_dict(d, {b'Foo': 5})
        with self.assertRaises(AttributeError):
            # 'bytes' object has no attribute 'encode'
            d[b'Foo']
        # Another example
        d = TransformDict(str.swapcase)
        d['Foo'] = 5
        self.assertEqual(d['Foo'], 5)
        self.check_underlying_dict(d, {'fOO': 5})
        with self.assertRaises(KeyError):
            d['fOO']

    # NOTE: we mostly test the operations which are not inherited from
    # MutableMapping.

    def test_setitem_getitem(self):
        d = TransformDict(str.lower)
        with self.assertRaises(KeyError):
            d['foo']
        d['Foo'] = 5
        self.assertEqual(d['foo'], 5)
        self.assertEqual(d['Foo'], 5)
        self.assertEqual(d['FOo'], 5)
        with self.assertRaises(KeyError):
            d['bar']
        self.check_underlying_dict(d, {'foo': 5})
        d['BAR'] = 6
        self.assertEqual(d['Bar'], 6)
        self.check_underlying_dict(d, {'foo': 5, 'bar': 6})
        # Overwriting
        d['foO'] = 7
        self.assertEqual(d['foo'], 7)
        self.assertEqual(d['Foo'], 7)
        self.assertEqual(d['FOo'], 7)
        self.check_underlying_dict(d, {'foo': 7, 'bar': 6})

    def test_delitem(self):
        d = TransformDict(str.lower, Foo=5)
        d['baR'] = 3
        del d['fOO']
        with self.assertRaises(KeyError):
            del d['Foo']
        with self.assertRaises(KeyError):
            del d['foo']
        self.check_underlying_dict(d, {'bar': 3})

    def test_get(self):
        d = TransformDict(str.lower)
        default = object()
        self.assertIs(d.get('foo'), None)
        self.assertIs(d.get('foo', default), default)
        d['Foo'] = 5
        self.assertEqual(d.get('foo'), 5)
        self.assertEqual(d.get('FOO'), 5)
        self.assertIs(d.get('bar'), None)
        self.check_underlying_dict(d, {'foo': 5})

    def test_getitem(self):
        d = TransformDict(str.lower)
        d['Foo'] = 5
        self.assertEqual(d.getitem('foo'), ('Foo', 5))
        self.assertEqual(d.getitem('FOO'), ('Foo', 5))
        with self.assertRaises(KeyError):
            d.getitem('bar')

    def test_pop(self):
        d = TransformDict(str.lower)
        default = object()
        with self.assertRaises(KeyError):
            d.pop('foo')
        self.assertIs(d.pop('foo', default), default)
        d['Foo'] = 5
        self.assertIn('foo', d)
        self.assertEqual(d.pop('foo'), 5)
        self.assertNotIn('foo', d)
        self.check_underlying_dict(d, {})
        d['Foo'] = 5
        self.assertIn('Foo', d)
        self.assertEqual(d.pop('FOO'), 5)
        self.assertNotIn('foo', d)
        self.check_underlying_dict(d, {})
        with self.assertRaises(KeyError):
            d.pop('foo')

    def test_clear(self):
        d = TransformDict(str.lower)
        d.clear()
        self.check_underlying_dict(d, {})
        d['Foo'] = 5
        d['baR'] = 3
        self.check_underlying_dict(d, {'foo': 5, 'bar': 3})
        d.clear()
        self.check_underlying_dict(d, {})

    def test_contains(self):
        d = TransformDict(str.lower)
        self.assertIs(False, 'foo' in d)
        d['Foo'] = 5
        self.assertIs(True, 'Foo' in d)
        self.assertIs(True, 'foo' in d)
        self.assertIs(True, 'FOO' in d)
        self.assertIs(False, 'bar' in d)

    def test_len(self):
        d = TransformDict(str.lower)
        self.assertEqual(len(d), 0)
        d['Foo'] = 5
        self.assertEqual(len(d), 1)
        d['BAR'] = 6
        self.assertEqual(len(d), 2)
        d['foo'] = 7
        self.assertEqual(len(d), 2)
        d['baR'] = 3
        self.assertEqual(len(d), 2)
        del d['Bar']
        self.assertEqual(len(d), 1)

    def test_iter(self):
        d = TransformDict(str.lower)
        it = iter(d)
        with self.assertRaises(StopIteration):
            next(it)
        d['Foo'] = 5
        d['BAR'] = 6
        self.assertEqual(set(x for x in d), {'Foo', 'BAR'})

    def test_first_key_retained(self):
        d = TransformDict(str.lower, {'Foo': 5, 'BAR': 6})
        self.assertEqual(set(d), {'Foo', 'BAR'})
        d['foo'] = 7
        d['baR'] = 8
        d['quux'] = 9
        self.assertEqual(set(d), {'Foo', 'BAR', 'quux'})
        del d['foo']
        d['FOO'] = 9
        del d['bar']
        d.setdefault('Bar', 15)
        d.setdefault('BAR', 15)
        self.assertEqual(set(d), {'FOO', 'Bar', 'quux'})

    def test_repr(self):
        d = TransformDict(str.lower)
        self.assertEqual(repr(d),
            "TransformDict(<method 'lower' of 'str' objects>, {})")
        d['Foo'] = 5
        self.assertEqual(repr(d),
            "TransformDict(<method 'lower' of 'str' objects>, {'Foo': 5})")

    def test_repr_non_hashable_keys(self):
        d = TransformDict(id)
        self.assertEqual(repr(d),
            "TransformDict(<built-in function id>, {})")
        d[[1]] = 2
        self.assertEqual(repr(d),
            "TransformDict(<built-in function id>, [([1], 2)])")


class TransformDictMappingTests(TransformDictTestBase,
                                mapping_tests.BasicTestMappingProtocol):

    TransformDict = TransformDict
    type2test = partial(TransformDict, str.lower)

    def check_shallow_copy(self, copy_func):
        d = self.TransformDict(str_lower, {'Foo': []})
        e = copy_func(d)
        self.assertIs(e.__class__, self.TransformDict)
        self.assertIs(e._transform, str_lower)
        self.check_underlying_dict(e, {'foo': []})
        e['Bar'] = 6
        self.assertEqual(e['bar'], 6)
        with self.assertRaises(KeyError):
            d['bar']
        e['foo'].append(5)
        self.assertEqual(d['foo'], [5])
        self.assertEqual(set(e), {'Foo', 'Bar'})

    def check_deep_copy(self, copy_func):
        d = self.TransformDict(str_lower, {'Foo': []})
        e = copy_func(d)
        self.assertIs(e.__class__, self.TransformDict)
        self.assertIs(e._transform, str_lower)
        self.check_underlying_dict(e, {'foo': []})
        e['Bar'] = 6
        self.assertEqual(e['bar'], 6)
        with self.assertRaises(KeyError):
            d['bar']
        e['foo'].append(5)
        self.assertEqual(d['foo'], [])
        self.check_underlying_dict(e, {'foo': [5], 'bar': 6})
        self.assertEqual(set(e), {'Foo', 'Bar'})

    def test_copy(self):
        self.check_shallow_copy(lambda d: d.copy())

    def test_copy_copy(self):
        self.check_shallow_copy(copy.copy)

    def test_cast_as_dict(self):
        d = self.TransformDict(str.lower, {'Foo': 5})
        e = dict(d)
        self.assertEqual(e, {'Foo': 5})

    def test_copy_deepcopy(self):
        self.check_deep_copy(copy.deepcopy)

    def test_pickling(self):
        def pickle_unpickle(obj, proto):
            data = pickle.dumps(obj, proto)
            return pickle.loads(data)
        for proto in range(0, pickle.HIGHEST_PROTOCOL + 1):
            with self.subTest(pickle_protocol=proto):
                self.check_deep_copy(partial(pickle_unpickle, proto=proto))


class MyTransformDict(TransformDict):
    pass


class TransformDictSubclassMappingTests(TransformDictMappingTests):

    TransformDict = MyTransformDict
    type2test = partial(MyTransformDict, str.lower)


def test_main(verbose=None):
    test_classes = [TestTransformDict, TransformDictMappingTests,
                    TransformDictSubclassMappingTests]
    support.run_unittest(*test_classes)


if __name__ == "__main__":
    test_main(verbose=True)
