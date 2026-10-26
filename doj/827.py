import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    s=sum(map(int,input().split()))
    print(*((s,0) if n%2 else (0,s)))

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()