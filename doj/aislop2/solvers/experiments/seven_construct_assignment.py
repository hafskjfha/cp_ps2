"""Disjoint-patch assignment construction, for measurement only."""
import random


def assignment(cost):
    n=len(cost)
    u=[0]*(n+1);v=[0]*(n+1);p=[0]*(n+1);way=[0]*(n+1)
    for i in range(1,n+1):
        p[0]=i;j0=0;minv=[10**9]*(n+1);used=[False]*(n+1)
        while True:
            used[j0]=True;i0=p[j0];delta=10**9;j1=0;line=cost[i0-1];ui=u[i0]
            for j in range(1,n+1):
                if not used[j]:
                    cur=line[j-1]-ui-v[j]
                    if cur<minv[j]:minv[j]=cur;way[j]=j0
                    if minv[j]<delta:delta=minv[j];j1=j
            for j in range(n+1):
                if used[j]:u[p[j]]+=delta;v[j]-=delta
                else:minv[j]-=delta
            j0=j1
            if p[j0]==0:break
        while True:
            j1=way[j0];p[j0]=p[j1];j0=j1
            if j0==0:break
    result=[0]*n
    for j in range(1,n+1):result[p[j]-1]=j-1
    return result


def construct(m,n,d,c,k,grid,target,stamp,mode=1,width=24,branch=8,strength=.15,seed=0):
    if k<8 or n==d:return []
    nn=n*n;side=n-d+1;dd=d*d
    indices,_,ops,_,_=m.build(n,d,target)
    actions=list(zip(indices,ops))
    limit=m.color_bound(grid+stamp,target)
    best_score=sum(a==b for a,b in zip(grid,target));best=[]
    rng=random.Random(73819+seed)
    offsets=[(x,y) for x in range(d) for y in range(d)]
    if mode==1:offsets=offsets[:1]
    elif mode==2:rng.shuffle(offsets);offsets=offsets[:3]
    for ox,oy in offsets:
        patches=[(x*side+y)*4 for x in range(ox,side,d) for y in range(oy,side,d)]
        patches.sort(key=lambda aid:sum(grid[p]==target[p] for p in indices[aid]))
        patches=patches[:max(1,int(k*.8))]
        count=len(patches)+1
        raw=[stamp]+[[grid[p] for p in indices[aid]] for aid in patches]
        rotations=[]
        for source in raw:
            arrs=[]
            for r in range(4):
                rotated=[0]*dd
                for u in range(d):
                    for v in range(d):
                        a,b=((u,v),(v,d-1-u),(d-1-u,d-1-v),(d-1-v,u))[r]
                        rotated[a*d+b]=source[u*d+v]
                arrs.append(rotated)
            rotations.append(arrs)
        costs=[];orient=[]
        for i in range(count):
            row=[0];ors=[0]
            for j,aid in enumerate(patches,1):
                wanted=[target[p] for p in indices[aid]]
                scores=[sum(a==b for a,b in zip(candidate,wanted)) for candidate in rotations[i]]
                r=max(range(4),key=lambda r:scores[r]*1000-(r!=0)*3)
                value=scores[r]*1000
                if i!=j:value-=int(strength*1000)
                elif r:value-=int(strength*2000)
                row.append(-value);ors.append(r)
            costs.append(row);orient.append(ors)
        placement=assignment(costs)
        seen={0};sequence=[]
        # The cycle containing the initial stamp.
        source=0;orientation=0
        while placement[source]!=0:
            dest=placement[source];seen.add(dest)
            r=(orient[source][dest]-orientation)%4
            sequence.append(patches[dest-1]+r)
            source=dest;orientation=(-r)%4
        # Every closed block cycle needs a temporary visit to its first block.
        for start in range(1,count):
            if start in seen:continue
            if placement[start]==start and orient[start][start]==0:
                seen.add(start);continue
            sequence.append(patches[start-1])
            source=start;orientation=0
            while True:
                seen.add(source);dest=placement[source]
                r=(orient[source][dest]-orientation)%4
                sequence.append(patches[dest-1]+r)
                if dest==start:break
                source=dest;orientation=(-r)%4
        # Correct construction invariant: each assignment delivers its promised
        # best rotation; validate independently in the probe.
        if len(sequence)>k:sequence=sequence[:k]
        sequence=m.refine(n,d,k,grid+stamp,target,actions,sequence,passes=8)
        sequence=m.pair_sweep(n,d,k,grid+stamp,target,actions,sequence,passes=3,width=24)
        state=grid+stamp
        for aid in sequence:m._st(state,nn,indices[aid])
        score=sum(a==b for a,b in zip(state,target))
        if score>best_score:best,best_score=sequence,score
        if best_score==limit:break
    return best
