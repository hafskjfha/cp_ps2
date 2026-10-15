import sys
from collections import deque

input=sys.stdin.readline

def solve():
    n,k=map(int,input().split())
    a=[*map(int,input().split())]
    psum=[0]*(n+1)
    count=[0]*k
    for i in range(n):
        psum[i+1]=psum[i]+a[i]
    
    ans=0
    q=deque([0])
    #print(psum)
    for i in range(1,n+1):
        if len(q)==k+1:
            count[q.popleft()]+=1
        ans+=count[psum[i]%k]
        q.append(psum[i]%k)
        #print(psum[i],ans)
    print(ans)
    #print("=====")

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()