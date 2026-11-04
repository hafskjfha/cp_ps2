import sys
from collections import deque

input=sys.stdin.readline

def solve():
    v,e,k=map(int,input().split())
    
    gr=[[]for _ in range(v+1)]
    for _ in range(e):
        a,b,c=map(int,input().split())
        gr[a].append((b,c))
        gr[b].append((a,c))
    INF=float('inf')
    ans=INF
    for i in range(1,k+1):
        vi=[INF]*(v+1)
        dq=deque([1])
        vi[1]=0
        while dq:
            a=dq.popleft()
            
            for da,c in gr[a]:
                if c==i:
                    if vi[a]<vi[da]:
                        vi[da]=vi[a]
                        dq.appendleft(da)
                else:
                    if vi[a]+1<vi[da]:
                        vi[da]=vi[a]+1
                        dq.append(da)
        ans=min(ans,vi[v])
    print(ans)
    

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()