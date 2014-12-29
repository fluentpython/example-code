import timeit

def exists_and_truthy_hasattr(obj, attr_name):
    if hasattr(obj, attr_name):
        return bool(getattr(obj, attr_name))
    else:
        return False

def exists_and_truthy_getattr(obj, attr_name):
    return bool(getattr(obj, attr_name, False))

def exists_and_truthy_tryget(obj, attr_name):
    try:
        return bool(getattr(obj, attr_name))
    except AttributeError:
        return False


class Gizmo:
    def __init__(self):
        self.gadget = True

gizmo = Gizmo()

test_keys = 'hasattr', 'getattr', 'tryget'

def average(timings):
    sample = timings[1:-1]
    return sum(sample) / len(sample)

def do_tests():
    for test_key in test_keys:
        func_name = 'exists_and_truthy_' + test_key
        test = func_name + '(gizmo, "gadget")'
        setup = 'from __main__ import gizmo, ' + func_name
        elapsed = average(timeit.repeat(test, repeat=5, setup=setup))
        print(test_key.rjust(7), format(elapsed, '0.5f'))

if __name__ == '__main__':
    do_tests()
    del gizmo.gadget
    do_tests()

