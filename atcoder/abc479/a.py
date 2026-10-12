import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    a=[*map(int,input().split())]
    print(sum(a[::2]))

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()