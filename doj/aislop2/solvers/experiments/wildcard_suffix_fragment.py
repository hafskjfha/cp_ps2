def solve(n,d,c,k,grid,target,stamp):
    reference=solve_without_suffix_finish(n,d,c,k,grid,target,stamp)
    if n!=4 or d!=3 or k<6 or color_bound(grid+stamp,target)<16:
        return reference
    indices,_,ops,_,_=build(n,d,target)
    board,buffer=grid[:],stamp[:]
    for x,y,r in reference:
        transition(board,buffer,indices[(x*2+y)*4+r])
    if board==target:
        return reference
    tried=set()
    for remove in (2,4,8,12):
        length=max(0,len(reference)-remove)
        if length in tried:
            continue
        tried.add(length)
        board,buffer=grid[:],stamp[:]
        for x,y,r in reference[:length]:
            transition(board,buffer,indices[(x*2+y)*4+r])
        tail=wildcard_finish(board,target,buffer,k-length)
        if tail is not None:
            return reference[:length]+[ops[aid] for aid in tail]
    return reference
