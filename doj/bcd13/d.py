import sys
from collections import deque

input=sys.stdin.readline

def solve():
    n=int(input())
    gr=[[]for _ in range(n+1)]
    pa=[*map(int,input().split())]
    inno=[0]*(n+1)
    #print(gr)
    for i,p in enumerate(pa,2):
        #print(i,p)
        gr[i].append(p)
        inno[p]+=1
        #gr[i].append(p)
    b=[0]+[*map(int,input().split())]
    
    q=deque([i for i in range(1,n+1)if inno[i]==0])
    ans=0
    
    while q:
        u=q.popleft()
        
        for v in gr[u]:
            inno[v]-=1
            if inno[v]==0:
                q.append(v)
            
            if b[u]>=1 and b[v]>=1:
                ans+=1
                b[u]-=1
                b[v]-=1
    
    print(ans)

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()