"""Pattern-directed pickup actions can prepare a useful stamp at a grid cost."""
import random


def construct(m,n,d,c,k,grid,target,stamp,width=16,branch=6,strength=.5,seed=0,mode=0,refine=True):
    if n<8 or k<8:return []
    nn=n*n;dd=d*d
    indices,_,ops,_,_=m.build(n,d,target)
    patterns={tuple(target[p] for p in indices[a]) for a in range(0,len(indices),4)}
    if len(patterns)>4*c:return []
    patterns=sorted({tuple(target[p] for p in patch) for patch in indices})
    actions=list(zip(indices,ops));wild=[6]*dd
    initial=m.RefineState(n,d,grid+stamp,target,actions,list(range(len(actions))))
    initial.grid=bytearray(initial.grid);initial.stamp=bytearray(initial.stamp)
    base=sum(a==b for a,b in zip(grid,target));upper=m.color_bound(grid+stamp,target)
    beam=[(initial,[],base)];best=[];bestscore=base
    rng=random.Random(sum((i+219)*v for i,v in enumerate(grid+stamp))+k*8831+seed)
    for depth in range(k):
        candidates=[];seen=set()
        for state,path,score in beam:
            choices=[]
            state.wstamp=wild
            direct=state.best()[0]
            if direct>=0:choices.append(direct)
            wishes=patterns if len(patterns)<=branch else rng.sample(patterns,branch)
            for goal in wishes:
                state.wstamp=goal
                aid,gain=state.best()
                if aid>=0:choices.append(aid)
            state.wstamp=wild
            for aid in dict.fromkeys(choices):
                if path and aid==path[-1]:continue
                patch=indices[aid]
                gain=sum((state.stamp[j]==target[p])-(state.grid[p]==target[p]) for j,p in enumerate(patch))
                child=object.__new__(m.RefineState);child.__dict__=state.__dict__.copy()
                child.grid=state.grid[:];child.stamp=state.stamp[:]
                child.values=[row[:] for row in state.values];child.old_planes=state.old_planes[:]
                child.apply(aid)
                key=bytes(child.grid+child.stamp)
                if key in seen:continue
                seen.add(key);value=score+gain;p2=path+[aid]
                if value>bestscore:best,bestscore=p2,value
                if value==upper:return [ops[a] for a in best]
                future=child.best()[1] if depth+1<k else 0
                candidates.append((value+strength*future,rng.random(),child,p2,value))
        if not candidates:break
        candidates.sort(key=lambda x:x[:2],reverse=True)
        beam=[row[2:] for row in candidates[:width]]
    if refine:
        best=m.refine(n,d,k,grid+stamp,target,actions,best,passes=6)
        best=m.pair_sweep(n,d,k,grid+stamp,target,actions,best,passes=2,width=24)
    return [ops[a] for a in best]
