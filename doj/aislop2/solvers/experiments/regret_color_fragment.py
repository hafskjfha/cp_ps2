def regret_color_repair(n,d,c,k,initial,target,actions,sequence,rounds=2):
    nn=n*n
    best=sequence[:]
    def final(path):
        state=initial[:]
        for aid in path:
            seq_transition(state,nn,actions[aid][0])
        return state
    state=final(best)
    score=sum(a==b for a,b in zip(state,target))
    upper=color_bound(initial,target)
    if score==upper:
        return best
    need=[0]*c
    movable=[0]*c
    for value,wanted in zip(state,target):
        if value!=wanted:
            need[wanted]+=1
            movable[value]+=1
    for value in state[nn:]:
        movable[value]+=1
    colors=[v for v in range(c) if need[v] and movable[v]]
    colors.sort(key=lambda v:(need[v]/movable[v],need[v]),reverse=True)
    for color in colors[:rounds]:
        weights=[1+(wanted==color) for wanted in target]
        candidate=weighted_refine(n,d,k,initial,target,weights,actions,best,passes=1)
        candidate=refine(n,d,k,initial,target,actions,candidate,passes=2,seed_offset=5947+color*1777)
        result=final(candidate)
        candidate_score=sum(a==b for a,b in zip(result,target))
        if candidate_score>score:
            best,score=candidate,candidate_score
            if score==upper:
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
    candidate=regret_color_repair(n,d,c,k,grid+stamp,target,list(zip(indices,ops)),sequence)
    return [ops[aid] for aid in candidate]

