N=200000
MOD=1000000007

fact=[1]*(N+1)
invFact=[1]*(N+1)
for i in range(2,N+1):fact[i]=(fact[i-1]*i)%MOD
invFact[N]=pow(fact[N],MOD-2,MOD)
for i in range(N-1,-1,-1):invFact[i]=(invFact[i+1]*(i+1))%MOD
def comb(n,r):return 0 if n<r or r<0 else fact[n]*invFact[n-r]*invFact[r]%MOD
def perm(n,r):return 0 if n<r or r<0 else fact[n]*invFact[n-r]%MOD