import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    s=input().strip().split('S')
    print(len(max(s,key=len)))

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()