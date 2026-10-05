"""Joint long-window reconstruction against exact propagated suffix wishes."""
import random


def search_window(m,n,d,start,wanted,indices,reference,depth,width,rng,neutral=False):
    nn=n*n;dd=d*d
    engine=m.FastBack(n,d,start[:nn],wanted[:nn],start[nn:],indices)
    board,_,planes=engine.first
    engine.first=(board,bytearray(wanted[nn:]),planes)
    def score(state):
        return sum(a==b for a,b in zip(state[0],start[:nn]))+sum(a==b for a,b in zip(state[1],start[nn:]))
    backward=list(reversed(reference))
    endpoint=engine.first
    for aid in backward:endpoint=engine.apply(endpoint,aid)
    best_score=score(endpoint);best=backward[:]
    initial_score=score(engine.first)
    if initial_score>best_score or (neutral and initial_score==best_score):best_score,best=initial_score,[]
    upper=sum(min(start.count(color),wanted.count(color))for color in range(6))
    if best_score==upper:return list(reversed(best)),best_score,0
    beam=[(engine.first,[],initial_score)]
    reference_state=engine.first;reference_path=[];expansions=0
    for level in range(depth):
        candidates=[];seen=set()
        incumbent_aid=backward[level]if level<len(backward)else None
        for state,path,value in beam:
            choices=engine.choices(state,rng,6)
            if incumbent_aid is not None and all(a!=incumbent_aid for a,_ in choices):
                wishes,carried,_=state
                extra=sum((carried[j]==start[p])+(wishes[p]==start[nn+j])-
                          (wishes[p]==start[p])-(carried[j]==start[nn+j])
                          for j,p in enumerate(indices[incumbent_aid]))
                choices.append((incumbent_aid,extra))
            for aid,gain in choices:
                if path and aid==path[-1]:continue
                child=engine.apply(state,aid);expansions+=1
                key=bytes(child[0]+child[1])
                if key in seen:continue
                seen.add(key)
                path2=path+[aid];value2=value+gain
                if value2>best_score or (neutral and value2==best_score and
                    (len(path2)<len(best) or (len(path2)==len(best) and rng.random()<0.05))):
                    best_score,best=value2,path2
                if best_score==upper:return list(reversed(best)),best_score,expansions
                future=max(0,engine.best(child))if level+1<depth else 0
                candidates.append((value2*8+future*3,rng.random(),child,path2,value2,key))
        candidates.sort(key=lambda row:(row[0],row[1]),reverse=True)
        selected=candidates[:width]
        beam=[(state,path,value)for _,_,state,path,value,_ in selected]
        # Preserve the exact incumbent trajectory at every depth, even if its
        # intermediate objective is below the beam's normal cutoff.
        if incumbent_aid is not None:
            reference_state=engine.apply(reference_state,incumbent_aid)
            reference_path=reference_path+[incumbent_aid]
            key=bytes(reference_state[0]+reference_state[1])
            if all(item[-1]!=key for item in selected):
                if len(beam)>=width:beam.pop()
                beam.append((reference_state,reference_path,score(reference_state)))
        if not beam:break
    return list(reversed(best)),best_score,expansions


def window_repair(m,n,d,c,k,initial,target,indices,sequence,rounds=3,width=24,
                  depths=(12,24,32),stats=None,neutral=False):
    if k<4 or not sequence:return sequence
    nn=n*n;dd=d*d;wanted_final=target+[6]*dd
    upper=sum(min(initial.count(color),target.count(color))for color in range(c))
    def apply(state,aid):
        for j,p in enumerate(indices[aid]):state[p],state[nn+j]=state[nn+j],state[p]
    def snapshots(path):
        row=initial[:];forward=[row[:]]
        for aid in path:apply(row,aid);forward.append(row[:])
        wishes=wanted_final[:];reverse=[None]*(len(path)+1);reverse[-1]=wishes[:]
        for step in range(len(path)-1,-1,-1):
            apply(wishes,path[step]);reverse[step]=wishes[:]
        return forward,reverse
    best=sequence[:];forward,reverse=snapshots(best)
    best_score=sum(a==b for a,b in zip(forward[-1],wanted_final))
    rng=random.Random(sum((i+67)*v for i,v in enumerate(initial))+k*1907+n*193+d*59)
    total_expansions=0;wins=0;neutral_moves=0;windows=[]
    for trial in range(rounds):
        if best_score==upper:break
        depth=min(depths[trial%len(depths)],k)
        span=min(depth,len(best));depth=min(depth,k-len(best)+span)
        max_left=len(best)-span
        if trial%3==0:left=max_left
        elif trial%3==1:
            # Prefer a weak interval, measured under its exact fixed suffix.
            starts=sorted(set((j*max_left//15 for j in range(16))))
            ranked=sorted((sum(a==b for a,b in zip(forward[p],reverse[p+span])),rng.random(),p)
                          for p in starts)
            left=ranked[-1][2]
        else:left=rng.randrange(max_left+1)
        right=left+span
        block,value,expanded=search_window(m,n,d,forward[left],reverse[right],indices,
                                           best[left:right],depth,width,rng,neutral)
        total_expansions+=expanded
        windows.append(dict(left=left,right=right,depth=depth,score=value,expansions=expanded))
        if value>best_score or (neutral and value==best_score and block!=best[left:right]):
            candidate=best[:left]+block+best[right:]
            assert len(candidate)<=k
            ahead,behind=snapshots(candidate)
            actual=sum(a==b for a,b in zip(ahead[-1],wanted_final))
            assert actual==value,(actual,value)
            if actual>best_score:wins+=1
            else:neutral_moves+=1
            best,best_score,forward,reverse=candidate,actual,ahead,behind
    if stats is not None:stats.update(expansions=total_expansions,accepted_windows=wins,neutral_windows=neutral_moves,windows=windows)
    return best
