"""Frozen width16 residual-cluster beam; retains the supplied reference floor."""
import random


def improve(m,n,d,c,k,grid,target,stamp,reference,width=16):
    if k<3 or n==d:return reference
    indices,_,ops,_,_=m.build(n,d,target)
    side=n-d+1;initial_grid=grid+stamp
    best=[(x*side+y)*4+r for x,y,r in reference]
    state_grid=initial_grid[:]
    for aid in best:m._st(state_grid,n*n,indices[aid])
    best_score=sum(a==b for a,b in zip(state_grid,target))
    upper=m.color_bound(initial_grid,target)
    if best_score==upper:return reference
    initial=m.State(n,d,c,grid[:],target,stamp[:])
    state_seed=sum((i+51)*v for i,v in enumerate(grid+stamp))+k*917
    rng=random.Random(state_seed)
    edges=[[] for _ in grid]
    for p in range(n*n):
        if p%n:edges[p].append((p-1,p))
        if p//n:edges[p].append((p-n,p))
        if p%n<n-1:edges[p].append((p,p+1))
        if p//n<n-1:edges[p].append((p,p+n))
    action_edges=[set(e for p in positions for e in edges[p]) for positions in initial.regions]
    auxiliary=sum(grid[a]!=target[a] and grid[b]!=target[b]
                  for a in range(n*n) for b in (a+1,a+n)
                  if b<n*n and (b==a+n or a//n==b//n))
    beam=[(initial,[],auxiliary)]
    beam_best=[];beam_score=initial.matches
    for depth in range(k):
        candidates=[];seen=set()
        for state,path,auxiliary in beam:
            for aid,gain in m.million_choices(state,rng,8):
                if path and aid==path[-1]:continue
                child=m.clone_state(state);child.apply(aid)
                key=bytes(child.grid+child.stamp)
                if key in seen:continue
                seen.add(key)
                change=sum((child.grid[a]!=target[a] and child.grid[b]!=target[b])-
                           (state.grid[a]!=target[a] and state.grid[b]!=target[b])
                           for a,b in action_edges[aid>>2])
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
    candidate=m.refine(n,d,k,initial_grid,target,actions,beam_best,passes=6)
    candidate=m.pair_sweep(n,d,k,initial_grid,target,actions,candidate,passes=2,width=24)
    state_grid=initial_grid[:]
    for aid in candidate:m._st(state_grid,n*n,indices[aid])
    value=sum(a==b for a,b in zip(state_grid,target))
    return [ops[aid] for aid in candidate] if value>best_score else reference
