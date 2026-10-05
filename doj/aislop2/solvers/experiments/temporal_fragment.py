def cancel_inverse_pairs(sequence):
    compact=[]
    for aid in sequence:
        if compact and compact[-1]==aid:
            compact.pop()
        else:
            compact.append(aid)
    return compact


def best_insertion(n,d,initial,target,actions,sequence,seed=0):
    final=initial[:]
    for aid in sequence:
        seq_transition(final,n*n,actions[aid][0])
    order=list(range(len(actions)))
    random.Random(seed).shuffle(order)
    state=RefineState(n,d,final,target,actions,order)
    best=(0,-1,-1)
    for pos in range(len(sequence),-1,-1):
        aid,gain=state.best()
        if gain>best[0]:
            best=gain,pos,aid
        if pos:
            old=sequence[pos-1]
            state.apply(old)
            state.apply(old,wishes=True)
    return best


def deletion_deltas(n,d,initial,target,actions,sequence):
    final=initial[:]
    for aid in sequence:
        seq_transition(final,n*n,actions[aid][0])
    state=RefineState(n,d,final,target,actions,list(range(len(actions))))
    deltas=[0]*len(sequence)
    for pos in range(len(sequence)-1,-1,-1):
        old=sequence[pos]
        state.apply(old)
        deltas[pos]=-operation_gain(state,old)
        state.apply(old,wishes=True)
    return deltas


def temporal_repair(n,d,k,initial,target,actions,sequence,rounds=1,removals=0):
    nn=n*n
    sequence=sequence[:]
    final=initial[:]
    for aid in sequence:
        seq_transition(final,nn,actions[aid][0])
    score=sum(a==b for a,b in zip(final,target))
    upper=color_bound(initial,target)
    for iteration in range(rounds):
        if score==upper:
            break
        seed=sum((p+11)*v for p,v in enumerate(initial))+iteration*10891
        best_gain,best_sequence=0,sequence
        if len(sequence)<k:
            gain,pos,aid=best_insertion(n,d,initial,target,actions,sequence,seed)
            if gain:
                best_gain,best_sequence=gain,sequence[:pos]+[aid]+sequence[pos:]
        if removals and sequence:
            deltas=deletion_deltas(n,d,initial,target,actions,sequence)
            order=sorted(range(len(sequence)),key=lambda p:(deltas[p],-p),reverse=True)
            for remove in order[:removals]:
                child=sequence[:remove]+sequence[remove+1:]
                gain,pos,aid=best_insertion(n,d,initial,target,actions,child,seed+remove)
                gain+=deltas[remove]
                if gain>best_gain:
                    best_gain,best_sequence=gain,child[:pos]+[aid]+child[pos:] if aid>=0 else child
        if best_gain<=0:
            break
        sequence=best_sequence
        score+=best_gain
    return sequence


def solve(n,d,c,k,grid,target,stamp):
    reference=solve_before_temporal(n,d,c,k,grid,target,stamp)
    if k<=2 or len(reference)>=k:
        return reference
    indices,_,ops,_,_=build(n,d,target)
    side=n-d+1
    sequence=[(x*side+y)*4+r for x,y,r in reference]
    candidate=temporal_repair(n,d,k,grid+stamp,target,list(zip(indices,ops)),sequence)
    return [ops[aid] for aid in candidate]
