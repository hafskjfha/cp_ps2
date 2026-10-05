"""Exact nonlocal operation relocation followed by sequence descent."""
import random


def improve(m,n,d,c,k,grid,target,stamp,reference,rounds=6,plateau=False):
    nn=n*n;side=n-d+1;initial=grid+stamp
    indices,_,ops,_,_=m.build(n,d,target);actions=list(zip(indices,ops))
    best=[(x*side+y)*4+r for x,y,r in reference]
    def score(path):
        state=initial[:]
        for aid in path:m._st(state,nn,indices[aid])
        return sum(a==b for a,b in zip(state,target))
    bestscore=score(best);upper=m.color_bound(initial,target)
    if bestscore==upper or k<3:return reference
    rng=random.Random(sum((j+793)*v for j,v in enumerate(initial))+k*8101)
    current=best[:]
    for trial in range(rounds):
        front=[initial[:]]
        for aid in current:
            row=front[-1][:];m._st(row,nn,indices[aid]);front.append(row)
        back=[None]*(len(current)+1);back[-1]=target+[6]*(d*d)
        for i in range(len(current)-1,-1,-1):
            row=back[i+1][:];m._st(row,nn,indices[current[i]]);back[i]=row
        value=score(current);chosen=None;ties=0
        order=list(range(len(current)));rng.shuffle(order)
        for i in order:
            aid=current[i];patch=indices[aid]
            state=front[i][:];wish=back[i+1][:]
            base=sum(a==b for a,b in zip(state,wish))
            for direction in (1,-1):
                if direction<0:state=front[i][:];wish=back[i+1][:]
                locations=range(i+2,len(current)+1) if direction>0 else range(i-1,-1,-1)
                for j in locations:
                    step=current[j-1] if direction>0 else current[j]
                    m._st(state,nn,indices[step]);m._st(wish,nn,indices[step])
                    gain=sum((state[nn+t]==wish[p])+(state[p]==wish[nn+t])-(state[p]==wish[p])-(state[nn+t]==wish[nn+t]) for t,p in enumerate(patch))
                    result=base+gain
                    if result>value or plateau and result==value:
                        if result>value:value=result;ties=0
                        ties+=1
                        if rng.randrange(ties)==0:chosen=(i,j)
        if chosen is None:break
        i,j=chosen;aid=current[i]
        candidate=current[:i]+current[i+1:j]+[aid]+current[j:] if j>i else current[:j]+[aid]+current[j:i]+current[i+1:]
        assert score(candidate)==value,(score(candidate),value,i,j)
        candidate=m.refine(n,d,k,initial,target,actions,candidate,passes=3,seed_offset=170839+trial*8161)
        candidate_score=score(candidate)
        if candidate_score>bestscore:bestscore,best=candidate_score,candidate[:]
        if bestscore==upper:break
        current=candidate if candidate_score>=bestscore else best[:]
    return [ops[aid]for aid in best]
