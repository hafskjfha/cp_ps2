import sys
sys.set_int_max_str_digits(300000) 
input=sys.stdin.readline

def solve():
    MOD=998244353
    n=int(input())
    if 1<=n<=9:
        print(n)
        return
    n-=10
    a,b=divmod(n,8)
    #print(a,b)
    ans=pow(10,a+1,MOD)
    print((ans*(b+1))%MOD)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()