import sys
import importlib
import doctest

from tombola import Tombola

TEST_FILE = 'tombola_tests.rst'
MODULE_NAMES = 'bingo lotto tombolist drum'.split()
TEST_MSG = '{0:16} {1.attempted:2} tests, {1.failed:2} failed - {2}'


def test(cls, verbose=False):

    res = doctest.testfile(TEST_FILE,
                           globs={'TombolaUnderTest': cls},
                           verbose=verbose,
                           optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)
    tag = 'FAIL' if res.failed else 'OK'
    print(TEST_MSG.format(cls.__name__, res, tag))


if __name__ == '__main__':

    for name in MODULE_NAMES:  # import modules to test, by name
        importlib.import_module(name)

    verbose = '-v' in sys.argv

    real_subclasses = Tombola.__subclasses__()
    virtual_subclasses = list(Tombola._abc_registry)

    for cls in real_subclasses + virtual_subclasses:
        test(cls, verbose)
