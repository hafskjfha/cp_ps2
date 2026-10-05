"""Six-step overlap routing: cancel the unaffected three-cycles of two stamps."""


def route_patterns_extended(n,d,repeats=(3,)):
    patterns=[]
    offsets=[[(u,v),(v,d-1-u),(d-1-u,d-1-v),(d-1-v,u)]
             for u in range(d) for v in range(d)]
    for dx in range(d):
        for dy in range(0 if dx==0 else 1-d,d):
            for r in range(4):
                left=[xy[r] for xy in offsets]
                for s in range(4):
                    right=[(dx+xy[s][0],dy+xy[s][1]) for xy in offsets]
                    powers=(1,) if dx==dy==0 else repeats
                    if not powers:continue
                    cells=set(left+right)
                    initial={p:p for p in cells}
                    initial.update({j:j for j in range(d*d)})
                    for backward in range(2):
                        a,b=(right,left) if backward else (left,right)
                        state=initial.copy()
                        for count in range(1,max(powers)+1):
                            for patch in (a,b):
                                for j,p in enumerate(patch):
                                    state[j],state[p]=state[p],state[j]
                            if count not in powers:continue
                            mapping=[]
                            for p in sorted(cells):
                                q=state[p]
                                if q==p:continue
                                src=n*n+q if isinstance(q,int) else q[0]*n+q[1]
                                mapping.append((p[0]*n+p[1],src,isinstance(q,int)))
                            if mapping:
                                patterns.append((dx,dy,r,s,backward,count,mapping))
    return patterns


def route_tail_extended(n,d,grid,target,stamp,k,repeats=(3,),rounds=3):
    if k<2:return []
    patterns=route_patterns_extended(n,d,tuple(x for x in repeats if 2*x<=k))
    width=n-d+1
    state=grid+stamp
    answer=[]
    for _ in range(rounds):
        missing={p for p in range(n*n) if state[p]!=target[p]}
        if not missing:break
        best_gain=0
        best=None
        for dx,dy,r,s,backward,count,mapping in patterns:
            if len(answer)+2*count>k:continue
            if len(missing)*len(mapping)<width*width:
                bases=sorted({p-offset for p in missing for offset,_,_ in mapping})
            else:
                bases=(x*n+y for x in range(width-dx)
                       for y in range(max(0,-dy),min(width,width-dy)))
            for base in bases:
                x,y=divmod(base,n)
                if not (0<=x<width-dx and max(0,-dy)<=y<min(width,width-dy)):continue
                gain=sum(base+p in missing for p,_,_ in mapping)
                if gain<=best_gain:continue
                for p,q,buffer in mapping:
                    pos=base+p
                    if state[q if buffer else base+q]!=target[pos]:
                        gain-=1
                        if gain<=best_gain:break
                if gain>best_gain:
                    best_gain=gain
                    left,right=(x,y,r),(x+dx,y+dy,s)
                    best=([right,left] if backward else [left,right])*count
        if best is None:break
        answer.extend(best)
        for x,y,r in best:
            for j,offset in enumerate([((u,v),(v,d-1-u),(d-1-u,d-1-v),(d-1-v,u))[r]
                                      for u in range(d) for v in range(d)]):
                p=(x+offset[0])*n+y+offset[1]
                state[n*n+j],state[p]=state[p],state[n*n+j]
    return answer
