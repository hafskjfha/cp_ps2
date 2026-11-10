import sys
input=sys.stdin.readline

def solve():
    a=int(input())
    b=int(input())
    print(a-b)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()