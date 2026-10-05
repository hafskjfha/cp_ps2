"""Beam over exact two-operation edges, including low-gain setup actions."""
import random


def choices(state,rng,branch):
    planes=[0]*5
    for j,color in enumerate(state.stamp):
        carry=state.target_bits[j][color];p=0
        while carry:
            old=planes[p];planes[p]=old^carry;carry&=old;p+=1
    carry=0
    for p in range(4):
        a,b=planes[p],state.old_planes[p];different=a^b
        planes[p]=different^carry;carry=a&b|different&carry
    planes[4]=carry
    remaining=state.all_actions;count=len(state.actions);seen=set();out=[];top=None
    quota=max(2,branch//4)
    while remaining and len(out)<branch:
        candidates,value=remaining,0
        for p in range(4,-1,-1):
            hits=candidates&planes[p]
            if hits:candidates=hits;value|=1<<p
        if top is None:top=value
        if value<top-3:break
        remaining^=candidates;take=min(branch-len(out),quota)
        while candidates and take:
            offset=rng.randrange(count);after=candidates>>offset
            rank=(after&-after).bit_length()-1+offset if after else (candidates&-candidates).bit_length()-1
            candidates^=1<<rank;aid=state.order[rank]
            outgoing=bytes(state.grid[p]for p in state.actions[aid][0])
            key=(outgoing,value)
            if key in seen:continue
            seen.add(key);out.append(aid);take-=1
    out.extend(rng.randrange(count)for _ in range(max(2,branch//4)))
    return out


def construct(m,n,d,c,k,grid,target,stamp,width=16,branch=12,strength=0,seed=0,mode=0,refine=True):
    nn=n*n
    indices,_,ops,_,_=m.build(n,d,target)
    initial=m.ClusterState(n,d,c,grid[:],target,stamp[:])
    upper=m.color_bound(grid+stamp,target)
    beam=[(initial,[])];best=[];bestscore=initial.matches
    rng=random.Random(sum((i+51)*v for i,v in enumerate(grid+stamp))+k*917+seed*941)
    count=len(indices)
    for depth in range(0,k,2):
        candidates=[];seen=set()
        for state,path in beam:
            for aid in choices(state,rng,branch):
                if path and aid==path[-1]:continue
                child=m.clone_cluster_state(state);child.apply(aid)
                p2=path+[aid]
                if child.matches>bestscore:best,bestscore=p2,child.matches
                if bestscore==upper:return [ops[x]for x in best]
                if depth+1<k:
                    gain,mask=child.best_candidates()
                    mask&=~(1<<aid)
                    if not mask:
                        remaining=[a for a,_ in m.million_choices(child,rng,8)if a!=aid]
                        if not remaining:continue
                        second=remaining[0]
                    else:
                        offset=rng.randrange(count);after=mask>>offset
                        second=(after&-after).bit_length()-1+offset if after else (mask&-mask).bit_length()-1
                    child.apply(second);p2=p2+[second]
                    if child.matches>bestscore:best,bestscore=p2,child.matches
                    if bestscore==upper:return [ops[x]for x in best]
                key=bytes(child.grid+child.stamp)
                if key in seen:continue
                seen.add(key)
                future=max(0,child.best()[0])if depth+2<k else 0
                priority=child.matches+.5*future
                candidates.append((priority,rng.random(),child,p2))
        if not candidates:break
        candidates.sort(key=lambda row:row[:2],reverse=True)
        beam=[];counts={};deferred=[]
        for _,_,child,path in candidates:
            sig=tuple(child.stamp)
            if counts.get(sig,0)>=max(2,width//4):deferred.append((child,path));continue
            counts[sig]=counts.get(sig,0)+1;beam.append((child,path))
            if len(beam)>=width:break
        if len(beam)<width:beam.extend(deferred[:width-len(beam)])
    path=best
    if refine:
        actions=list(zip(indices,ops))
        path=m.refine(n,d,k,grid+stamp,target,actions,path,passes=6)
        path=m.pair_sweep(n,d,k,grid+stamp,target,actions,path,passes=2,width=24)
    return [ops[x]for x in path]
