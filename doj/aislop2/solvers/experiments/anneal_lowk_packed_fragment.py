def lowk_packed_transitions(n,d):
    row_bits=3*d
    row_mask=(1<<row_bits)-1
    stride=3*n
    rotations=[]
    for r in range(4):
        rows=[]
        for u in range(d):
            table=[]
            for value in range(1<<row_bits):
                result=0
                for v in range(d):
                    x,y=((u,v),(v,d-1-u),(d-1-u,d-1-v),(d-1-v,u))[r]
                    result|=((value>>(3*v))&7)<<(3*(x*d+y))
                table.append(result)
            rows.append(table)
        rotations.append(rows)
    stamp_shift=3*n*n
    board_mask=(1<<stamp_shift)-1
    stencil=sum(row_mask<<(u*stride) for u in range(d))
    patches=[(3*(x*n+y),board_mask^(stencil<<(3*(x*n+y))))
             for x in range(n-d+1) for y in range(n-d+1)]
    if d==2:
        def rotate(value,r):
            tables=rotations[r]
            return tables[0][value&63]|tables[1][(value>>6)&63]
        def expand(state):
            board,stamp=state&board_mask,state>>stamp_shift
            rotated=[rotate(stamp,r) for r in range(4)]
            scatter=[(v&63)|((v>>6)<<stride) for v in rotated]
            for position,(shift,mask) in enumerate(patches):
                shifted=board>>shift
                patch=(shifted&63)|(((shifted>>stride)&63)<<6)
                retained=board&mask
                for r in range(4):
                    yield 4*position+r,retained|(scatter[r]<<shift)|(rotate(patch,(-r)&3)<<stamp_shift)
    else:
        def rotate(value,r):
            tables=rotations[r]
            return tables[0][value&511]|tables[1][(value>>9)&511]|tables[2][value>>18]
        def expand(state):
            board,stamp=state&board_mask,state>>stamp_shift
            rotated=[rotate(stamp,r) for r in range(4)]
            scatter=[(v&511)|(((v>>9)&511)<<stride)|((v>>18)<<(2*stride)) for v in rotated]
            for position,(shift,mask) in enumerate(patches):
                shifted=board>>shift
                patch=(shifted&511)|(((shifted>>stride)&511)<<9)|(((shifted>>(2*stride))&511)<<18)
                retained=board&mask
                for r in range(4):
                    yield 4*position+r,retained|(scatter[r]<<shift)|(rotate(patch,(-r)&3)<<stamp_shift)
    return expand


def lowk_packed_beam(n,d,k,grid,target,stamp):
    import heapq
    nn=n*n
    best_score=sum(a==b for a,b in zip(grid,target))
    limit=color_bound(grid+stamp,target)
    if k<=0 or best_score==limit:
        return []
    action_count=4*(n-d+1)**2
    width=min(96,max(1,100000//action_count))
    codes=[aid.to_bytes(2,'little') for aid in range(action_count)]
    initial=sum(v<<(3*i) for i,v in enumerate(grid+stamp))
    wanted=sum(v<<(3*i) for i,v in enumerate(target))
    mask=sum(1<<(3*i) for i in range(nn))
    expand=lowk_packed_transitions(n,d)
    seed=sum((i+53)*v for i,v in enumerate(grid+target+stamp))+n*1013+d*971+k*7187
    rng=random.Random(seed)
    frontier=[(initial,b'')]
    visited={initial}
    best_path=b''
    for depth in range(k):
        candidates={}
        last=depth+1==k
        for state,path in frontier:
            for aid,child in expand(state):
                if child in visited or child in candidates:
                    continue
                diff=child^wanted
                score=nn-((diff|(diff>>1)|(diff>>2))&mask).bit_count()
                if score>best_score:
                    best_score,best_path=score,path+codes[aid]
                    if best_score==limit:
                        return [best_path[i]|(best_path[i+1]<<8) for i in range(0,len(best_path),2)]
                if not last:
                    candidates[child]=(score,rng.getrandbits(32),path,aid)
        if last or not candidates:
            break
        chosen=heapq.nlargest(width,candidates,key=candidates.get)
        frontier=[(state,candidates[state][2]+codes[candidates[state][3]]) for state in chosen]
        visited.update(chosen)
    return [best_path[i]|(best_path[i+1]<<8) for i in range(0,len(best_path),2)]


def solve(n,d,c,k,grid,target,stamp):
    reference=solve_without_lowk_packed(n,d,c,k,grid[:],target,stamp[:])
    if n<10 or not 4<=k<=8:
        return reference
    indices,_,operations,_,_=build(n,d,target)
    actions=list(zip(indices,operations))
    width=n-d+1
    initial=grid+stamp
    reference_ids=[((x*width+y)*4+r) for x,y,r in reference]
    final=initial[:]
    for aid in reference_ids:
        seq_transition(final,n*n,indices[aid])
    best_score=sum(a==b for a,b in zip(final,target))
    if best_score==color_bound(initial,target):
        return reference
    candidate=lowk_packed_beam(n,d,k,grid,target,stamp)
    candidate=refine(n,d,k,initial,target,actions,candidate,passes=2)
    final=initial[:]
    for aid in candidate:
        seq_transition(final,n*n,indices[aid])
    if sum(a==b for a,b in zip(final,target))>best_score:
        return [operations[aid] for aid in candidate]
    return reference
