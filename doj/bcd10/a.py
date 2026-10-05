import sys
input=sys.stdin.readline

def solve():
    brix=float(input())
    print(f"{86/brix:.1f}")

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()