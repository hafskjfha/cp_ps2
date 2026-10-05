import functools

@functools.cache
def factorial(n):
    return n * factorial(n-1) if n else 1

import time

a=time.perf_counter()
factorial(10)
print(time.perf_counter()-a)

a=time.perf_counter()
factorial(9)
print(time.perf_counter()-a)

a=time.perf_counter()
factorial(12)
print(time.perf_counter()-a)