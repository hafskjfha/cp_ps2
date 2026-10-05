def million_macro_refine(n,d,c,k,grid,target,stamp,reference):
    nn=n*n;side=n-d+1
    indices,_,ops,_,_=build(n,d,target)
    actions=list(zip(indices,ops));initial=grid+stamp
    state=initial[:];snapshots=[state[:]]
    for x,y,r in reference:
        _st(state,nn,indices[(x*side+y)*4+r]);snapshots.append(state[:])
    score=sum(a==b for a,b in zip(state,target));upper=color_bound(initial,target)
    if score==upper or k<16:return reference
    best=reference;proposals=[]
    for fraction in (0.5,0.75,0.9):
        cut=int(fraction*len(reference));state=snapshots[cut]
        tail=route_tail(n,d,state[:nn],target,state[nn:],k-cut,(3,),30)
        candidate=reference[:cut]+tail;state=state[:]
        for x,y,r in tail:_st(state,nn,indices[(x*side+y)*4+r])
        value=sum(a==b for a,b in zip(state,target))
        if value>score:score=value;best=candidate
        proposals.append((value,-len(candidate),candidate))
    proposals.sort(key=lambda z:z[:2],reverse=True)
    for value,_,candidate in proposals[:2]:
        if value<score-10:continue
        sequence=[(x*side+y)*4+r for x,y,r in candidate]
        sequence=refine(n,d,k,initial,target,actions,sequence,passes=4,seed_offset=7919)
        state=initial[:]
        for aid in sequence:_st(state,nn,indices[aid])
        value=sum(a==b for a,b in zip(state,target))
        if value>score:
            score=value;best=[ops[aid]for aid in sequence]
        if value==upper:break
    return best
