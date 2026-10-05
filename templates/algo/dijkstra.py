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

def get_path(s,t,prev):
    path=[]
    cur=t
    while cur!=-1:
        path.append(cur)
        if cur==s:
            break
        cur=prev[cur]
    
    if path[-1]!=s:
        return []

    path.reverse()
    return path