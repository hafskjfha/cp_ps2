def wildcard_finish(grid,target,stamp,k,depth=8):
    if grid==target:
        return []
    if color_bound(grid+stamp,target)<16:
        return None
    expand=packed_transitions()
    initial=sum(v<<(3*i) for i,v in enumerate(grid+stamp))
    wanted=sum(v<<(3*i) for i,v in enumerate(target))
    board_mask=(1<<48)-1
    forward={initial:b''}
    frontier=[initial]
    forward_depth=min(4,k,depth)
    for _ in range(forward_depth):
        next_layer=[]
        for state in frontier:
            path=forward[state]
            for aid,child in expand(state):
                if child in forward:
                    continue
                new_path=path+bytes((aid,))
                forward[child]=new_path
                if child&board_mask==wanted:
                    return list(new_path)
                next_layer.append(child)
        frontier=next_layer
    backward_depth=min(4,k-forward_depth,depth-forward_depth)
    if backward_depth<=0:
        return None
    states=list(forward)
    byte_count=(len(states)+7)//8
    buffers=[[bytearray(byte_count) for _ in range(6)] for _ in range(25)]
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
        for p in range(25):
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
    goal=wanted|(((1<<27)-1)<<48)
    backward={goal:b''}
    frontier=[goal]
    for _ in range(backward_depth):
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
    reference=solve_without_wildcard(n,d,c,k,grid,target,stamp)
    if n!=4 or d!=3 or len(reference)>=k:
        return reference
    indices,_,ops,_,_=build(n,d,target)
    board,buffer=grid[:],stamp[:]
    for x,y,r in reference:
        transition(board,buffer,indices[(x*2+y)*4+r])
    tail=wildcard_finish(board,target,buffer,k-len(reference))
    return reference+[ops[aid] for aid in tail] if tail is not None else reference
