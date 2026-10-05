"""Research helper: bit-parallel heat-bath sampling of sequence coordinates."""
import math,random


def gibbs_refine(n,d,c,k,initial,target,indices,sequence,module,
                 pairs=64,alternatives=12,passes=1,seed_offset=0):
    nn,dd=n*n,d*d
    upper=sum(min(initial.count(v),target.count(v)) for v in range(c))
    q=len(indices);side=n-d+1
    actions=list(zip(indices,[(a//4//side,a//4%side,a%4) for a in range(q)]))
    rng=random.Random(sum((i+127)*v for i,v in enumerate(initial))+k*8971+seed_offset)
    best=list(sequence)
    final=initial[:]
    for a in sequence:module['_st'](final,nn,indices[a])
    score=bestscore=sum(a==b for a,b in zip(final,target))
    if score==upper or k<3:return best
    path=list(sequence)+[-1]*(k-len(sequence))
    order=list(range(q))
    period=16
    maximum=alternatives/20

    def sample(state,temp):
        planes=[0]*5
        for jj in range(dd):
            for carry in (state.values[jj][state.wstamp[jj]],state.goals[jj][state.stamp[jj]]):
                plane=0
                while carry:
                    old=planes[plane];planes[plane]=old^carry;carry&=old;plane+=1
        carry=0
        for plane in range(5):
            a,b=planes[plane],state.old_planes[plane]
            diff=a^b;planes[plane]=diff^carry;carry=(a&b)|(diff&carry)
        remaining=state.all_bits;groups=[];maximum_value=None
        offset=dd+sum(a==b for a,b in zip(state.stamp,state.wstamp))
        total=0.0
        while remaining:
            candidates=remaining;value=0
            for i in range(4,-1,-1):
                hits=candidates&planes[i]
                if hits:candidates=hits;value|=1<<i
            remaining^=candidates
            if maximum_value is None:maximum_value=max(value,offset)
            if value<maximum_value-3:break
            weight=math.exp((value-maximum_value)/temp)*candidates.bit_count()
            total+=weight
            groups.append((total,candidates,value-offset))
        noop=math.exp((offset-maximum_value)/temp)
        sample_value=rng.random()*(total+noop)
        if sample_value>=total:return -1,0
        for total,candidates,gain in groups:
            if sample_value<total:
                off=rng.randrange(q);after=candidates>>off
                aid=(after&-after).bit_length()-1+off if after else (candidates&-candidates).bit_length()-1
                return aid,gain
        raise AssertionError

    for iteration in range(pairs):
        if iteration%period==0:
            path=list(best)+[-1]*(k-len(best))
            final=initial[:]
            for a in path:
                if a>=0:module['_st'](final,nn,indices[a])
            score=bestscore
        temp=maximum*(1-(iteration%period)/(period-1))**2+0.025
        state=module['RefineState'](n,d,final,target,actions,order)
        for i in range(len(path)-1,-1,-1):
            old=path[i]
            if old>=0:
                score+=module['_og'](state,old)
                state.apply(old)
            chosen,gain=sample(state,temp)
            path[i]=chosen
            score+=gain
            if chosen>=0:state.apply(chosen,wishes=True)
            if score>bestscore:
                bestscore=score;best=[a for a in path if a>=0]
                if bestscore==upper:return best
        final=initial[:]
        for a in path:
            if a>=0:module['_st'](final,nn,indices[a])
        actual=sum(a==b for a,b in zip(final,target))
        assert actual==score,(actual,score)
    if passes:best=module['refine'](n,d,k,initial,target,actions,best,passes=passes,seed_offset=902177+seed_offset)
    return best
