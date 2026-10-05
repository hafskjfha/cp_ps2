import sys
from collections import deque
input=sys.stdin.readline

def tarjan_scc(n, graph):
    order = [-1] * n
    low = [0] * n
    on_stack = [False] * n

    scc_stack = []
    sccs = []

    timer = 0

    for start in range(n):
        if order[start] != -1:
            continue

        dfs_stack = [(start, 0)]

        order[start] = low[start] = timer
        timer += 1
        scc_stack.append(start)
        on_stack[start] = True

        while dfs_stack:
            u, i = dfs_stack[-1]

            if i < len(graph[u]):
                v = graph[u][i]

                dfs_stack[-1] = (u, i + 1)

                if order[v] == -1:
                    order[v] = low[v] = timer
                    timer += 1

                    scc_stack.append(v)
                    on_stack[v] = True
                    dfs_stack.append((v, 0))

                elif on_stack[v]:
                    low[u] = min(low[u], order[v])

            else:
                dfs_stack.pop()

                if dfs_stack:
                    parent, _ = dfs_stack[-1]
                    low[parent] = min(low[parent], low[u])

                if low[u] == order[u]:
                    component = []

                    while True:
                        v = scc_stack.pop()
                        on_stack[v] = False
                        component.append(v)

                        if v == u:
                            break

                    sccs.append(component)

    return sccs

def check(scc,gr2,node_scc):
    
    for u in scc:
        for v,t in gr2[u]:
            if node_scc[u]==node_scc[v] and t==1:
                return False
    
    return True

def solve():
    n,m=map(int,input().split())
    gr1=[[]for _ in range(n+1)]
    gr2=[[]for _ in range(n+1)]
    for _ in range(m):
        t,u,v=map(int,input().split())
        if t==1 and u==v:
            print("No")
            return
        gr1[u].append(v)
        gr2[u].append((v,t))
    
    sccs=tarjan_scc(n+1,gr1)
    node_scc=[None]*(n+1)
    
    for scc in sccs:
        for i in range(len(scc)):
            node=scc[i]
            node_scc[node]=scc[0]
        if not check(scc,gr2,node_scc):
            return print("No")
        
    
    dag=[[]for _ in range(n+1)]
    for u in range(1,n+1):
        for v,t in gr2[u]:
            if node_scc[u]!=node_scc[v]:
                dag[node_scc[u]].append((node_scc[v],t))
                
    indgree=[0]*(n+1)
    for u in range(1,n+1):
        for v,t in dag[u]:
            indgree[v]+=1
    
    res=[1]*(n+1)
    q=deque([i for i in range(1,n+1) if indgree[i]==0])
    
    while q:
        u=q.popleft()
        
        for v,t in dag[u]:
            indgree[v]-=1
            res[v]=max(res[v],res[u]+t)
            if indgree[v]==0:
                q.append(v)
    
    print("Yes")
    print(*[res[node_scc[i]] for i in range(1,n+1)])
    

def main():
    t=1#int(input())
    for _ in range(t):
        solve()
main()