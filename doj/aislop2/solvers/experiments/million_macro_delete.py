def million_deletions(n,d,initial,target,indices,sequence,reverse=False,cap=48):
    nn=n*n
    sequence=sequence[:]
    for iteration in range(cap):
        state=initial[:];forward=[]
        for aid in sequence:
            forward.append(state[:]);_st(state,nn,indices[aid])
        wishes=target+[6]*(d*d)
        chosen=-1;bestgain=0
        for i in range(len(sequence)-1,-1,-1):
            before=forward[i];gain=0
            for j,p in enumerate(indices[sequence[i]]):
                a,b=before[p],before[nn+j]
                wa,wb=wishes[p],wishes[nn+j]
                gain+=(a==wa)+(b==wb)-(b==wa)-(a==wb)
            if gain>=bestgain:
                chosen=i;bestgain=gain
                if reverse and gain>=0:break
            _st(wishes,nn,indices[sequence[i]])
        if chosen<0:break
        sequence.pop(chosen)
    return sequence

def million_delete_route(n,d,c,k,grid,target,stamp,reference,reverse=False):
    nn=n*n;side=n-d+1;initial=grid+stamp
    indices,_,ops,_,_=build(n,d,target)
    sequence=[(x*side+y)*4+r for x,y,r in reference]
    state=initial[:]
    for aid in sequence:_st(state,nn,indices[aid])
    baseline=sum(a==b for a,b in zip(state,target))
    if baseline==color_bound(initial,target):return reference
    sequence=million_deletions(n,d,initial,target,indices,sequence,reverse)
    state=initial[:]
    for aid in sequence:_st(state,nn,indices[aid])
    candidate=[ops[aid]for aid in sequence]
    for powers,rounds in [((3,),30)]+[((p,),1)for p in (6,6,9,5,12,3,6,9,12)]:
        tail=route_tail(n,d,state[:nn],target,state[nn:],k-len(candidate),powers,rounds)
        candidate+=tail
        for x,y,r in tail:_st(state,nn,indices[(x*side+y)*4+r])
    value=sum(a==b for a,b in zip(state,target))
    return candidate if value>baseline else reference
