def prune_sequence(nn,initial,target,actions,sequence):
    prefix=initial[:]
    for aid in sequence:
        seq_transition(prefix,nn,actions[aid][0])
    wishes=target+[-1]*(len(initial)-nn)
    kept=[]
    for aid in reversed(sequence):
        patch=actions[aid][0]
        seq_transition(prefix,nn,patch)
        gain=0
        for j,p in enumerate(patch):
            a,b=prefix[p],prefix[nn+j]
            x,y=wishes[p],wishes[nn+j]
            gain+=(b==x)+(a==y)-(a==x)-(b==y)
        if gain>0:
            kept.append(aid)
            seq_transition(wishes,nn,patch)
    return kept[::-1]


def solve(n,d,c,k,grid,target,stamp):
    operations=solve_without_pruning(n,d,c,k,grid,target,stamp)
    if len(operations)<2:
        return operations
    indices,_,ops,_,_=build(n,d,target)
    actions=list(zip(indices,ops))
    width=n-d+1
    sequence=[((x*width+y)*4+r) for x,y,r in operations]
    candidate=prune_sequence(n*n,grid+stamp,target,actions,sequence)
    if len(candidate)<len(sequence):
        candidate=refine(n,d,k,grid+stamp,target,actions,candidate,passes=4)
    return [ops[aid] for aid in candidate]
