import sys
input=sys.stdin.readline

def solve():
    a,b,c=map(int,input().split())
    print(max(abs(a-b),abs(a+c-b)))

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()