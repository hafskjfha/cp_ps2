def packed_transitions():
    rotations=[]
    for r in range(4):
        rows=[]
        for u in range(3):
            table=[]
            for value in range(512):
                result=0
                for v in range(3):
                    x,y=((u,v),(v,2-u),(2-u,2-v),(2-v,u))[r]
                    result|=((value>>(3*v))&7)<<(3*(x*3+y))
                table.append(result)
            rows.append(table)
        rotations.append(rows)
    board_mask=(1<<48)-1
    patches=[]
    for x in range(2):
        for y in range(2):
            shift=3*(4*x+y)
            mask=board_mask^((511|(511<<12)|(511<<24))<<shift)
            patches.append((shift,mask))
    def rotate(value,r):
        tables=rotations[r]
        return tables[0][value&511]|tables[1][(value>>9)&511]|tables[2][value>>18]
    def expand(state):
        board,stamp=state&board_mask,state>>48
        rotated=[rotate(stamp,r) for r in range(4)]
        scatter=[(v&511)|((v&261632)<<3)|((v&133955584)<<6) for v in rotated]
        for p,(shift,mask) in enumerate(patches):
            shifted=board>>shift
            patch=(shifted&511)|((shifted>>3)&261632)|((shifted>>6)&133955584)
            retained=board&mask
            for r in range(4):
                child=retained|(scatter[r]<<shift)|(rotate(patch,(-r)&3)<<48)
                yield p*4+r,child
    return expand


def packed_late_beam(grid,target,stamp,k,width=512):
    if k<=0:
        return []
    import heapq
    initial=sum(v<<(3*i) for i,v in enumerate(grid+stamp))
    wanted=sum(v<<(3*i) for i,v in enumerate(target))
    comparison_mask=sum(1<<(3*i) for i in range(16))
    def matches(state):
        diff=state^wanted
        return 16-((diff|(diff>>1)|(diff>>2))&comparison_mask).bit_count()
    best_score=matches(initial)
    upper=color_bound(grid+stamp,target)
    if best_score==upper:
        return []
    best=[]
    expand=packed_transitions()
    rng=random.Random(initial+k*8819)
    frontier=[(initial,b'')]
    visited={initial}
    for depth in range(min(k,80)):
        candidates={}
        for state,path in frontier:
            for aid,child in expand(state):
                if child in visited or child in candidates:
                    continue
                score=matches(child)
                new_path=path+bytes((aid,))
                if score>best_score:
                    best_score,best=score,new_path
                    if score==upper:
                        return list(best)
                candidates[child]=(score,rng.getrandbits(32),new_path)
        if not candidates:
            break
        chosen=heapq.nlargest(width,candidates,key=candidates.get)
        frontier=[(state,candidates[state][2]) for state in chosen]
        visited.update(chosen)
    return list(best)


def solve(n,d,c,k,grid,target,stamp):
    reference=solve_without_late_beam(n,d,c,k,grid,target,stamp)
    if n!=4 or d!=3 or len(reference)>=k:
        return reference
    indices,_,ops,_,_=build(n,d,target)
    board,buffer=grid[:],stamp[:]
    for x,y,r in reference:
        transition(board,buffer,indices[(x*2+y)*4+r])
    tail=packed_late_beam(board,target,buffer,k-len(reference))
    return reference+[ops[aid] for aid in tail]
