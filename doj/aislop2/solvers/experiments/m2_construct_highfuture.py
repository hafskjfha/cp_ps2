"""Plane-only forward beam with optional stamp-orbit state deduplication."""
import random
import math


def pooled_choices(m,state,rng,branch,pool=24):
    planes=[0]*5
    for j,color in enumerate(state.stamp):
        carry=state.target_bits[j][color];p=0
        while carry:
            old=planes[p];planes[p]=old^carry;carry&=old;p+=1
    carry=0
    for p in range(4):
        a,b=planes[p],state.old_planes[p];different=a^b
        planes[p]=different^carry;carry=a&b|different&carry
    planes[4]=carry
    remaining=state.all_actions;count=len(state.actions);seen=set();poolrows=[];top=None
    shadow=object.__new__(m.ClusterState);shadow.__dict__=state.__dict__.copy()
    while remaining and len(poolrows)<pool:
        candidates,value=remaining,0
        for p in range(4,-1,-1):
            hits=candidates&planes[p]
            if hits:candidates=hits;value|=1<<p
        if top is None:top=value
        if value<top-1:break
        remaining^=candidates;take=min(pool-len(poolrows),pool//2)
        while candidates and take:
            offset=rng.randrange(count);after=candidates>>offset
            rank=(after&-after).bit_length()-1+offset if after else (candidates&-candidates).bit_length()-1
            candidates^=1<<rank;aid=state.order[rank]
            outgoing=bytes(state.grid[p]for p in state.actions[aid][0])
            if outgoing in seen:continue
            seen.add(outgoing);shadow.stamp=outgoing
            future=max(0,shadow.best()[0]);gain=value-state.size
            poolrows.append((gain+.5*future,rng.random(),aid,gain));take-=1
    poolrows.sort(reverse=True)
    return [(aid,gain)for _,_,aid,gain in poolrows[:branch]]


def construct(m,n,d,c,k,grid,target,stamp,width=48,branch=6,strength=0,seed=0,mode=0,refine=True):
    nn=n*n
    indices,_,ops,_,_=m.build(n,d,target)
    initial=m.ClusterState(n,d,c,grid[:],target,stamp[:])
    upper=m.color_bound(grid+stamp,target)
    rotations=[]
    for r in range(4):
        rotations.append([((u,v),(v,d-1-u),(d-1-u,d-1-v),(d-1-v,u))[r][0]*d+
                          ((u,v),(v,d-1-u),(d-1-u,d-1-v),(d-1-v,u))[r][1]
                          for u in range(d)for v in range(d)])
    beam=[(initial,[])];best=[];bestscore=initial.matches;finalists=[]
    rng=random.Random(sum((i+51)*v for i,v in enumerate(grid+stamp))+k*917+seed*941)
    for depth in range(k):
        candidates=[];seen=set()
        for state,path in beam:
            choices=pooled_choices(m,state,rng,branch)if mode==3 else m.million_choices(state,rng,branch)
            for aid,gain in choices:
                if path and aid==path[-1]:continue
                child=m.clone_cluster_state(state);child.apply(aid)
                if mode==1:
                    stampkey=min(bytes(child.stamp[p]for p in rotation)for rotation in rotations)
                    key=bytes(child.grid)+stampkey
                else:key=bytes(child.grid+child.stamp)
                if key in seen:continue
                seen.add(key)
                p2=path+[aid]
                if child.matches>bestscore:best,bestscore=p2,child.matches
                if bestscore==upper:return [ops[x]for x in best]
                future=max(0,child.best()[0])if depth+1<k else 0
                if mode==2 and depth+2<k:
                    follow=m.million_choices(child,rng,2);roll=0
                    for a,g in follow:
                        nxt=m.clone_cluster_state(child);nxt.apply(a)
                        roll=max(roll,g+max(0,nxt.best()[0]))
                    future=roll
                potential=math.log2(child.best_candidates()[1].bit_count())if mode==4 else 0
                if mode==6:
                    planes=child.old_planes
                    potential=sum((1<<(2*i))*plane.bit_count()for i,plane in enumerate(planes))
                    potential+=sum((1<<(i+j+1))*(planes[i]&planes[j]).bit_count()for i in range(4)for j in range(i+1,4))
                    potential/=4*d*d
                priority=child.matches+1.0*future+strength*potential
                candidates.append((priority,rng.random(),child,p2))
        if not candidates:break
        candidates.sort(key=lambda row:row[:2],reverse=True)
        beam=[];counts={};deferred=[]
        for _,_,child,path in candidates:
            sig=tuple(child.stamp)
            if counts.get(sig,0)>=max(2,width//4):deferred.append((child,path));continue
            counts[sig]=counts.get(sig,0)+1;beam.append((child,path))
            if len(beam)>=width:break
        if len(beam)<width:beam.extend(deferred[:width-len(beam)])
        if mode==5 and depth>=k-4:
            finalists.extend((state.matches,path)for state,path in beam)
    path=best
    if refine:
        actions=list(zip(indices,ops))
        path=m.refine(n,d,k,grid+stamp,target,actions,path,passes=6)
        path=m.pair_sweep(n,d,k,grid+stamp,target,actions,path,passes=2,width=24)
        if mode==5:
            def score(sequence):
                board=grid+stamp
                for aid in sequence:m._st(board,nn,indices[aid])
                return sum(a==b for a,b in zip(board,target))
            selected=[best];bestvalue=score(path)
            pool=[row for row in finalists if row[0]>=bestscore-2]
            for _ in range(3):
                if not pool:break
                _,candidate=max(pool,key=lambda row:(min(sum(a!=b for a,b in zip(row[1],old))+abs(len(row[1])-len(old))for old in selected),row[0]))
                selected.append(candidate)
                pool=[row for row in pool if row[1]!=candidate]
                candidate=m.refine(n,d,k,grid+stamp,target,actions,candidate,passes=6)
                candidate=m.pair_sweep(n,d,k,grid+stamp,target,actions,candidate,passes=2,width=24)
                value=score(candidate)
                if value>bestvalue:path,bestvalue=candidate,value
    return [ops[x]for x in path]
