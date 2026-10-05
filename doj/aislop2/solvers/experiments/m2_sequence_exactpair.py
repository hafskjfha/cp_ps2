"""Complete two-operation coordinate optimization on bounded action spaces."""
import random


def exactpair_refine(n,d,c,k,initial,target,indices,sequence,module,
                    rounds=2,blocks=(1,2,3),passes=1,reverse=True):
    if n>14 or k<5:return sequence
    nn=n*n;side=n-d+1
    upper=sum(min(initial.count(v),target.count(v)) for v in range(c))
    final=initial[:]
    for aid in sequence:module['_st'](final,nn,indices[aid])
    score=sum(a==b for a,b in zip(final,target))
    if score==upper:return sequence
    actions=list(zip(indices,[(a//4//side,a//4%side,a%4) for a in range(len(indices))]))
    rng=random.Random(sum((i+313)*v for i,v in enumerate(initial))+k*6311)
    order=list(range(len(indices)));rng.shuffle(order)
    path=list(sequence)
    for trial in range(rounds):
        path=path+[-1]*min(4,k-len(path))
        state=module['RefineState'](n,d,final,target,actions,order)
        i=len(path)-1
        if trial%2 and i>=0:
            old=path[i]
            if old>=0:state.apply(old)
            new,gain=state.best();path[i]=new
            if new>=0:state.apply(new,wishes=True)
            i-=1
        while i>=1:
            left,right=path[i-1:i+1]
            if right>=0:state.apply(right)
            if left>=0:state.apply(left)
            pair=module['optimize_pair'](state,left,right,[(a,0) for a in [-1]+order])
            path[i-1:i+1]=pair
            for aid in reversed(pair):
                if aid>=0:state.apply(aid,wishes=True)
            i-=2
        if i==0:
            old=path[0]
            if old>=0:state.apply(old)
            path[0],_=state.best()
        path=[a for a in path if a>=0]
        final=initial[:]
        for aid in path:module['_st'](final,nn,indices[aid])
        score2=sum(a==b for a,b in zip(final,target))
        assert score2>=score
        score=score2
        if score==upper:break
    if passes:path=module['refine'](n,d,k,initial,target,actions,path,passes=passes,seed_offset=981139)
    return path
