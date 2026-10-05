from math import *

def sieve(n):
    is_prime = bytearray(b'\x01') * (n + 1)
    if n >= 0: is_prime[0] = 0
    if n >= 1: is_prime[1] = 0
    for p in range(2, isqrt(n) + 1):
        if is_prime[p]:
            start = p * p
            is_prime[start:n+1:p] = b'\x00' * (((n-start)//p)+1)
    return is_prime