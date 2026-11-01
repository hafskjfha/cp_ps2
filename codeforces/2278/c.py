import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    a=[*map(int,input().split())]
    if a[1:n-1].count(1)==n-2:
        if a[0]==a[n-1]==1:
            print(-1)
        else:
            print(max(a[0],a[n-1])+min(a[0],a[n-1])-1)
    else:
        print(sum(a)-1)

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()