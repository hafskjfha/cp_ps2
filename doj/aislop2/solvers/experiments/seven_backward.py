"""Backward wildcard beam construction (research fragment)."""
import random

def choices(state,rng,branch=6):
    planes=[0]*5
    for j in range(state.dd):
        for carry in (state.values[j][state.wstamp[j]],state.goals[j][state.stamp[j]]):
            level=0
            while carry:
                old=planes[level];planes[level]=old^carry;carry&=old;level+=1
    carry=0
    for level in range(5):
        a,b=planes[level],state.old_planes[level]
        diff=a^b;planes[level]=diff^carry;carry=a&b|diff&carry
    remaining=state.all_bits
    out=[]
    subtract=state.dd+sum(a==b for a,b in zip(state.stamp,state.wstamp))
    count=len(state.actions)
    while remaining and len(out)<branch:
        candidates,value=remaining,0
        for level in range(4,-1,-1):
            hits=candidates&planes[level]
            if hits:candidates=hits;value|=1<<level
        remaining^=candidates
        for _ in range(min(branch-len(out),4)):
            if not candidates:break
            offset=rng.randrange(count)
            after=candidates>>offset
            aid=(after&-after).bit_length()-1+offset if after else (candidates&-candidates).bit_length()-1
            candidates^=1<<aid
            out.append((aid,value-subtract))
        if out and value-subtract<out[0][1]-1:break
    return out

def clone(state,side=True):
    child=object.__new__(type(state))
    child.__dict__=state.__dict__.copy()
    if side:
        child.wishes=state.wishes[:]
        child.wstamp=state.wstamp[:]
        child.goals=[row[:] for row in state.goals]
    else:
        child.grid=state.grid[:]
        child.stamp=state.stamp[:]
        child.values=[row[:] for row in state.values]
    child.old_planes=state.old_planes[:]
    return child

def construct(m,n,d,c,k,grid,target,stamp,width=24,branch=6,future_weight=3,mixed=0):
    nn=n*n
    indices,_,ops,_,_=m.build(n,d,target)
    actions=list(zip(indices,ops))
    initial=grid+stamp
    first=m.RefineState(n,d,initial,target,actions,list(range(len(actions))))
    base=sum(a==b for a,b in zip(grid,target))
    upper=m.color_bound(initial,target)
    beam=[(first,[],[],base)]
    best,bestscore=[],base
    rng=random.Random(sum((i+83)*v for i,v in enumerate(initial))+k*1709)
    for depth in range(k):
        candidates=[];seen=set()
        for state,forward,backward,score in beam:
            for aid,gain in choices(state,rng,branch):
                if (forward and aid==forward[-1])or(backward and aid==backward[-1]):continue
                for side in ((True,False)if mixed==1 else (bool(depth%2),)if mixed==2 else (True,)):
                    child=clone(state,side)
                    child.apply(aid,wishes=side)
                    key=bytes(child.wishes+child.wstamp+child.grid+child.stamp)
                    if key in seen:continue
                    seen.add(key)
                    fwd=forward if side else forward+[aid]
                    back=backward+[aid]if side else backward
                    value=score+gain
                    if value>bestscore:best,bestscore=fwd+list(reversed(back)),value
                    if value==upper:
                        return [ops[x] for x in best]
                    future=child.best()[1] if depth+1<k else 0
                    candidates.append((value*8+future_weight*future,rng.random(),child,fwd,back,value))
        if not candidates:break
        candidates.sort(key=lambda row:row[:2],reverse=True)
        beam=[(child,fwd,back,value)for _,_,child,fwd,back,value in candidates[:width]]
    path=best
    path=m.refine(n,d,k,initial,target,actions,path,passes=6)
    path=m.pair_sweep(n,d,k,initial,target,actions,path,passes=2,width=24)
    return [ops[x] for x in path]
