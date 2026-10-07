import sys
input=sys.stdin.readline

def solve():
    x,y,r=map(int,input().split())
    print(x+r,y)

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()