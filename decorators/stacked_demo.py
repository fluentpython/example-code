def d1(f):
    def wrapped():
        print('d1/wrapped')
        return f()
    return wrapped


def d2(f):
    def wrapped():
        print('d2/wrapped')
        return f()
    return wrapped


@d1
@d2
def f():
    print('f')

f()

def g():
    print('g')

g = d1(d2(g))

g()
