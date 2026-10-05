def finish_macros(n,d,k,initial,target,actions,sequence):
    nn=n*n
    final=initial[:]
    for action in sequence:
        seq_transition(final,nn,actions[action][0])
    available,needed=[0]*6,[0]*6
    for color in initial:
        available[color]+=1
    for color in target:
        needed[color]+=1
    upper=sum(min(a,b) for a,b in zip(available,needed))
    score=sum(a==b for a,b in zip(final,target))
    if score==upper or len(sequence)+3>k:
        return sequence
    state=RefineState(n,d,final,target,actions,list(range(len(actions))))
    rng=random.Random(sum((i+1)*v for i,v in enumerate(initial))+29137)
    sequence=sequence[:]
    macros=0
    while len(sequence)<k and score<upper:
        action,gain=state.best()
        if gain>0:
            chosen=(action,)
        elif len(sequence)+3<=k and macros<8:
            gain,pair=best_patch_exchange(state,None,rng)
            if pair is None:
                break
            chosen=(pair[0],pair[1],pair[0])
            macros+=1
        else:
            break
        for action in chosen:
            state.apply(action)
            sequence.append(action)
        score+=gain
    return sequence


def solve(n,d,c,k,grid,target,stamp):
    operations=solve_without_macros(n,d,c,k,grid,target,stamp)
    if len(operations)+3>k:
        return operations
    indices,_,ops,_,_=build(n,d,target)
    actions=list(zip(indices,ops))
    width=n-d+1
    sequence=[((x*width+y)*4+r) for x,y,r in operations]
    sequence=finish_macros(n,d,k,grid+stamp,target,actions,sequence)
    return [actions[action][1] for action in sequence]
