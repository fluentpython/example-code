import atexit

from evaldecos import deco_alpha
from evaldecos import deco_beta


print('<<1>> start')


func_A = lambda: print('<<2>> func_A')


def func_B():
    print('<<3>> func_B')

    def func_C():
        print('<<4>> func_C')

    return func_C


@deco_alpha
def func_D():
    print('<<6>> func_D')


def func_E():
    print('<<7>> func_E')


class ClassOne(object):
    print('<<7>> ClassOne body')

    def __init__(self):
        print('<<8>> ClassOne.__init__')

    def __del__(self):
        print('<<9>> ClassOne.__del__')

    def method1(self):
        print('<<10>> ClassOne.method')
        return "result from 'ClassOne.method1'"

    class ClassTwo(object):
        print('<<11>> ClassTwo body')


@deco_beta
class ClassThree(ClassOne):
    print('<<12>> ClassThree body')

    def method3(self):
        print('<<13>> ClassOne.method')
        return "result from 'ClassThree.method3'"


if True:
    print("<<14>> 'if True'")


if False:
    print("<<15>> 'if False'")


atexit.register(func_E)

print("<<16>> right before 'if ... __main__'")


if __name__ == '__main__':
    print('<<17>> start __main__ block')
    print(func_A)
    print(func_A())
    print('<<18>> continue __main__ block')
    print(func_B)
    b_result = func_B()
    print(b_result)
    one = ClassOne()
    one.method1()
    b_result()
    print(func_D)
    func_D()
    three = ClassThree()
    three.method3()

    class ClassFour(object):
        print('<<19>> ClasFour body')

    print('<<20>> end __main__ block')


print('<<21>> The End')
