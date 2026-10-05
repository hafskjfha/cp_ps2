def solve_retained_iterated(n,d,c,k,grid,target,stamp):
    if n>16 or k<=2:
        return solve_original_iterated(n,d,c,k,grid,target,stamp)
    initial=grid+stamp
    indices,_,ops,_,_=build(n,d,target)
    actions=list(zip(indices,ops))
    width=n-d+1
    def evaluate(sequence):
        final=initial[:]
        for aid in sequence:
            seq_transition(final,n*n,indices[aid])
        return sum(a==b for a,b in zip(final,target))
    operations=construct(n,d,c,k,grid[:],target,stamp[:])
    base=[((x*width+y)*4+r) for x,y,r in operations]
    base=refine(n,d,k,initial,target,actions,base)
    base=pair_sweep(n,d,k,initial,target,actions,base)
    base=pair_repair(n,d,k,initial,target,actions,base)
    base=refine(n,d,k,initial,target,actions,base,passes=2)
    perturbed=iterated_refine(n,d,k,initial,target,actions,base)
    if k<=24:
        beam=finite_beam(n,d,c,k,grid,target,stamp,width=24 if k<=12 else 12)
        beam=[((x*width+y)*4+r) for x,y,r in beam]
        beam=refine(n,d,k,initial,target,actions,beam)
        beam_score=evaluate(beam)
        if beam_score>evaluate(base):
            base=beam
        if beam_score>evaluate(perturbed):
            perturbed=beam
    choices=[base]
    if perturbed!=base:
        choices.append(perturbed)
    best_score,best=-1,None
    for candidate in choices:
        candidate=triple_refine(n,d,k,initial,target,actions,candidate)
        candidate=refine(n,d,k,initial,target,actions,candidate,passes=2)
        score=evaluate(candidate)
        if score>best_score:
            best_score,best=score,candidate
    return [ops[aid] for aid in best]
