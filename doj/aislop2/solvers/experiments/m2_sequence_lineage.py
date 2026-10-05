"""Masked noncontiguous refinement along residual color transport traces."""
import random


def lineage_refine(n,d,c,k,initial,target,indices,sequence,module,
                   rounds=32,blocks=(4,8,12),passes=2,reverse=True):
    if k<8 or n<=d:return sequence
    if d==3 and n<=16 and 20<=k<=80:return sequence
    nn=n*n;dd=d*d;side=n-d+1
    actions=list(zip(indices,[(a//4//side,a//4%side,a%4) for a in range(len(indices))]))
    upper=sum(min(initial.count(v),target.count(v)) for v in range(c))
    def evaluate(path):
        row=initial[:]
        for aid in path:
            if aid>=0:
                for j,p in enumerate(indices[aid]):row[p],row[nn+j]=row[nn+j],row[p]
        return sum(a==b for a,b in zip(row,target)),row
    best=list(sequence);score,final=evaluate(best)
    if score==upper:return best
    rng=random.Random(sum((i+197)*v for i,v in enumerate(initial))+k*3529)
    for trial in range(rounds):
        wrong=[p for p in range(nn) if final[p]!=target[p]]
        p=rng.choice(wrong)
        partners=[q for q in wrong if final[q]==target[p] and target[q]==final[p]]
        if not partners:partners=[q for q in wrong if final[q]==target[p]]
        if not partners:partners=[nn+j for j in range(dd) if final[nn+j]==target[p]]
        if not partners:continue
        q=rng.choice(partners)
        tracked={p,q};active=[]
        for pos in range(len(best)-1,-1,-1):
            aid=best[pos];changed=False
            for j,a in enumerate(indices[aid]):
                b=nn+j;left=a in tracked;right=b in tracked
                if left or right:changed=True
                if left!=right:
                    if left:tracked.remove(a);tracked.add(b)
                    else:tracked.remove(b);tracked.add(a)
            if changed:active.append(pos)
        count=blocks[trial%len(blocks)]
        if len(active)>count:
            active=active[:count] if trial%2 else rng.sample(active,count)
        active=set(active)
        if not active:continue
        candidate=best+[-1]*min(4,k-len(best))
        active.update(range(len(best),len(candidate)))
        weights=[0]*nn
        weights[p]=2
        if q<nn:weights[q]=2
        if trial%3==1:
            weights=[max(w,int(rng.random()<.10)) for w in weights]
        elif trial%3==2:
            weights=[max(w,int(rng.random()<.35)) for w in weights]
        for sweep in range(2):
            _,end=evaluate(candidate)
            order=list(range(len(actions)));rng.shuffle(order)
            state=module['WeightedRefineState'](n,d,end,target,weights,actions,order)
            for pos in range(len(candidate)-1,-1,-1):
                old=candidate[pos]
                if old>=0:state.apply(old)
                chosen=state.best()[0] if pos in active else old
                candidate[pos]=chosen
                if chosen>=0:state.apply(chosen,wishes=True)
        candidate=[a for a in candidate if a>=0]
        candidate=module['refine'](n,d,k,initial,target,actions,candidate,passes=passes,seed_offset=316927+trial*49891)
        value,row=evaluate(candidate)
        if value>=score:
            best,score,final=candidate[:],value,row
            if score==upper:break
    return best
