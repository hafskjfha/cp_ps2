"""Frozen width16 residual-cluster beam; retains the supplied reference floor."""
import random


def cluster_improve(n,d,c,k,grid,target,stamp,reference,width=16):
    if k<3 or n==d:return reference
    indices,_,ops,_,_=build(n,d,target)
    side=n-d+1;initial_grid=grid+stamp
    best=[(x*side+y)*4+r for x,y,r in reference]
    state_grid=initial_grid[:]
    for aid in best:_st(state_grid,n*n,indices[aid])
    best_score=sum(a==b for a,b in zip(state_grid,target))
    upper=color_bound(initial_grid,target)
    if best_score==upper:return reference
    initial=State(n,d,c,grid[:],target,stamp[:])
    state_seed=sum((i+51)*v for i,v in enumerate(grid+stamp))+k*917
    rng=random.Random(state_seed)
    neighbors=[]
    for p in range(n*n):
        neighbors.append(((1<<(p-1)) if p%n else 0)|
                         ((1<<(p-n)) if p//n else 0)|
                         ((1<<(p+1)) if p%n<n-1 else 0)|
                         ((1<<(p+n)) if p//n<n-1 else 0))
    initial._cluster_wrong=sum(1<<p for p in range(n*n) if grid[p]!=target[p])
    auxiliary=sum(grid[a]!=target[a] and grid[b]!=target[b]
                  for a in range(n*n) for b in (a+1,a+n)
                  if b<n*n and (b==a+n or a//n==b//n))
    beam=[(initial,[],auxiliary)]
    beam_best=[];beam_score=initial.matches
    for depth in range(k):
        candidates=[];seen=set()
        for state,path,auxiliary in beam:
            for aid,gain in million_choices(state,rng,8):
                if path and aid==path[-1]:continue
                child=clone_state(state);child.apply(aid)
                key=bytes(child.grid+child.stamp)
                if key in seen:continue
                seen.add(key)
                wrong=state._cluster_wrong;change=0
                for p in indices[aid]:
                    if (state.grid[p]==target[p]) != (child.grid[p]==target[p]):
                        bit=1<<p;degree=(wrong&neighbors[p]).bit_count()
                        change+=-degree if wrong&bit else degree
                        wrong^=bit
                child._cluster_wrong=wrong
                new_auxiliary=auxiliary+change
                path2=path+[aid]
                if child.matches>beam_score:beam_best,beam_score=path2,child.matches
                if beam_score==upper:return [ops[aid] for aid in beam_best]
                future=max(0,child.best()[0]) if depth+1<k else 0
                priority=child.matches+0.5*future+0.15*new_auxiliary
                candidates.append((priority,rng.random(),child,path2,new_auxiliary))
        if not candidates:break
        candidates.sort(key=lambda row:(row[0],row[1]),reverse=True)
        beam=[];stamp_counts={};deferred=[]
        for _,_,state,path,auxiliary in candidates:
            sig=tuple(state.stamp)
            if stamp_counts.get(sig,0)>=max(2,width//4):
                deferred.append((state,path,auxiliary));continue
            stamp_counts[sig]=stamp_counts.get(sig,0)+1
            beam.append((state,path,auxiliary))
            if len(beam)>=width:break
        if len(beam)<width:beam.extend(deferred[:width-len(beam)])
    actions=list(zip(indices,ops))
    candidate=refine(n,d,k,initial_grid,target,actions,beam_best,passes=6)
    candidate=pair_sweep(n,d,k,initial_grid,target,actions,candidate,passes=2,width=24)
    state_grid=initial_grid[:]
    for aid in candidate:_st(state_grid,n*n,indices[aid])
    value=sum(a==b for a,b in zip(state_grid,target))
    return [ops[aid] for aid in candidate] if value>best_score else reference


_cluster_domain_cache=None

def cluster_domain(n,d,c,k,grid,target,stamp):
    if n<=16 or d!=3 or k<=10:return False
    global _cluster_domain_cache
    key=(n,d,c,k,tuple(grid),tuple(target),tuple(stamp))
    if _cluster_domain_cache is not None and _cluster_domain_cache[0]==key:
        return _cluster_domain_cache[1]
    reverse_eligible=(n>=10 and k>=12 and
                      100*sum(a==b for a,b in zip(grid,target))<88*color_bound(grid+stamp,target))
    if reverse_eligible:
        patterns=set()
        for x in range(n-d+1):
            for y in range(n-d+1):
                patterns.add(tuple(target[(x+i)*n+y+j]for i in range(d)for j in range(d)))
                if len(patterns)>4*c:
                    reverse_eligible=False
                    break
            if not reverse_eligible:break
    result=not reverse_eligible
    _cluster_domain_cache=(key,result)
    return result

_cluster_original_construct_all=construct_all
_cluster_original_million_beam=million_beam

def construct_all(n,d,c,k,grid,target,stamp):
    reference=_cluster_original_construct_all(n,d,c,k,grid,target,stamp)
    if cluster_domain(n,d,c,k,grid,target,stamp):
        return cluster_improve(n,d,c,k,grid,target,stamp,reference,width=16)
    return reference

def million_beam(n,d,c,k,grid,target,stamp,reference,width=12,branch=6,future_weight=4,enhance=False):
    if cluster_domain(n,d,c,k,grid,target,stamp):return reference
    return _cluster_original_million_beam(n,d,c,k,grid,target,stamp,reference,width,branch,future_weight,enhance)
