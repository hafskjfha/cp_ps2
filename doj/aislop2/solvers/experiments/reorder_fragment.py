def reorder_sequence(n,d,k,initial,target,actions,sequence):
    length=len(sequence)
    if length<2:
        return sequence
    state=SequenceState(initial,target,actions,sequence,n*n)
    upper=color_bound(initial,target)
    if state.score==upper:
        return sequence
    rng=random.Random(sum((i+11)*v for i,v in enumerate(initial))+k*373)
    pairs=[(i,i+gap) for gap in range(1,min(7,length)) for i in range(length-gap)]
    for _ in range(2):
        rng.shuffle(pairs)
        changed=False
        for i,j in pairs:
            block=state.sequence[i:j+1]
            candidates=(block[1:]+block[:1],block[-1:]+block[:-1],
                        block[-1:]+block[1:-1]+block[:1])
            best_delta,best=0,None
            for candidate in candidates:
                if candidate==block:
                    continue
                delta=state.delta(i,candidate)
                if delta>best_delta:
                    best_delta,best=delta,candidate
            if best is not None:
                state.accept(i,best,best_delta)
                changed=True
                if state.score==upper:
                    return state.sequence
        if not changed:
            break
    return state.sequence
