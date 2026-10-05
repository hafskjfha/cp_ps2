"""All-action compact beam with exact packed one-step continuation scores."""
import heapq
import random


def construct(m,n,d,c,k,grid,target,stamp,width=512,future_weight=3,refine=True):
    indices,_,ops,_,_=m.build(n,d,target)
    initial=m.PackedClusterState(n,d,c,grid[:],target,stamp[:])
    upper=m.color_bound(grid+stamp,target)
    beam=[(initial,[])];best=[];bestscore=initial.matches
    rng=random.Random(sum((i+91)*v for i,v in enumerate(grid+stamp))+k*941)
    norms={}
    def key(state):
        raw=bytes(state.stamp);norm=norms.get(raw)
        if norm is None:
            s=state.stamp
            quarter=bytes((s[2],s[5],s[8],s[1],s[4],s[7],s[0],s[3],s[6]))if d==3 else bytes((s[1],s[3],s[0],s[2]))
            norm=min(raw,raw[::-1],quarter,quarter[::-1])
            if len(norms)>=16384:norms.clear()
            norms[raw]=norm
        return bytes(state.grid)+norm
    visited={key(initial)};expansions=0
    for depth in range(k):
        candidates=[];seen=set()
        for state,path in beam:
            for aid in range(len(indices)):
                if path and aid==path[-1]:continue
                child=m.clone_packed_cluster_state(state);child.apply(aid);expansions+=1
                signature=key(child)
                if signature in visited or signature in seen:continue
                seen.add(signature);p2=path+[aid]
                if child.matches>bestscore:best,bestscore=p2,child.matches
                if bestscore==upper:return [ops[x]for x in best],expansions
                future=max(0,child.best()[0])if depth+1<k else 0
                priority=child.matches*8+future_weight*future
                candidates.append((priority,rng.getrandbits(32),child,p2,signature))
        if not candidates:break
        chosen=heapq.nlargest(width,candidates,key=lambda row:row[:2])
        beam=[(child,path)for _,_,child,path,_ in chosen]
        visited.update(signature for _,_,_,_,signature in chosen)
    path=best
    if refine:
        actions=list(zip(indices,ops))
        path=m.refine(n,d,k,grid+stamp,target,actions,path,passes=6)
        path=m.pair_sweep(n,d,k,grid+stamp,target,actions,path,passes=2,width=24)
    return [ops[x]for x in path],expansions
