"""Join independently searched physical and wildcard frontiers by exact matches."""
import heapq
import random


def construct(m,n,d,c,k,grid,target,stamp,width=24,branch=6,strength=0,seed=0,mode=4):
    if n<6 or k<4:return []
    nn=n*n;dd=d*d
    indices,_,ops,_,_=m.build(n,d,target);actions=list(zip(indices,ops))
    initial=grid+stamp;upper=m.color_bound(initial,target)
    cuts=sorted({max(1,min(k-1,int(k*x))) for x in (.25,.5,.75)})
    backcuts={k-x for x in cuts}
    f0=m.ClusterState(n,d,c,grid[:],target,stamp[:])
    fb=[(f0,[])];forward={}
    rng=random.Random(sum((i+37)*v for i,v in enumerate(initial))+k*991+seed)
    for depth in range(max(cuts)):
        candidates=[];seen=set()
        for state,path in fb:
            for aid,gain in m.million_choices(state,rng,branch):
                if path and aid==path[-1]:continue
                child=m.clone_cluster_state(state);child.apply(aid)
                key=bytes(child.grid+child.stamp)
                if key in seen:continue
                seen.add(key)
                candidates.append((child.matches+.5*max(0,child.best()[0]),rng.random(),child,path+[aid]))
        candidates.sort(key=lambda row:row[:2],reverse=True)
        fb=[row[2:]for row in candidates[:width]]
        if depth+1 in cuts:forward[depth+1]=fb[:]
        if not fb:break
    engine=m.FastBack(n,d,grid,target,stamp,indices)
    base=sum(a==b for a,b in zip(grid,target));bb=[(engine.first,[],base)];backward={}
    for depth in range(max(backcuts)):
        candidates=[];seen=set()
        for state,path,score in bb:
            for aid,gain in engine.choices(state,rng,branch):
                if path and aid==path[-1]:continue
                child=engine.apply(state,aid);key=bytes(child[0]+child[1])
                if key in seen:continue
                seen.add(key);value=score+gain
                candidates.append((value+.375*max(0,engine.best(child)),rng.random(),child,path+[aid],value))
        candidates.sort(key=lambda row:row[:2],reverse=True)
        bb=[row[2:]for row in candidates[:width]]
        if depth+1 in backcuts:backward[depth+1]=bb[:]
        if not bb:break
    tables=[bytes(int(v==color)for v in range(256))for color in range(c)]
    def pack(board):
        data=bytes(board)
        return [int.from_bytes(data.translate(table),'little')for table in tables]
    rotations=[]
    for r in range(4):
        rotations.append([p*d+q for u in range(d)for v in range(d)for p,q in [((u,v),(v,d-1-u),(d-1-u,d-1-v),(d-1-v,u))[r]]])
    choices=[]
    for cut in cuts:
        left=[(pack(state.grid),state.stamp,path)for state,path in forward.get(cut,[])]
        right=[(pack(state[0]),state[1],path)for state,path,score in backward.get(k-cut,[])]
        for a,sa,pa in left:
            for b,sb,pb in right:
                boardscore=sum((x&y).bit_count()for x,y in zip(a,b))
                stampvalues=[sum(sa[j]==sb[p]for j,p in enumerate(rot))for rot in rotations]
                r=max(range(4),key=stampvalues.__getitem__)
                value=boardscore+stampvalues[r]
                choices.append((value,rng.random(),pa,pb,r))
    choices.sort(key=lambda row:row[:2],reverse=True)
    best=[];bestscore=base;used=set()
    for value,_,pa,pb,r in choices:
        candidate=pa+[(aid//4)*4+(aid+r)%4 for aid in reversed(pb)]
        key=tuple(candidate)
        if key in used:continue
        used.add(key)
        # Independent scalar resimulation validates stamp-frame alignment.
        state=initial[:]
        for aid in candidate:m._st(state,nn,indices[aid])
        assert sum(a==b for a,b in zip(state,target))==value
        candidate=m.refine(n,d,k,initial,target,actions,candidate,passes=6)
        candidate=m.pair_sweep(n,d,k,initial,target,actions,candidate,passes=2,width=24)
        state=initial[:]
        for aid in candidate:m._st(state,nn,indices[aid])
        value=sum(a==b for a,b in zip(state,target))
        if value>bestscore:best,bestscore=candidate,value
        if bestscore==upper or len(used)>=mode:break
    return [ops[aid]for aid in best]
