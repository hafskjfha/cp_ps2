_PACKED_EXPAND = None
_WILDCARD_BACKWARD = None


def wildcard_backward_records(expand,wanted):
    goal=wanted|(((1<<27)-1)<<48)
    backward={goal:b''}
    frontier=[goal]
    for depth in range(1,5):
        next_layer=[]
        for state in frontier:
            path=backward[state]
            for aid,child in expand(state):
                if child in backward:
                    continue
                new_path=path+bytes((aid,))
                backward[child]=new_path
                next_layer.append(child)
                wishes=child
                constraints=bytearray()
                for position in range(25):
                    color=wishes&7
                    wishes>>=3
                    if color!=7:
                        constraints.append(position*6+color)
                yield depth,new_path,bytes(constraints)
        frontier=next_layer


def wildcard_finish(grid,target,stamp,k,depth=8):
    global _PACKED_EXPAND,_WILDCARD_BACKWARD
    if grid==target:
        return []
    if color_bound(grid+stamp,target)<16:
        return None
    if _PACKED_EXPAND is None:
        _PACKED_EXPAND=packed_transitions()
    expand=_PACKED_EXPAND
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
    indexes=[int.from_bytes(buf,'little') for row in buffers for buf in row]
    counts=[bits.bit_count() for bits in indexes]
    counts_get=counts.__getitem__
    all_bits=(1<<len(states))-1
    if _WILDCARD_BACKWARD is None or _WILDCARD_BACKWARD[0]!=wanted:
        _WILDCARD_BACKWARD=[wanted,[],wildcard_backward_records(expand,wanted)]
    cache=_WILDCARD_BACKWARD
    records=cache[1]
    cursor=0
    while True:
        if cursor==len(records):
            if cache[2] is None:
                break
            record=next(cache[2],None)
            if record is None:
                cache[2]=None
                break
            records.append(record)
        level,new_path,encoded=records[cursor]
        if level>backward_depth:
            break
        cursor+=1
        hits=all_bits
        for identifier in sorted(encoded,key=counts_get):
            hits&=indexes[identifier]
            if not hits:
                break
        if hits:
            match=states[(hits&-hits).bit_length()-1]
            return list(forward[match]+new_path[::-1])
    return None


