import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    if n<=3:print(-1)
    else:
        print(*range(1,n+1))

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()