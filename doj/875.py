import sys
input=sys.stdin.readline

def solve():
    n,p=map(int,input().split())
    print("P is NP!"if p==n*p else "P is not NP!")

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()