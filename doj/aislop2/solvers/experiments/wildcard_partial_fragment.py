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


def wildcard_partial(n,grid,target,stamp,k):
    if k<=0:
        return None
    nn=n*n
    missing=[p for p in range(nn) if grid[p]!=target[p]]
    if not missing or color_bound(grid+stamp,target)<=nn-len(missing):
        return None
    expand=packed3_transitions(n)
    initial=sum(v<<(3*i) for i,v in enumerate(grid+stamp))
    forward={initial:b''}
    frontier=[initial]
    forward_depth=min(3,k)
    for _ in range(forward_depth):
        next_layer=[]
        for state in frontier:
            path=forward[state]
            for aid,child in expand(state):
                if child not in forward:
                    forward[child]=path+bytes((aid,))
                    next_layer.append(child)
        frontier=next_layer
    states=list(forward)
    byte_count=(len(states)+7)//8
    buffers=[[bytearray(byte_count) for _ in range(6)] for _ in range(nn+9)]
    for index,state in enumerate(states):
        offset,bit=index>>3,1<<(index&7)
        for row in buffers:
            row[state&7][offset]|=bit
            state>>=3
    indexes=[[int.from_bytes(buf,'little') for buf in row] for row in buffers]
    counts=[[bits.bit_count() for bits in row] for row in indexes]
    all_bits=(1<<len(states))-1
    def matching_state(wishes):
        constraints=[]
        for p in range(nn+9):
            color=wishes&7
            wishes>>=3
            if color!=7:
                constraints.append((counts[p][color],indexes[p][color]))
        constraints.sort(key=lambda pair:pair[0])
        hits=all_bits
        for _,bits in constraints:
            hits&=bits
            if not hits:
                return None
        return states[(hits&-hits).bit_length()-1]
    unknown=set(missing)
    goals=[]
    for fixed in missing:
        wishes=[target[p] if p==fixed or p not in unknown else 7 for p in range(nn)]+[7]*9
        goals.append(sum(v<<(3*i) for i,v in enumerate(wishes)))
    backward={goal:b'' for goal in goals}
    frontier=goals
    for goal in goals:
        match=matching_state(goal)
        if match is not None:
            return list(forward[match])
    for _ in range(min(2,k-forward_depth)):
        next_layer=[]
        for state in frontier:
            path=backward[state]
            for aid,child in expand(state):
                if child in backward:
                    continue
                new_path=path+bytes((aid,))
                backward[child]=new_path
                match=matching_state(child)
                if match is not None:
                    return list(forward[match]+new_path[::-1])
                next_layer.append(child)
        frontier=next_layer
    return None


def solve(n,d,c,k,grid,target,stamp):
    reference=solve_without_partial(n,d,c,k,grid,target,stamp)
    if n not in (5,6) or d!=3 or len(reference)>=k:
        return reference
    indices,_,ops,_,_=build(n,d,target)
    board,buffer=grid[:],stamp[:]
    width=n-d+1
    for x,y,r in reference:
        transition(board,buffer,indices[(x*width+y)*4+r])
    missing=sum(a!=b for a,b in zip(board,target))
    if not 1<=missing<=4:
        return reference
    tail=wildcard_partial(n,board,target,buffer,k-len(reference))
    return reference+[ops[aid] for aid in tail] if tail is not None else reference
