def binary_transitions():
    rotations=[]
    for r in range(4):
        table=[]
        for value in range(512):
            result=0
            for u in range(3):
                for v in range(3):
                    x,y=((u,v),(v,2-u),(2-u,2-v),(2-v,u))[r]
                    result|=((value>>(u*3+v))&1)<<(x*3+y)
            table.append(result)
        rotations.append(table)
    patches=[]
    for x in range(2):
        for y in range(2):
            base=4*x+y
            scatter=[((v&7)<<base)|((v&56)<<(base+1))|((v&448)<<(base+2)) for v in range(512)]
            paint=[[scatter[v] for v in rotations[r]] for r in range(4)]
            patches.append((base,65535^scatter[511],paint))
    def expand(state):
        board,stamp=state&65535,state>>16
        for position,(base,mask,paint) in enumerate(patches):
            patch=((board>>base)&7)|((board>>(base+1))&56)|((board>>(base+2))&448)
            retained=board&mask
            for rotation in range(4):
                child=retained|paint[rotation][stamp]|(rotations[(-rotation)&3][patch]<<16)
                yield position*4+rotation,child
    return expand


def binary_bfs(grid,target,stamp,k):
    initial=sum(v<<i for i,v in enumerate(grid+stamp))
    wanted=sum(v<<i for i,v in enumerate(target))
    if initial&65535==wanted:
        return []
    required=initial.bit_count()-wanted.bit_count()
    if not 0<=required<=9:
        return None
    expand=binary_transitions()
    forward={initial:(None,None)}
    frontier=[initial]
    first_depth=min(3,k)
    def prefix(state):
        path=[]
        while forward[state][0] is not None:
            state,action=forward[state]
            path.append(action)
        return path[::-1]
    for _ in range(first_depth):
        next_layer=[]
        for state in frontier:
            for action,child in expand(state):
                if child in forward:
                    continue
                forward[child]=(state,action)
                if child&65535==wanted:
                    return prefix(child)
                next_layer.append(child)
        frontier=next_layer
    goals=[wanted|(v<<16) for v in range(512) if v.bit_count()==required]
    backward={state:(None,None) for state in goals}
    frontier=goals
    for _ in range(min(2,k-first_depth)):
        next_layer=[]
        for state in frontier:
            for action,child in expand(state):
                if child in backward:
                    continue
                backward[child]=(state,action)
                if child in forward:
                    answer=prefix(child)
                    while backward[child][0] is not None:
                        child,action=backward[child]
                        answer.append(action)
                    return answer
                next_layer.append(child)
        frontier=next_layer
    return None
