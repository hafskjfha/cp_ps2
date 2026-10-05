def sieve_of_eratosthenes(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * 2, n + 1, i):
                is_prime[j] = False

    return is_prime

n,m=map(int,open(0))
isp=sieve_of_eratosthenes(m)
primes=[i for i in range(n,m+1)if isp[i]]
if primes:
    print(sum(primes))
    print(primes[0])
else:
    print(-1)
