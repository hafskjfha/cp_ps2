def patch_allowed(n,d):
    width=n-d+1
    all_bits=(1<<(4*width*width))-1
    allowed=[]
    for x in range(width):
        for y in range(width):
            lo=max(0,y-d+1)
            hi=min(width,y+d)
            overlap=0
            for row in range(max(0,x-d+1),min(width,x+d)):
                overlap |= ((1<<(4*(hi-lo)))-1) << (4*(row*width+lo))
            allowed.append(all_bits^overlap)
    return allowed


def best_patch_exchange(evaluator,allowed,rng,width=64):
    saved_stamp,saved_wstamp=evaluator.stamp,evaluator.wstamp
    regions=list(range(len(evaluator.regions)))
    rng.shuffle(regions)
    regions.sort(key=lambda region:evaluator.counts[region])
    best_gain,best_pair=0,None
    for region in regions[:width]:
        if not allowed[region]:
            continue
        positions=evaluator.regions[region]
        evaluator.stamp=[evaluator.grid[p] for p in positions]
        evaluator.wstamp=[evaluator.wishes[p] for p in positions]
        second,gain=evaluator.best(allowed[region])
        if gain>best_gain:
            best_gain,best_pair=gain,(region*4,second)
    evaluator.stamp,evaluator.wstamp=saved_stamp,saved_wstamp
    return best_gain,best_pair


def solve_patch_exchange(n,d,c,k,grid,target,stamp):
    if k<3 or n<2*d:
        return []
    state=State(n,d,c,grid[:],target,stamp[:])
    evaluator=RefineState(n,d,grid+stamp,target,state.actions,list(range(len(state.actions))))
    allowed=patch_allowed(n,d)
    rng=random.Random(sum((i+1)*value for i,value in enumerate(grid+stamp))+47191)
    operations=[]
    macro_count=0
    while len(operations)<k:
        gain,action=state.best()
        if gain>0:
            plan=(action,)
        elif len(operations)+3<=k and macro_count<8:
            gain,pair=best_patch_exchange(evaluator,allowed,rng)
            if pair is None:
                break
            plan=(pair[0],pair[1],pair[0])
            macro_count+=1
        else:
            break
        for action in plan:
            state.apply(action)
            evaluator.apply(action)
            operations.append(state.actions[action][1])
    return operations
