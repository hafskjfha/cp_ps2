import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    a=[*map(int,input().split())]
    b=[*map(int,input().split())]
    m=max(a)
    INF=float('inf')
    pm=[0]
    for x in b:
        pm.append(max(pm[-1],x))
    ans=0
    for x in a:
        ans+=pm[x]
    #print(pm)
    print(ans)

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()