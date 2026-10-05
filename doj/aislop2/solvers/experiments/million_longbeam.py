"""Long-horizon, bit-parallel beam candidate construction."""
import random

def choices(state,rng,branch=6):
    planes=[0]*5
    for j,color in enumerate(state.stamp):
        carry=state.target_bits[j][color]
        plane=0
        while carry:
            old=planes[plane];planes[plane]=old^carry;carry&=old;plane+=1
    carry=0
    for plane in range(4):
        a,b=planes[plane],state.old_planes[plane]
        different=a^b;planes[plane]=different^carry;carry=a&b|different&carry
    planes[4]=carry
    remaining=state.all_actions
    out=[]
    count=len(state.actions)
    seen={}
    while len(out)<branch and remaining:
        candidates,value=remaining,0
        for plane in range(4,-1,-1):
            hits=candidates&planes[plane]
            if hits:candidates=hits;value|=1<<plane
        remaining^=candidates
        take=min(branch-len(out),4)
        while candidates and take:
            offset=rng.randrange(count)
            after=candidates>>offset
            rank=(after&-after).bit_length()-1+offset if after else (candidates&-candidates).bit_length()-1
            candidates^=1<<rank
            aid=state.order[rank]
            outgoing=tuple(state.grid[p] for p in state.actions[aid][0])
            if seen.get(outgoing,0)>=2:continue
            seen[outgoing]=seen.get(outgoing,0)+1
            out.append((aid,value-state.size));take-=1
        if out and value-state.size<out[0][1]-1:break
    return out

def improve(m,n,d,c,k,grid,target,stamp,reference,width=12,branch=6,future_weight=4,enhance=False):
    if k<3 or n==d:return reference
    base=sum(a==b for a,b in zip(grid,target))
    upper=m.color_bound(grid+stamp,target)
    indices,_,operations,_,_=m.build(n,d,target)
    actions=list(zip(indices,operations));side=n-d+1;initial=grid+stamp
    def score(path):
        state=initial[:]
        for aid in path:m._st(state,n*n,indices[aid])
        return sum(a==b for a,b in zip(state,target))
    best=[(x*side+y)*4+r for x,y,r in reference];best_score=score(best)
    if best_score==upper:return reference
    state=m.State(n,d,c,grid[:],target,stamp[:])
    rng=random.Random(sum((i+51)*v for i,v in enumerate(grid+stamp))+k*917)
    beam=[(state,[])]
    beam_best,beam_score=[],base
    for depth in range(k):
        candidates=[];seen=set()
        for state,path in beam:
            for aid,gain in choices(state,rng,branch):
                if path and aid==path[-1]:continue
                child=m.clone_state(state);child.apply(aid)
                key=bytes(child.grid+child.stamp)
                if key in seen:continue
                seen.add(key)
                path2=path+[aid]
                if child.matches>beam_score:
                    beam_best,beam_score=path2,child.matches
                if beam_score==upper:
                    return [operations[x] for x in beam_best]
                future=max(0,child.best()[0]) if depth+1<k else 0
                priority=child.matches*8+future_weight*future
                candidates.append((priority,rng.random(),child,path2))
        if not candidates:break
        candidates.sort(key=lambda x:(x[0],x[1]),reverse=True)
        beam=[];stamp_counts={};deferred=[]
        for _,_,state,path in candidates:
            sig=tuple(state.stamp)
            if stamp_counts.get(sig,0)>=max(2,width//4):
                deferred.append((state,path));continue
            stamp_counts[sig]=stamp_counts.get(sig,0)+1
            beam.append((state,path))
            if len(beam)>=width:break
        if len(beam)<width:beam.extend(deferred[:width-len(beam)])
    candidate=m.refine(n,d,k,initial,target,actions,beam_best,passes=6)
    candidate=m.pair_sweep(n,d,k,initial,target,actions,candidate,passes=2,width=24)
    if enhance:
        candidate=m.anneal_walk(n,d,k,initial,target,actions,candidate)
        candidate=m.refine(n,d,k,initial,target,actions,candidate,passes=2)
        candidate=m.triple_refine(n,d,k,initial,target,actions,candidate,passes=2)
        candidate=m.refine(n,d,k,initial,target,actions,candidate,passes=2)
    value=score(candidate)
    if value>best_score:best=candidate
    return [operations[x] for x in best]
