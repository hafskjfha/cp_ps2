import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    print(n//2*(n//2+n%2))

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()