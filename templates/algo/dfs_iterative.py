def dfs(s,adj,n):
    vi=[False]*n
    st=[s]
    vi[s]=True
    while st:
        u=st.pop()
        for v in adj[u]:
            if not vi[v]:
                vi[v]=True
                st.append(v)
                
    return vi