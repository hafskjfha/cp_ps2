"""Structured zero/weighted objectives with exact incumbent retention."""
import random


def objective_refine(n,d,c,k,initial,target,indices,sequence,module,
                     rounds=32,blocks=(0,1,2,3),passes=3,reverse=True):
    if k<8 or n<=d:return sequence
    # Compact D3 construction is being optimized independently in this campaign.
    if d==3 and n<=16 and 20<=k<=80:return sequence
    nn=n*n;side=n-d+1
    actions=list(zip(indices,[(a//4//side,a//4%side,a%4) for a in range(len(indices))]))
    upper=sum(min(initial.count(v),target.count(v)) for v in range(c))
    def evaluate(path):
        row=initial[:]
        for aid in path:
            for j,p in enumerate(indices[aid]):row[p],row[nn+j]=row[nn+j],row[p]
        return sum(a==b for a,b in zip(row,target)),row
    best=list(sequence);score,final=evaluate(best)
    if score==upper:return best
    current=best[:]
    rng=random.Random(sum((i+281)*v for i,v in enumerate(initial))+k*6311)
    for trial in range(rounds):
        mode=blocks[trial%len(blocks)]
        rate=(.1,.25,.4,.6)[trial//len(blocks)%4]
        if mode==0:
            weights=[1+(rng.random()<rate) for _ in range(nn)]
        elif mode==1:
            weights=[0 if rng.random()<rate else 1 for _ in range(nn)]
        elif mode==2:
            weights=[2 if final[p]!=target[p] else int(rng.random()>=rate) for p in range(nn)]
        elif mode==3:
            wrong=[p for p in range(nn) if final[p]!=target[p]]
            center=rng.choice(wrong) if wrong else rng.randrange(nn)
            x,y=divmod(center,n);radius=rng.randrange(d,max(d+1,n//2+1))
            weights=[2 if abs(p//n-x)+abs(p%n-y)<=radius else int(rng.random()>=rate) for p in range(nn)]
        elif mode==4:
            color=rng.randrange(c)
            weights=[2 if value==color else int(rng.random()>=rate) for value in target]
        else:
            horizontal=bool(rng.randrange(2));offset=rng.randrange(n);span=rng.randrange(d,max(d+1,n//2+1))
            weights=[2 if ((p//n if horizontal else p%n)-offset)%n<span else int(rng.random()>=rate) for p in range(nn)]
        candidate=module['weighted_refine'](n,d,k,initial,target,weights,actions,current,passes=1)
        candidate=module['refine'](n,d,k,initial,target,actions,candidate,passes=passes,seed_offset=719287+trial*14881)
        value,row=evaluate(candidate)
        if value>=score:
            best,score,final=candidate[:],value,row
            if score==upper:break
        current=candidate if value>=score-2 else best[:]
        if trial%8==7:current=best[:]
    return best
