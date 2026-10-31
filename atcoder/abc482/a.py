import sys
input=sys.stdin.readline

def solve():
    print("odd" if input().strip().count('o')%2 else "even")

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()