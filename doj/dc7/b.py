import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    a=[*map(int,input().split())]
    print(sum((sorted(a))[1:]))

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()