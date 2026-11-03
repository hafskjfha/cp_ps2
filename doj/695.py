import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    a=[*map(int,input().split())]
    x=0
    ans=0
    pfixsum=[0]
    for x in a:pfixsum.append(pfixsum[-1]+x)
    
    for i in range(1,n+1):
        k=pfixsum[n]-pfixsum[i-1]
        if k>=0:
            ans+=i*k
        else:
            ans+=-i*k
    print(ans)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()