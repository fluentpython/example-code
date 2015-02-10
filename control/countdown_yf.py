from time import sleep

def countdown(n):
    while n:
        print('\tn ->', n)
        yield n
        n -= 1
        sleep(1)

def foo():
    for i in range(6, 3, -1):
        yield i
    yield from countdown(3)

#for j in foo():
#    print('j ->', j)


def squares(n):
    yield from [i for i in range(n)]
    yield from [i*i for i in range(n)]

def squares_stupid(n):
    for i in range(n):
        yield i

    for i in range(n):
        yield i*i

#for s in squares(10):
#    print(s)


def tokenize():
    while True:
        source = input('> ')
        try:
            obj = eval(source)
        except BaseException:
            print('*crash*')
            return
        try:
            it = iter(obj)
        except TypeError:
            yield obj
            return
        else:
            yield from it

#g = tokenize()

#for res in g:
#    print(res)


from concurrent.futures import Future

def f():
    f = future()

def foo(fut):
    print(fut, fut.result())
f = Future()
f.add_done_callback(foo)
f.set_result(42)




