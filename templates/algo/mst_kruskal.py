def kruskal(n, edges):
    # edges: (w, u, v)
    edges.sort()
    dsu = DSU(n)
    cost = 0
    used = 0
    for w, u, v in edges:
        if dsu.union(u, v):
            cost += w
            used += 1
            if used == n - 1:
                break
    return cost if used == n - 1 else None