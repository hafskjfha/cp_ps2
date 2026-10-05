def complete_spaced_pair(state,i,j,action,fixed_slot,nn,dd):
    middle=state.sequence[i+1:j]
    if fixed_slot==0:
        before=state.prefix[i][:]
        for chosen in [action]+middle:
            if chosen>=0:
                seq_transition(before,nn,state.actions[chosen][0])
        second,_=best_action(before,state.wishes[j+1],state.actions,nn,dd,
                             current=state.sequence[j],allow_zero=True)
        return [action]+middle+[second]
    wished=state.wishes[j+1][:]
    for chosen in [action]+middle[::-1]:
        if chosen>=0:
            seq_transition(wished,nn,state.actions[chosen][0])
    first,_=best_action(state.prefix[i],wished,state.actions,nn,dd,
                        current=state.sequence[i],allow_zero=True)
    return [first]+middle+[action]


def pair_repair(n,d,k,initial,target,actions,sequence,proposals=None):
    if k<2:
        return sequence
    nn,dd=n*n,d*d
    state=SequenceState(initial,target,actions,sequence+[-1]*(k-len(sequence)),nn)
    if state.score==nn:
        return sequence
    rng=random.Random(sum((i+7)*v for i,v in enumerate(initial))+k*977+9167)
    width=n-d+1
    if proposals is None:
        proposals=min(2400,max(160,450000//nn))
    for step in range(proposals):
        gap=1 if step%2==0 else rng.randint(2,min(12,k-1)) if k>2 else 1
        i=rng.randrange(k-gap)
        j=i+gap
        fixed_slot=(step//2)%2
        old=state.sequence[j if fixed_slot else i]
        mode=rng.randrange(5)
        if mode<2 and old>=0:
            x,y,r=actions[old][1]
            x=min(width-1,max(0,x+rng.choice((-2,-1,0,0,1,2))))
            y=min(width-1,max(0,y+rng.choice((-2,-1,0,0,1,2))))
            action=((x*width+y)*4+rng.randrange(4))
        elif mode==4:
            action=-1
        else:
            action=rng.randrange(len(actions))
        replacements=complete_spaced_pair(state,i,j,action,fixed_slot,nn,dd)
        if state.sequence[i:j+1]==replacements:
            continue
        delta=state.delta(i,replacements)
        if delta>0 or (delta==0 and rng.randrange(8)==0):
            state.accept(i,replacements,delta)
            if state.score==nn:
                break
    return [aid for aid in state.sequence if aid>=0]
