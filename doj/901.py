import sys
from fractions import Fraction
input=sys.stdin.readline

def solve():
    n,q=map(int,input().split())
    p=list(map(Fraction,input().split()))

    zero=Fraction("0")
    one=Fraction("1")
    k=Fraction("0.05")
    
    dp=[zero]*21
    dp[0]=one
    prefix=[zero]*(n+1)

    for i in range(n):
        ndp=[zero]*21
        e=zero

        for s in range(21):
            prob=max(zero,p[i]-k*s)
            eat=dp[s]*prob
            skip=dp[s]*(one-prob)

            e+=eat
            ndp[min(20,s+1)]+=eat
            ndp[max(0,s-1)]+=skip

        dp=ndp
        prefix[i+1]=prefix[i]+e

    for _ in range(q):
        l,r=map(int,input().split())
        print(f"{float(prefix[r]-prefix[l-1]):.10f}")

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()