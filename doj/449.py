import sys
input=sys.stdin.readline

def solve():
    x1,y1=map(int,input().split())
    for _ in range(int(input())):
        x,y=map(int,input().split())
        print(0 if x==x1 or y==y1 else 1)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()