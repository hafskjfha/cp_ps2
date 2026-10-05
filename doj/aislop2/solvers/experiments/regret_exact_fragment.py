def regret_exact_tail(n,d,c,k,grid,target,stamp):
    state=State(n,d,c,grid[:],target,stamp[:])
    answer=[]
    best=state.matches
    for first in range(len(state.actions)):
        state.apply(first)
        if state.matches>best:
            best,answer=state.matches,[first]
        if k>=2:
            for second in range(len(state.actions)):
                state.apply(second)
                gain,last=state.best() if k>=3 else (0,-1)
                score=state.matches+max(0,gain)
                if score>best:
                    best=score
                    answer=[first,second]+([last] if gain>0 else [])
                state.apply(second)
                if best==state.limit:
                    break
        state.apply(first)
        if best==state.limit:
            break
    return [state.actions[aid][1] for aid in answer]


_regret_parent=solve

def solve(n,d,c,k,grid,target,stamp):
    reference=_regret_parent(n,d,c,k,grid[:],target,stamp[:])
    if k-len(reference)<1 or 4*(n-d+1)**2>144:
        return reference
    indices,_,ops,_,_=build(n,d,target)
    side=n-d+1
    final,buffer=grid[:],stamp[:]
    for x,y,r in reference:
        transition(final,buffer,indices[(x*side+y)*4+r])
    if sum(a==b for a,b in zip(final,target))==color_bound(grid+stamp,target):
        return reference
    return reference+regret_exact_tail(n,d,c,min(3,k-len(reference)),final,target,buffer)

