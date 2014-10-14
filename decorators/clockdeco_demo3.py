import functools
from clockdeco import clock


@functools.lru_cache()
@clock
def factorial(n):
    return 1 if n < 2 else n*factorial(n-1)


@functools.lru_cache()
@clock
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)


print(factorial(6))
print(fibonacci(6))
