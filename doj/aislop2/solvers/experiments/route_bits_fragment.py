"""Exact parallel scoring of sparse routing permutations at every legal anchor."""


def route_tail_bits(n,d,grid,target,stamp,k,repeats=(3,),rounds=3):
    if k<6:return []
    active=tuple(x for x in repeats if 2*x<=k)
    if not active:return []
    patterns=route_patterns(n,d,active)
    width=n-d+1
    state=grid+stamp
    wanted=[0]*6
    for p,color in enumerate(target):wanted[color]|=1<<p
    def shift(bits,offset):
        return bits>>offset if offset>=0 else bits<<-offset
    offsets={p for *_,mapping in patterns for p,_,_ in mapping}
    sources={q for *_,mapping in patterns for _,q,buffer in mapping if not buffer}
    wishes={p:tuple(shift(bits,p) for bits in wanted) for p in offsets}
    legal={}
    for dx,dy,*_ in patterns:
        key=(dx,dy)
        if key in legal:continue
        left,right=max(0,-dy),min(width,width-dy)
        if left>=right or dx>=width:
            legal[key]=0
        else:
            row=((1<<(right-left))-1)<<left
            legal[key]=sum(row<<(x*n) for x in range(width-dx))
    rotations=[[(p*n+q) for u in range(d) for v in range(d)
                for p,q in [((u,v),(v,d-1-u),(d-1-u,d-1-v),(d-1-v,u))[r]]]
               for r in range(4)]
    answer=[]
    for _ in range(rounds):
        have=[0]*6
        agreement=0
        for p,color in enumerate(state[:n*n]):
            have[color]|=1<<p
            if color==target[p]:agreement|=1<<p
        if agreement==(1<<(n*n))-1:break
        values={q:tuple(shift(bits,q) for bits in have) for q in sources}
        old={p:shift(agreement,p) for p in offsets}
        matches={}
        best_gain=0
        best=None
        for dx,dy,r,s,backward,count,mapping in patterns:
            if len(answer)+2*count>k:continue
            anchors=legal[(dx,dy)]
            if not anchors:continue
            planes=[0]*(2*len(mapping)+1).bit_length()
            for p,q,buffer in mapping:
                if buffer:
                    new=wishes[p][state[q]]
                else:
                    key=(p,q)
                    new=matches.get(key)
                    if new is None:
                        new=0
                        for want,value in zip(wishes[p],values[q]):new|=want&value
                        matches[key]=new
                for carry in (new&anchors,anchors&~old[p]):
                    level=0
                    while carry:
                        before=planes[level]
                        planes[level]=before^carry
                        carry&=before
                        level+=1
            candidates,value=anchors,0
            for level in range(len(planes)-1,-1,-1):
                hits=candidates&planes[level]
                if hits:
                    candidates=hits
                    value|=1<<level
            gain=value-len(mapping)
            if gain>best_gain:
                best_gain=gain
                base=(candidates&-candidates).bit_length()-1
                x,y=divmod(base,n)
                left,right=(x,y,r),(x+dx,y+dy,s)
                best=([right,left] if backward else [left,right])*count
        if best is None:break
        answer.extend(best)
        for x,y,r in best:
            base=x*n+y
            for j,offset in enumerate(rotations[r]):
                p=base+offset
                state[n*n+j],state[p]=state[p],state[n*n+j]
    return answer
