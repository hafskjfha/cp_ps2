def miller_rabin(n, a):
    if n % a == 0:
        return n == a

    d = n - 1
    s = 0

    while d % 2 == 0:
        d //= 2
        s += 1

    x = pow(a, d, n)

    if x == 1 or x == n - 1:
        return True

    for _ in range(s - 1):
        x = x * x % n

        if x == n - 1:
            return True

    return False


def is_prime(n):
    if n < 2:
        return False

    bases = [2, 325, 9375, 28178, 450775, 9780504, 1795265022]

    for a in bases:
        if a % n == 0:
            continue

        if not miller_rabin(n, a):
            return False

    return True