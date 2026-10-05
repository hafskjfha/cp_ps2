_MILLION_PATTERNS={}
def million_patterns(n,d):
    key=(n,d)
    if key in _MILLION_PATTERNS:return _MILLION_PATTERNS[key]
    patterns=[];seen=set();nn=n*n;dd=d*d
    offsets=[[(u,v),(v,d-1-u),(d-1-u,d-1-v),(d-1-v,u)]for u in range(d)for v in range(d)]
    for dx in range(d):
        for dy in range(1 if dx==0 else 1-d,d):
            for r in range(4):
                left=[xy[r]for xy in offsets]
                for s in range(4):
                    right=[(dx+xy[s][0],dy+xy[s][1])for xy in offsets]
                    cells=set(left+right)
                    initial={p:p for p in cells};initial.update({j:j for j in range(dd)})
                    for backward in range(2):
                        a,b=(right,left)if backward else(left,right)
                        state=initial.copy()
                        for patch in(a,b)*3:
                            for j,p in enumerate(patch):state[j],state[p]=state[p],state[j]
                        def node(p):return (1,p)if isinstance(p,int)else(0,p[0]*n+p[1])
                        pairs=tuple(sorted((node(p),node(q))for p,q in state.items()if p!=q))
                        if len(pairs)>8 or not pairs or pairs in seen:continue
                        seen.add(pairs)
                        local=tuple(p for ((kind,p),_)in pairs if kind==0)
                        remote=tuple(p for ((kind,p),_)in pairs if kind==1)
                        if not local or not remote:continue
                        patterns.append((dx,dy,r,s,backward,pairs,local,remote))
    _MILLION_PATTERNS[key]=patterns
    return patterns

def million_conjugate_tail(n,d,grid,target,stamp,k,rounds=12,cap=0):
    if k<8 or n<=d:return []
    nn=n*n;side=n-d+1
    indices,_,ops,_,_=build(n,d,target)
    evaluator=RefineState(n,d,grid+stamp,target,list(zip(indices,ops)),[])
    patterns=million_patterns(n,d)
    allbits=evaluator.all_bits
    initial=grid+stamp
    answer=[]
    for turn in range(min(rounds,k//8)):
        values,goals=evaluator.values,evaluator.goals
        board=evaluator.grid
        old=[]
        for j in range(d*d):
            mask=0
            for c in range(6):mask|=values[j][c]&goals[j][c]
            old.append(mask)
        cross={}
        bestgain=0;best=None;count=0
        for dx,dy,r,s,back,pairs,local,remote in patterns:
            for x in range(side-dx):
                for y in range(max(0,-dy),min(side,side-dy)):
                    base=x*n+y
                    loss=sum(board[base+p]==target[base+p]for p in local)
                    if len(local)-loss+len(remote)<=bestgain:continue
                    anchors=allbits
                    for p in local:anchors&=~evaluator.cover_bits[base+p]
                    if not anchors:continue
                    constant=-loss-len(remote)
                    masks=[]
                    for (pk,p),(qk,q)in pairs:
                        if not pk:
                            if not qk:constant+=board[base+q]==target[base+p]
                            else:masks.append(values[q][target[base+p]])
                        elif not qk:masks.append(goals[p][board[base+q]])
                        else:
                            key=p,q
                            mask=cross.get(key)
                            if mask is None:
                                mask=0
                                for c in range(6):mask|=goals[p][c]&values[q][c]
                                cross[key]=mask
                            masks.append(mask)
                    masks.extend(allbits^old[j]for j in remote)
                    if len(masks)+constant<=bestgain:continue
                    planes=[0]*5
                    for carry in masks:
                        carry&=anchors;level=0
                        while carry:
                            before=planes[level];planes[level]=before^carry;carry&=before;level+=1
                    candidates=anchors;value=0
                    for level in range(4,-1,-1):
                        hits=candidates&planes[level]
                        if hits:candidates=hits;value|=1<<level
                    gain=value+constant
                    if gain>bestgain:
                        aid=(candidates&-candidates).bit_length()-1
                        left=(x*side+y)*4+r;right=((x+dx)*side+y+dy)*4+s
                        bestgain=gain;best=[aid]+([right,left]if back else[left,right])*3+[aid]
                    count+=1
                    if cap and count>=cap:break
                if cap and count>=cap:break
            if cap and count>=cap:break
        if best is None:break
        before=sum(a==b for a,b in zip(evaluator.grid,target))
        for aid in best:evaluator.apply(aid)
        after=sum(a==b for a,b in zip(evaluator.grid,target))
        assert after-before==bestgain,(n,d,bestgain,after-before)
        answer.extend(ops[aid]for aid in best)
    return answer

def million_conjugate(n,d,c,k,grid,target,stamp,reference,cuts=(1,)):
    nn=n*n;side=n-d+1
    indices,_,ops,_,_=build(n,d,target)
    state=grid+stamp;snapshots=[state[:]]
    for x,y,r in reference:
        _st(state,nn,indices[(x*side+y)*4+r]);snapshots.append(state[:])
    best=reference;score=sum(a==b for a,b in zip(state,target))
    upper=color_bound(grid+stamp,target)
    if score==upper:return best
    for fraction in cuts:
        cut=int(fraction*len(reference))
        if k-cut<8:continue
        state=snapshots[cut]
        tail=million_conjugate_tail(n,d,state[:nn],target,state[nn:],k-cut)
        state=state[:]
        for x,y,r in tail:_st(state,nn,indices[(x*side+y)*4+r])
        value=sum(a==b for a,b in zip(state,target))
        if value>score:score=value;best=reference[:cut]+tail
        if value==upper:break
    return best
