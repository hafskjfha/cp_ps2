import sys
input=sys.stdin.readline

ans=0

def dfs(n,w,arr,i,nw,nv):
    global ans
    ans=max(ans,nv)
    
    for j in range(i+1,n):
        a,b=arr[j]
        if nw+b<=w:
            dfs(n,w,arr,j,nw+b,nv+a)

def solve():
    n,w=map(int,input().split())
    arr=[tuple(map(int,input().split()))for _ in range(n)]
    
    dfs(n,w,arr,-1,0,0)
    global ans
    print(ans)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()