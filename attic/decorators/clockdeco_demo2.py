from clockdeco import clock

import time

@clock
def snooze(milis):
    time.sleep(milis/1000)

@clock
def factorial(n):
    return 1 if n < 2 else n*factorial(n-1)


@clock
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)

snooze(123)
print(factorial(6))
print(fibonacci(4))
