import doctest
import importlib
import glob


TARGET_GLOB = 'sentence*.py'
TEST_FILE = 'sentence.rst'
TEST_MSG = '{0:16} {1.attempted:2} tests, {1.failed:2} failed - {2}'


def main(argv):
    verbose = '-v' in argv
    for module_file_name in sorted(glob.glob(TARGET_GLOB)):
        module_name = module_file_name.replace('.py', '')
        module = importlib.import_module(module_name)
        try:
            cls = getattr(module, 'Sentence')
        except AttributeError:
            continue
        test(cls, verbose)


def test(cls, verbose=False):

    res = doctest.testfile(
            TEST_FILE,
            globs={'Sentence': cls},
            verbose=verbose,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)
    tag = 'FAIL' if res.failed else 'OK'
    print(TEST_MSG.format(cls.__module__, res, tag))


if __name__ == '__main__':
    import sys
    main(sys.argv)
