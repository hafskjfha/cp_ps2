#from itertools import permutations
import sys
input=sys.stdin.readline
N=200000
MOD=1000000007

fact=[1]*(N+1)
invFact=[1]*(N+1)
for i in range(2,N+1):fact[i]=(fact[i-1]*i)%MOD
invFact[N]=pow(fact[N],MOD-2,MOD)
for i in range(N-1,-1,-1):invFact[i]=(invFact[i+1]*(i+1))%MOD
def comb(n,r):return fact[n]*invFact[n-r]*invFact[r]%MOD if n>=r or r<0 else 0

def solve():
    n,l,r,k=map(int,input().split())
    # count=0
    # for arr in permutations(range(1,n+1),n):
    #     if max(arr[l-1:r])==k:
    #         #print(arr)
    #         count+=1
    # import math
    # print((math.comb(k-1,r-l)*math.factorial(r-l+1)) * math.factorial(n-(r-l+1)))
    print((fact[n-(r-l+1)]*(fact[r-l+1]*comb(k-1,r-l)))%MOD)
    #print(count)
    #print("=====")

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()