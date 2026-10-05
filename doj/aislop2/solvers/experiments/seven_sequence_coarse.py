"""Research helper: multiscale color-equivalence objective continuation."""
import random


def coarse_refine(n,d,c,k,initial,target,indices,sequence,module,
                  pairs=16,alternatives=12,passes=3,seed_offset=0):
    nn=n*n
    upper=sum(min(initial.count(v),target.count(v)) for v in range(c))
    q=len(indices);side=n-d+1
    actions=list(zip(indices,[(a//4//side,a//4%side,a%4) for a in range(q)]))
    rng=random.Random(sum((i+139)*v for i,v in enumerate(initial))+k*11297+seed_offset)

    def evaluate(path):
        final=initial[:]
        for a in path:module['_st'](final,nn,indices[a])
        return sum(a==b for a,b in zip(final,target))

    best=list(sequence);bestscore=evaluate(best)
    if c<3 or bestscore==upper or k<4:return best
    maps=[]
    for a in range(c):
        for b in range(a+1,c):
            mapping=list(range(c));mapping[b]=a
            maps.append(mapping)
    rng.shuffle(maps)
    for i in range(1,1<<(c-1)):
        maps.append([1 if i>>a&1 else 0 for a in range(c)])
    if len(maps)>pairs:maps=maps[:pairs]
    current=list(best)
    for trial,mapping in enumerate(maps):
        mapped_initial=[mapping[v] for v in initial]
        mapped_target=[mapping[v] for v in target]
        candidate=module['refine'](n,d,k,mapped_initial,mapped_target,actions,current,passes=2,seed_offset=trial*91621+seed_offset)
        candidate=module['refine'](n,d,k,initial,target,actions,candidate,passes=passes,seed_offset=trial*120011+seed_offset)
        value=evaluate(candidate)
        if value>bestscore:
            best,bestscore=list(candidate),value
            if value==upper:return best
        current=candidate if value>=bestscore-2 else list(best)
        if trial%4==3:current=list(best)
    return best
