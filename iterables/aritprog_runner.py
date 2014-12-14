import doctest
import importlib
import glob


TARGET_GLOB = 'aritprog*.py'
TEST_FILE = 'aritprog.rst'
TEST_MSG = '{0:16} {1.attempted:2} tests, {1.failed:2} failed - {2}'


def main(argv):
    verbose = '-v' in argv
    for module_file_name in sorted(glob.glob(TARGET_GLOB)):
        module_name = module_file_name.replace('.py', '')
        module = importlib.import_module(module_name)
        gen_factory = getattr(module, 'ArithmeticProgression', None)
        if gen_factory is None:
            gen_factory = getattr(module, 'aritprog_gen', None)
        if gen_factory is None:
            continue

        test(gen_factory, verbose)


def test(gen_factory, verbose=False):
    res = doctest.testfile(
            TEST_FILE,
            globs={'aritprog_gen': gen_factory},
            verbose=verbose,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)
    tag = 'FAIL' if res.failed else 'OK'
    print(TEST_MSG.format(gen_factory.__module__, res, tag))


if __name__ == '__main__':
    import sys
    main(sys.argv)
