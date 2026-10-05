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