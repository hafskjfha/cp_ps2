import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    arr=[*map(int,input().split())]
    if len(set(arr))==1:
        print(-1)
    else:
        print(*sorted(arr,reverse=True))

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()