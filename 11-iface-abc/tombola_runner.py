# BEGIN TOMBOLA_RUNNER
import doctest

from tombola import Tombola

# modules to test
import bingo, lotto, tombolist, drum  # <1>

TEST_FILE = 'tombola_tests.rst'
TEST_MSG = '{0:16} {1.attempted:2} tests, {1.failed:2} failed - {2}'


def main(argv):
    verbose = '-v' in argv
    real_subclasses = Tombola.__subclasses__()  # <2>
    virtual_subclasses = list(Tombola._abc_registry)  # <3>

    for cls in real_subclasses + virtual_subclasses:  # <4>
        test(cls, verbose)


def test(cls, verbose=False):

    res = doctest.testfile(
            TEST_FILE,
            globs={'ConcreteTombola': cls},  # <5>
            verbose=verbose,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)
    tag = 'FAIL' if res.failed else 'OK'
    print(TEST_MSG.format(cls.__name__, res, tag))  # <6>


if __name__ == '__main__':
    import sys
    main(sys.argv)
# END TOMBOLA_RUNNER
