"""Retain an incumbent prefix and rebuild a large suffix backward."""

def improve(m,n,d,c,k,grid,target,stamp,reference,width=24,cuts=(.25,.5,.75),refine=True):
    nn=n*n;side=n-d+1
    indices,_,ops,_,_=m.build(n,d,target);actions=list(zip(indices,ops))
    initial=grid+stamp
    def value(path):
        board=initial[:]
        for aid in path:m._st(board,nn,indices[aid])
        return sum(a==b for a,b in zip(board,target))
    path=[(x*side+y)*4+r for x,y,r in reference]
    best=path;score=value(path)
    upper=m.color_bound(initial,target)
    for fraction in cuts:
        if score==upper:break
        cut=int(len(path)*fraction)
        board=initial[:]
        for aid in path[:cut]:m._st(board,nn,indices[aid])
        suffix=m.seven_backward_construct(n,d,c,k-cut,board[:nn],target,board[nn:],width=width)
        candidate=path[:cut]+[(x*side+y)*4+r for x,y,r in suffix]
        if refine:
            candidate=m.refine(n,d,k,initial,target,actions,candidate,passes=4)
            candidate=m.pair_sweep(n,d,k,initial,target,actions,candidate,passes=2,width=24)
        result=value(candidate)
        if result>score:best,score=candidate,result
    return [ops[x]for x in best]
