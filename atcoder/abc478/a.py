import sys
input=sys.stdin.readline

def solve():
    n,m=map(int,input().split())
    
    for i in range(n):
        if i<   m%n:
            print(m//n+1)
        else:
            print(m//n)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()