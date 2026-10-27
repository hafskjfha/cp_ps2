def euler_tour(adj, root=1):
    n = len(adj)
    tin = [0] * n
    tout = [0] * n
    euler = [0] * n
    timer = 0

    stack = [(root, 0, False)]

    while stack:
        v, parent, exit = stack.pop()

        if exit:
            tout[v] = timer
            continue

        timer += 1
        tin[v] = timer
        euler[timer] = v

        stack.append((v, parent, True))

        for nxt in reversed(adj[v]):
            if nxt != parent:
                stack.append((nxt, v, False))

    return tin, tout, euler