"""Escape sequence minima by temporarily dropping subsets of cell objectives."""
import random


def improve(m,n,d,c,k,grid,target,stamp,reference,trials=16):
    nn=n*n;side=n-d+1;initial=grid+stamp
    indices,_,ops,_,_=m.build(n,d,target);actions=list(zip(indices,ops))
    best=[(x*side+y)*4+r for x,y,r in reference]
    def score(seq):
        values=initial[:]
        for aid in seq:m._st(values,nn,indices[aid])
        return sum(a==b for a,b in zip(values,target)),values
    bestscore,final=score(best);upper=m.color_bound(initial,target)
    if k<4 or bestscore==upper:return reference
    rng=random.Random(sum((j+373)*v for j,v in enumerate(initial))+k*5871)
    current=best[:]
    for trial in range(trials):
        kind=trial%4
        if kind==0:
            rate=(.15,.3,.5,.7)[(trial//4)%4]
            weights=[int(rng.random()>rate) for _ in target]
        elif kind==1:
            color=rng.randrange(c)
            weights=[int(v!=color) for v in target]
        elif kind==2:
            mistakes=[p for p in range(nn) if final[p]!=target[p]]
            center=rng.choice(mistakes) if mistakes else rng.randrange(nn)
            weights=[int(abs(p//n-center//n)>d or abs(p%n-center%n)>d) for p in range(nn)]
        else:
            axis=rng.randrange(2);cut=rng.randrange(n)
            weights=[int((p//n if axis else p%n)>=cut) for p in range(nn)]
        candidate=m.weighted_refine(n,d,k,initial,target,weights,actions,current,passes=2)
        candidate=m.refine(n,d,k,initial,target,actions,candidate,passes=5,seed_offset=trial*7619+120043)
        value,row=score(candidate)
        if value>=bestscore:
            best,bestscore,final=candidate[:],value,row
            if value==upper:break
        current=candidate if value>=bestscore-2 else best[:]
        if trial%4==3:current=best[:]
    return [ops[x] for x in best]
