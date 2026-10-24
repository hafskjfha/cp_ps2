import sys
input=sys.stdin.readline

from heapq import heappop,heappush

def dijkstra(s,adj,n):
    INF=float('inf')
    dist=[INF]*n
    prev=[-1]*n
    dist[s]=0
    pq=[(0,s)]
    
    while pq:
        d,u=heappop(pq)
        if d!=dist[u]:
            continue
        for v,w in adj[u]:
            nd=d+w
            if nd<dist[v]:
                dist[v]=nd
                prev[v]=u
                heappush(pq,(nd,v))
    
    return dist,prev

def solve():
    n,m,s,t=map(int,input().split())
    temp=[[]for _ in range(n+1)]
    for _ in range(m):
        u,v=map(int,input().split())
        temp[u].append(v)
    gr=[[]for _ in range(n+1)]
    for u in range(1,n+1):
        temp[u].sort()
        if not temp[u]:continue
        gr[u].append((temp[u][0],0))
        for i in range(1,len(temp[u])):
            gr[u].append((temp[u][i],1))
    
    #print(gr)
    
    dist,_=dijkstra(s,gr,n+1)
    print(dist[t] if dist[t]!=float('inf')else -1)
    

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()