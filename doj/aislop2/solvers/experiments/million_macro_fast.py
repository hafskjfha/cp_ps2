def macro_prefix_fast(n,d,c,k,grid,target,stamp,reference,cuts=(0.25,0.5,0.75),mixed=False):
    nn=n*n
    indices,_,ops,_,_=build(n,d,target)
    width=n-d+1
    initial=grid+stamp
    final=initial[:]
    snapshots=[final[:]]
    for x,y,r in reference:
        _st(final,nn,indices[(x*width+y)*4+r])
        snapshots.append(final[:])
    score=sum(a==b for a,b in zip(final,target))
    upper=color_bound(initial,target)
    if score==upper or k<12:return reference
    best=reference
    for fraction in cuts:
        cut=int(len(reference)*fraction)
        state=snapshots[cut]
        if sum(a==b for a,b in zip(state,target))+(2 if d==3 else 1)*(k-cut)<=score:continue
        candidate=reference[:cut]
        tail=route_tail(n,d,state[:nn],target,state[nn:],k-cut,(3,),30)
        candidate=candidate+tail
        state=state[:]
        for x,y,r in tail:
            _st(state,nn,indices[(x*width+y)*4+r])
        if mixed:
            for power in (6,9,5,12,3,6,9):
                tail=route_tail(n,d,state[:nn],target,state[nn:],k-len(candidate),(power,),2)
                candidate+=tail
                for x,y,r in tail:
                    _st(state,nn,indices[(x*width+y)*4+r])
        value=sum(a==b for a,b in zip(state,target))
        if value>score:
            score,best=value,candidate
        if value==upper:break
    return best
