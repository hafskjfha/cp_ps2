import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    for i in range(1,n+1):
        print("sorting",i)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()