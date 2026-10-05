import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    a=[*map(int,input().split())]
    
    x,y=-1,-1
    for i in range(n):
        if a[i]==0:
            x=i
            break

    for i in range(n-1,-1,-1):
        if a[i]==0:
            y=i
            break
    
    if x==y:
        return print(-1)
    print((x!=0)+(y!=n-1))

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()