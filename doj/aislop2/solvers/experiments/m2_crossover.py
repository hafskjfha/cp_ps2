"""Recombine independently constructed paths, then repair exact suffix goals."""


def improve(m,n,d,c,k,grid,target,stamp,reference,alternatives,tries=8):
    nn=n*n;side=n-d+1;initial=grid+stamp
    indices,_,ops,_,_=m.build(n,d,target);actions=list(zip(indices,ops))
    def encode(path):return [(x*side+y)*4+r for x,y,r in path]
    def score(path):
        state=initial[:]
        for aid in path:m._st(state,nn,indices[aid])
        return sum(a==b for a,b in zip(state,target))
    best=encode(reference);bestscore=score(best);upper=m.color_bound(initial,target)
    if bestscore==upper:return reference
    proposals=[];seen={tuple(best)}
    for other in alternatives:
        other=encode(other)
        if not other or tuple(other) in seen:continue
        seen.add(tuple(other))
        for a,b in ((best,other),(other,best)):
            for frac in (.15,.3,.45,.6,.75,.9):
                cut=int(min(len(a),len(b))*frac)
                cand=a[:cut]+b[cut:]
                if len(cand)>k:cand=cand[:k]
                key=tuple(cand)
                if key not in seen:
                    seen.add(key);proposals.append((score(cand),cand))
    proposals.sort(key=lambda x:x[0],reverse=True)
    for i,(_,candidate) in enumerate(proposals[:tries]):
        candidate=m.refine(n,d,k,initial,target,actions,candidate,passes=5,seed_offset=19171*(i+1))
        candidate=m.pair_sweep(n,d,k,initial,target,actions,candidate,passes=1,width=12)
        value=score(candidate)
        if value>bestscore:best,bestscore=candidate,value
        if value==upper:break
    return [ops[aid] for aid in best]
