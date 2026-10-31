import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    arr=[*map(int,input().split())]
    ans=float('-inf')
    for i in range(n):
        ans=max(ans,arr[i]+n-i-1-i)
    print(ans)

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()