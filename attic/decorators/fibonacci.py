
# source: http://oeis.org/A000045
fibo_seq = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610,
            987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025,
            121393, 196418, 317811, 514229, 832040, 1346269, 2178309,
            3524578, 5702887, 9227465, 14930352, 24157817, 39088169]

from functools import lru_cache

def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)

@lru_cache()
def fibonacci2(n):
    if n < 2:
        return n
    return fibonacci2(n-2) + fibonacci2(n-1)

def memoize(func):
    '''simplest memoizing decorator'''
    cache = {}
    def memoized(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return memoized

def test():
    for i, expected in enumerate(fibo_seq[:31]):
        print(i, expected)
        assert fibonacci(i) == expected

def chronograph():
    global fibonacci
    from time import time
    t0 = time()
    n = 32
    res = fibonacci(n)
    #res = [fibonacci(n) for n in range(30)]
    t1 = time()
    print(n, res, format(t1-t0, '0.6f'))

    t0 = time()
    res = fibonacci2(n)
    #res = [fibonacci2(n) for n in range(30)]
    t1 = time()
    print(n, res, format(t1-t0, '0.6f'))

    t0 = time()
    fibonacci = memoize(fibonacci)
    res = fibonacci(n)
    #res = [fibonacci2(n) for n in range(30)]
    t1 = time()
    print(n, res, format(t1-t0, '0.6f'))

if __name__=='__main__':
    #test()
    chronograph()
