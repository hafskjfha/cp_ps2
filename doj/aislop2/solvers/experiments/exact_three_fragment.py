def exact_three(n,d,c,grid,target,stamp):
    state=State(n,d,c,grid[:],target,stamp[:])
    actions=state.actions
    one,first=state.best()
    best,path=max(0,one),([first] if one>0 else [])
    limit=min(3*d*d,color_bound(grid+stamp,target)-state.matches)
    ranked=sorted(((state.gain(aid),aid) for aid in range(len(actions))),reverse=True)
    seen=set()
    for gain1,first in ranked:
        if gain1+2*d*d<=best:
            break
        state.apply(first)
        signature=bytes(state.grid)+bytes(state.stamp)
        if signature in seen:
            state.apply(first)
            continue
        seen.add(signature)
        for second in range(len(actions)):
            gain2=state.gain(second)
            total=gain1+gain2
            if total>best:
                best,path=total,[first,second]
            if total+d*d<=best:
                continue
            state.apply(second)
            gain3,third=state.best()
            state.apply(second)
            if total+gain3>best:
                best,path=total+gain3,[first,second,third]
            if best==limit:
                break
        state.apply(first)
        if best==limit:
            break
    return [actions[aid][1] for aid in path]
