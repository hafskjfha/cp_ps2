import sys
input=sys.stdin.readline

def solve():
    a,b,c,d=map(int,input().split())
    n=a+b+c+d
    MOD=998244353
    
    fac = [1] * (n+1)
    inv_fac = [1] * (n+1)
    for i in range(2,n+1):
        fac[i] = (fac[i-1]*i)%MOD
        
    inv_fac[n]=pow(fac[n],MOD-2,MOD)
    
    for i in range(n,0,-1):
        inv_fac[i-1]=(inv_fac[i]*i)%MOD
    
    ans=0
    for i in range(c+1):
        ans = (ans + ((fac[a+i+b])*(inv_fac[b]*inv_fac[a+i]) * ((fac[c-i+d-1])*(inv_fac[c-i]*inv_fac[d-1])))) % MOD
    
    print(ans)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()