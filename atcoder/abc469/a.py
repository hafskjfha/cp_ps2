import sys
input=sys.stdin.readline

def solve():
    n,k=map(int,input().split())
    print(n-k+1)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()