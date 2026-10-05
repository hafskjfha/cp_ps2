def packed_exact_four(grid,target,stamp,k):
    expand=packed_transitions()
    initial=sum(v<<(3*i) for i,v in enumerate(grid+stamp))
    wanted=sum(v<<(3*i) for i,v in enumerate(target))
    comparison_mask=sum(1<<(3*i) for i in range(16))
    def matches(state):
        diff=state^wanted
        return 16-((diff|(diff>>1)|(diff>>2))&comparison_mask).bit_count()
    best_score,best=matches(initial),b''
    upper=color_bound(grid+stamp,target)
    if best_score==upper:
        return []
    visited={initial}
    frontier=[(initial,b'')]
    for _ in range(min(k,4)):
        next_layer=[]
        for state,path in frontier:
            for aid,child in expand(state):
                if child in visited:
                    continue
                visited.add(child)
                new_path=path+bytes((aid,))
                score=matches(child)
                if score>best_score:
                    best_score,best=score,new_path
                    if score==upper:
                        return list(best)
                next_layer.append((child,new_path))
        frontier=next_layer
    return list(best)


def solve(n,d,c,k,grid,target,stamp):
    if n==4 and d==3 and k<=4:
        path=packed_exact_four(grid,target,stamp,k)
        return [(aid//8,(aid//4)%2,aid%4) for aid in path]
    return solve_without_exact_four(n,d,c,k,grid,target,stamp)
