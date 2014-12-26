import timeit

test_hasattr = """
if hasattr(gizmo, 'gadget'):
    feature = gizmo.gadget
else:
    feature = None
"""

test_getattr = """
feature = getattr(gizmo, 'gadget', None)
"""

test_tryget = """
try:
    feature = getattr(gizmo, 'gadget')
except AttributeError:
    feature = None
"""


class Gizmo:
    def __init__(self):
        self.gadget = True

gizmo = Gizmo()

test_keys = 'hasattr', 'getattr', 'tryget'

def test():
    for test_key in test_keys:
        test_name = 'test_' + test_key
        test = globals()[test_name]
        setup = 'from __main__ import gizmo'
        t_yes = min(timeit.repeat(test, repeat=5, setup=setup))
        del gizmo.gadget
        t_not = min(timeit.repeat(test, repeat=5, setup=setup))
        gizmo.gadget = True
        print('|{:7} | {:.3} | {:.3}'.format(test_key, t_yes, t_not))

if __name__ == '__main__':
    test()

