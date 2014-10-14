import sys
import importlib
import doctest

from tombola import Tombola

TESTS = 'tombola_tests.rst'

MODULES = 'bingo lotto tombolist drum'.split()


def test_module(module_name, verbose=False):

    module = importlib.import_module(module_name)

    tombola_class = None
    for name in dir(module):
        obj = getattr(module, name)
        if (isinstance(obj, type) and
                issubclass(obj, Tombola) and
                obj.__module__ == module_name):
            tombola_class = obj
            break  # stop at first matching class

    if tombola_class is None:
        print('ERROR: no Tombola subclass found in', module_name)
        sys.exit(1)

    res = doctest.testfile(TESTS,
                           globs={'TombolaUnderTest': tombola_class},
                           verbose=verbose,
                           optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)
    print('{:10} {}'.format(module_name, res))


if __name__ == '__main__':

    args = sys.argv[:]
    if '-v' in args:
        args.remove('-v')
        verbose = True
    else:
        verbose = False

    if len(args) == 2:
        module_names = [args[1]]
    else:
        module_names = MODULES

    for name in module_names:
        print('*' * 60, name)
        test_module(name, verbose)
