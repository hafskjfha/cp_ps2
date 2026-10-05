"""Global structured-target two-step construction using pattern groups."""
import heapq
import random


def construct(m,n,d,c,k,grid,target,stamp,mode=1,width=24,branch=8,strength=.15,seed=0):
    if k<3 or n==d:return []
    initial=m.State(n,d,c,grid[:],target,stamp[:])
    groups={}
    for aid,mask in enumerate(initial.masks):groups.setdefault(mask,[]).append(aid>>2)
    if len(groups)>80:return []
    groups=[(mask,set(regions)) for mask,regions in groups.items()]
    groups.sort(key=lambda x:len(x[1]),reverse=True)
    actions=initial.actions;indices=[a[0] for a in actions]
    all_ids=range(len(actions))
    rng=random.Random(61739+seed)
    order=list(all_ids);rng.shuffle(order)
    best=[];best_score=initial.matches;upper=initial.limit
    for restart in range(max(1,mode)):
        state=m.clone_state(initial)
        path=[];scores=[state.matches];local_best=[];local_score=state.matches
        outgoing=[sum(1<<(c*j+state.grid[p]) for j,p in enumerate(index)) for index in indices]
        seen=set()
        while len(path)<k and local_score<upper:
            mask=state.stampmask;counts=state.counts
            mins=[(g,min(counts[p] for p in rs)) for g,rs in groups]
            potentials={};candidates=[]
            for aid in order:
                code=outgoing[aid]
                future=potentials.get(code)
                if future is None:
                    future=max((code&g).bit_count()-old for g,old in mins)
                    potentials[code]=future
                gain=(mask&state.masks[aid]).bit_count()-counts[aid>>2]
                value=gain+(future if len(path)+1<k else 0)
                candidates.append((value,rng.random(),aid))
            candidates=heapq.nlargest(width,candidates)
            choices=[]
            for _,tie,aid in candidates:
                child=m.clone_state(state);child.apply(aid)
                gain=child.matches-state.matches
                if len(path)+1<k:
                    second_gain,second=child.best()
                    child.apply(second)
                    pair=(aid,second)
                    value=gain+second_gain
                else:pair=(aid,);value=gain
                signature=bytes(child.grid+child.stamp)
                if signature in seen:continue
                future=max(0,child.best()[0]) if len(path)+len(pair)<k else 0
                choices.append((value+strength*future,tie,pair,child,signature))
            if not choices:break
            _,_,pair,state,signature=max(choices,key=lambda x:(x[0],x[1]))
            if state.matches<scores[-1]-1:break
            seen.add(signature);path.extend(pair);scores.append(state.matches)
            changed=set(p for aid in pair for p in indices[aid])
            regions=set(r for p in changed for r in state.cover[p])
            for region in regions:
                for aid in range(region*4,region*4+4):
                    outgoing[aid]=sum(1<<(c*j+state.grid[p]) for j,p in enumerate(indices[aid]))
            if state.matches>local_score:local_best,local_score=path[:],state.matches
        local_best=m.refine(n,d,k,grid+stamp,target,actions,local_best,passes=6)
        local_best=m.pair_sweep(n,d,k,grid+stamp,target,actions,local_best,passes=2,width=24)
        result=grid+stamp
        for aid in local_best:m._st(result,n*n,indices[aid])
        value=sum(a==b for a,b in zip(result,target))
        if value>best_score:best,best_score=local_best,value
        if value==upper:break
    return best
