def regret_state(n,d,actual,wanted,actions,order):
    state=RefineState(n,d,actual,wanted[:n*n],actions,order)
    state.wstamp=wanted[n*n:]
    return state


def regret_lookahead(n,d,k,initial,target,actions,sequence,rounds=24):
    nn,dd=n*n,d*d
    initial_wishes=target+[6]*dd
    def snapshots(path):
        actual=initial[:]
        forward=[actual[:]]
        for aid in path:
            seq_transition(actual,nn,actions[aid][0])
            forward.append(actual[:])
        wanted=initial_wishes[:]
        reverse=[None]*(len(path)+1)
        reverse[-1]=wanted[:]
        for i in range(len(path)-1,-1,-1):
            seq_transition(wanted,nn,actions[path[i]][0])
            reverse[i]=wanted[:]
        return forward,reverse
    best=sequence[:]
    forward,reverse=snapshots(best)
    best_score=sum(a==b for a,b in zip(forward[-1],initial_wishes))
    upper=color_bound(initial,target)
    if best_score==upper or len(best)<4:
        return best
    rng=random.Random(sum((i+43)*v for i,v in enumerate(initial))+k*8161)
    for trial in range(rounds):
        length=min(len(best),(6,10,16)[trial%3])
        left=rng.randrange(len(best)-length+1)
        right=left+length
        budget=min(length+2,k-len(best)+length)
        order=list(range(len(actions)))
        rng.shuffle(order)
        state=regret_state(n,d,forward[left],reverse[right],actions,order)
        score=sum(a==b for a,b in zip(forward[left],reverse[right]))
        block=[]
        removed=best[left:right]
        backward=bool(trial%2)
        seen=set()
        for step in range(budget):
            aid,gain=state.best()
            if step+1<budget:
                pair_value=gain
                first=aid
                pool=list(dict.fromkeys([aid]+rng.sample(removed,min(5,len(removed)))))
                for trial_action in pool:
                    if trial_action<0:
                        continue
                    immediate=operation_gain(state,trial_action)
                    state.apply(trial_action,wishes=backward)
                    _,following=state.best()
                    state.apply(trial_action,wishes=backward)
                    value=immediate+following
                    if value>pair_value:
                        pair_value,first,gain=value,trial_action,immediate
                aid=first
            if aid<0:
                break
            state.apply(aid,wishes=backward)
            block.append(aid)
            score+=gain
            signature=tuple(state.wstamp if backward else state.stamp)
            if not gain and signature in seen:
                break
            if gain:
                seen.clear()
            seen.add(signature)
            if score>best_score:
                middle=list(reversed(block)) if backward else block[:]
                candidate=best[:left]+middle+best[right:]
                best,best_score=candidate,score
                forward,reverse=snapshots(best)
                break
        if best_score==upper:
            break
    return best


_regret_parent=solve

def solve(n,d,c,k,grid,target,stamp):
    reference=_regret_parent(n,d,c,k,grid[:],target,stamp[:])
    if k<4:
        return reference
    indices,_,ops,_,_=build(n,d,target)
    width=n-d+1
    sequence=[(x*width+y)*4+r for x,y,r in reference]
    candidate=regret_lookahead(n,d,k,grid+stamp,target,list(zip(indices,ops)),sequence)
    return [ops[aid] for aid in candidate]

