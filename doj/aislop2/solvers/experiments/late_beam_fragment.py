def packed3_transitions(n):
    rotations=[]
    for r in range(4):
        tables=[]
        for u in range(3):
            row=[]
            for value in range(512):
                output=0
                for v in range(3):
                    x,y=((u,v),(v,2-u),(2-u,2-v),(2-v,u))[r]
                    output|=((value>>(3*v))&7)<<(3*(3*x+y))
                row.append(output)
            tables.append(row)
        rotations.append(tables)
    shift_stamp=3*n*n
    board_mask=(1<<shift_stamp)-1
    stride=3*n
    patches=[]
    for x in range(n-2):
        for y in range(n-2):
            shift=3*(n*x+y)
            mask=board_mask^((511|(511<<stride)|(511<<(2*stride)))<<shift)
            patches.append((shift,mask))
    def rotate(value,r):
        tables=rotations[r]
        return tables[0][value&511]|tables[1][(value>>9)&511]|tables[2][value>>18]
    def expand(state):
        board,stamp=state&board_mask,state>>shift_stamp
        rotated=[rotate(stamp,r) for r in range(4)]
        scatter=[(v&511)|(((v>>9)&511)<<stride)|((v>>18)<<(2*stride)) for v in rotated]
        for p,(shift,mask) in enumerate(patches):
            shifted=board>>shift
            patch=(shifted&511)|(((shifted>>stride)&511)<<9)|(((shifted>>(2*stride))&511)<<18)
            retained=board&mask
            for r in range(4):
                yield 4*p+r,retained|(scatter[r]<<shift)|(rotate(patch,(-r)&3)<<shift_stamp)
    return expand


def late_beam_finish(n,grid,target,stamp,k):
    if k<=0:
        return None
    nn=n*n
    initial_score=sum(a==b for a,b in zip(grid,target))
    if initial_score==color_bound(grid+stamp,target):
        return None
    expand=packed3_transitions(n)
    initial=sum(v<<(3*i) for i,v in enumerate(grid+stamp))
    wanted=sum(v<<(3*i) for i,v in enumerate(target))
    comparison_mask=sum(1<<(3*i) for i in range(nn))
    rng=random.Random(initial+k*997)
    import heapq
    frontier=[(initial,b'')]
    visited={initial}
    for depth in range(min(6,k)):
        candidates={}
        for state,path in frontier:
            for aid,child in expand(state):
                if child in visited or child in candidates:
                    continue
                new_path=path+bytes((aid,))
                diff=child^wanted
                score=nn-((diff|(diff>>1)|(diff>>2))&comparison_mask).bit_count()
                if score>initial_score:
                    return list(new_path)
                candidates[child]=(score,rng.getrandbits(32),new_path)
        if not candidates:
            break
        selected=heapq.nlargest(256,candidates,key=candidates.get)
        frontier=[(state,candidates[state][2]) for state in selected]
        visited.update(selected)
    return None


def solve(n,d,c,k,grid,target,stamp):
    reference=solve_without_late_beam(n,d,c,k,grid,target,stamp)
    if not 5<=n<=9 or d!=3 or len(reference)>=k:
        return reference
    indices,_,ops,_,_=build(n,d,target)
    board,buffer=grid[:],stamp[:]
    width=n-d+1
    for x,y,r in reference:
        transition(board,buffer,indices[(x*width+y)*4+r])
    missing=sum(a!=b for a,b in zip(board,target))
    if not 1<=missing<=8:
        return reference
    candidate=reference[:]
    for _ in range(2):
        tail=late_beam_finish(n,board,target,buffer,k-len(candidate))
        if tail is None:
            break
        for aid in tail:
            transition(board,buffer,indices[aid])
            candidate.append(ops[aid])
    return candidate
