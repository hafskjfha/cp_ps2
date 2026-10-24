import sys
input=sys.stdin.readline

def solve():
    s=sum(map(int,input().split()))
    print(len(str(s)))

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()