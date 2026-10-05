"""Reverse beam guided by the spatial shape of unsatisfied source wishes."""
import random
import math


def construct(m,n,d,c,k,grid,target,stamp,width=24,branch=8,strength=.15,seed=0,mode=0,refine=True):
    nn=n*n
    indices,_,ops,_,_=m.build(n,d,target)
    engine=m.FastBack(n,d,grid,target,stamp,indices)
    base=sum(a==b for a,b in zip(grid,target))
    upper=m.color_bound(grid+stamp,target)
    neighbors=[]
    for p in range(nn):
        neighbors.append(((1<<(p-1))if p%n else 0)|((1<<(p+1))if p%n<n-1 else 0)|
                         ((1<<(p-n))if p>=n else 0)|((1<<(p+n))if p<nn-n else 0))
    wrong=sum(1<<p for p in range(nn)if grid[p]!=target[p])
    aux=sum((wrong&neighbors[p]).bit_count()for p in range(nn)if wrong>>p&1)//2
    beam=[(engine.first,[],base,wrong,aux)]
    best=[];bestscore=base
    rng=random.Random(sum((i+83)*v for i,v in enumerate(grid+stamp))+k*1709+seed*941)
    for depth in range(k):
        candidates=[];seen=set()
        for state,path,score,wrong,aux in beam:
            for aid,gain in engine.choices(state,rng,branch):
                if path and aid==path[-1]:continue
                child=engine.apply(state,aid)
                key=bytes(child[0]+child[1])
                if key in seen:continue
                seen.add(key)
                w2=wrong;a2=aux
                for p in indices[aid]:
                    old=bool(wrong>>p&1)
                    new=child[0][p]<6 and child[0][p]!=grid[p]
                    if old!=new:
                        degree=(w2&neighbors[p]).bit_count()
                        a2+=degree if new else -degree
                        w2^=1<<p
                p2=path+[aid];value=score+gain
                if value>bestscore:best,bestscore=p2,value
                if value==upper:return [ops[x]for x in reversed(best)]
                future=max(0,engine.best(child))if depth+1<k else 0
                if mode==1 and depth+2<k:
                    # Two-ply optimistic continuation; action gain remains exact.
                    follow=engine.choices(child,rng,2)
                    future=max((g+max(0,engine.best(engine.apply(child,a)))for a,g in follow),default=0)
                if mode==2:
                    planes=engine.scoreplanes(child);hits=engine.allbits
                    for plane in reversed(planes):
                        yes=hits&plane
                        if yes:hits=yes
                    potential=math.log2(hits.bit_count())
                else:potential=a2
                priority=value+.375*future+strength*potential
                candidates.append((priority,rng.random(),child,p2,value,w2,a2))
        if not candidates:break
        candidates.sort(key=lambda row:row[:2],reverse=True)
        beam=[row[2:]for row in candidates[:width]]
    path=list(reversed(best))
    if refine:
        actions=list(zip(indices,ops))
        path=m.refine(n,d,k,grid+stamp,target,actions,path,passes=6)
        path=m.pair_sweep(n,d,k,grid+stamp,target,actions,path,passes=2,width=24)
    return [ops[x]for x in path]
