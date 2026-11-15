import sys
input=sys.stdin.readline

def solve():
    a,b=map(int,input().split())
    print((30-a)*(30-b))

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()