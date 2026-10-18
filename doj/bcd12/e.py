import sys
input=sys.stdin.readline

def solve():
    n,k,e=map(int,input().split())
    a=[*map(int,input().split())]
    print(1 if sum(a)<=e else 0)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()