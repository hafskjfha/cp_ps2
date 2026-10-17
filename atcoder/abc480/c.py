import sys
input=sys.stdin.readline

ceil = lambda a, b: (a + b - 1) // b

def solve():
    n,k,t=map(int,input().split())
    a=sorted(map(int,input().split()))
    last=0
    ans=0
    for x in a:
        if x>t:break
        if last<x:
            ans+=ceil(x-last,k)
        last=x+k
        #print(last)
        if last>=t:
            last=t
            break
        
    print(ans+ceil(t-last,k))

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()