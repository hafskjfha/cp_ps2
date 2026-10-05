def refine_trial(state,action,wishes=False):
    if action<0:
        return None
    if wishes:
        grid,stamp,bits=state.wishes,state.wstamp,state.goals
    else:
        grid,stamp,bits=state.grid,state.stamp,state.values
    patch=state.actions[action][0]
    undo=(wishes,patch,[grid[p] for p in patch],stamp[:],
          [row[:] for row in bits],state.counts[:],state.old_planes[:])
    state.apply(action,wishes=wishes)
    return undo


def refine_restore(state,undo):
    if undo is None:
        return
    wishes,patch,colors,stamp,bits,counts,planes=undo
    grid=state.wishes if wishes else state.grid
    for p,color in zip(patch,colors):
        grid[p]=color
    if wishes:
        state.wstamp,state.goals=stamp,bits
    else:
        state.stamp,state.values=stamp,bits
    state.counts,state.old_planes=counts,planes


def optimize_pair(state,first,second,candidates):
    best=operation_gain(state,first)
    undo=refine_trial(state,first)
    best+=operation_gain(state,second)
    refine_restore(state,undo)
    answer=(first,second)
    if best<0:
        best,answer=0,(-1,-1)
    for fixed,side in candidates:
        gain=operation_gain(state,fixed)
        undo=refine_trial(state,fixed,wishes=bool(side))
        chosen,other=state.best()
        refine_restore(state,undo)
        total=gain+other
        if total>=best:
            best=total
            answer=(chosen,fixed) if side else (fixed,chosen)
    return answer


def optimize_triple(state,first,middle,last,left,right):
    best=operation_gain(state,first)
    outer=refine_trial(state,first)
    best+=operation_gain(state,middle)
    inner=refine_trial(state,middle)
    best+=operation_gain(state,last)
    refine_restore(state,inner)
    refine_restore(state,outer)
    answer=(first,middle,last)
    for first in left:
        base=operation_gain(state,first)
        outer=refine_trial(state,first)
        for last in right:
            extra=operation_gain(state,last)
            inner=refine_trial(state,last,wishes=True)
            middle,gain=state.best()
            refine_restore(state,inner)
            total=base+extra+gain
            if total>=best:
                best=total
                answer=(first,middle,last)
        refine_restore(state,outer)
    return answer
