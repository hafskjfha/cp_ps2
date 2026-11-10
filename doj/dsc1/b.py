import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    print(*sorted(map(int,input().split())))

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()