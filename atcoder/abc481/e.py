import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    codi=[tuple(map(int,input().split()))for _ in range(n)]
    

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()