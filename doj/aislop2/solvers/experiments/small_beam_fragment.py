def solve(n,d,c,k,grid,target,stamp):
    reference=solve_without_deep_beam(n,d,c,k,grid,target,stamp)
    if n>6 or k<=24:
        return reference
    indices,_,ops,_,_=build(n,d,target)
    actions=list(zip(indices,ops))
    width=n-d+1
    def evaluate(operations):
        final,buffer=grid[:],stamp[:]
        for x,y,r in operations:
            transition(final,buffer,indices[(x*width+y)*4+r])
        return sum(a==b for a,b in zip(final,target))
    reference_score=evaluate(reference)
    if reference_score==color_bound(grid+stamp,target):
        return reference
    candidate=finite_beam(n,d,c,min(k,60),grid,target,stamp,width=96)
    sequence=[((x*width+y)*4+r) for x,y,r in candidate]
    sequence=refine(n,d,k,grid+stamp,target,actions,sequence)
    candidate=[actions[aid][1] for aid in sequence]
    return candidate if evaluate(candidate)>reference_score else reference
