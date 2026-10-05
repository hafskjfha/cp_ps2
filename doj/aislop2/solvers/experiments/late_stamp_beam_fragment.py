def stamp_beam_finish(n,grid,target,stamp,k):

    if k<=0:

        return None

    nn=n*n

    initial_score=sum(a==b for a,b in zip(grid,target))

    if initial_score==color_bound(grid+stamp,target):

        return None

    need=[0]*8
    for actual,wanted_color in zip(grid,target):
        if actual!=wanted_color:
            need[wanted_color]+=1
    utility=[sum(need[(value>>(3*j))&7] for j in range(3)) for value in range(512)]
    shift_stamp=3*nn
    expand=packed3_transitions(n)

    initial=sum(v<<(3*i) for i,v in enumerate(grid+stamp))

    wanted=sum(v<<(3*i) for i,v in enumerate(target))

    comparison_mask=sum(1<<(3*i) for i in range(nn))

    rng=random.Random(initial+k*997)

    import heapq

    frontier=[(initial,b'')]

    visited={initial}

    for depth in range(min(8,k)):

        candidates={}

        for state,path in frontier:

            for aid,child in expand(state):

                if child in visited or child in candidates:

                    continue

                new_path=path+bytes((aid,))

                diff=child^wanted

                score=nn-((diff|(diff>>1)|(diff>>2))&comparison_mask).bit_count()

                if score>initial_score:

                    return list(new_path)

                carried=child>>shift_stamp
                stamp_value=utility[carried&511]+utility[(carried>>9)&511]+utility[carried>>18]
                candidates[child]=(score,stamp_value,rng.getrandbits(32),new_path)

        if not candidates:

            break

        selected=heapq.nlargest(384,candidates,key=candidates.get)

        frontier=[(state,candidates[state][3]) for state in selected]

        visited.update(selected)

    return None

def solve(n,d,c,k,grid,target,stamp):
    reference=solve_without_stamp_beam(n,d,c,k,grid,target,stamp)
    if not 5<=n<=9 or d!=3 or k-len(reference)<3:
        return reference
    indices,_,ops,_,_=build(n,d,target)
    board,buffer=grid[:],stamp[:]
    width=n-d+1
    for x,y,r in reference:
        transition(board,buffer,indices[(x*width+y)*4+r])
    missing=sum(a!=b for a,b in zip(board,target))
    if not 1<=missing<=8:
        return reference
    tail=stamp_beam_finish(n,board,target,buffer,k-len(reference))
    if tail is None:
        return reference
    for aid in tail:
        transition(board,buffer,indices[aid])
    if sum(a==b for a,b in zip(board,target))<=n*n-missing:
        return reference
    return reference+[ops[aid] for aid in tail]
