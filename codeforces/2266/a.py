import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    a=[*map(int,input().split())]
    k=min(a)
    print(n-k)

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()