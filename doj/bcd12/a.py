import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    print("YES"if 0<=n<=2200 else "NO")

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()