import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    arr=[*map(int,input().split())]
    if 9 not in arr:
        print(-1)
    else:
        print(min(arr))

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()