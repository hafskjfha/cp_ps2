def iterated_refine(n,d,k,initial,target,actions,sequence):
    nn=n*n
    def evaluate(path):
        final=initial[:]
        for action in path:
            if action>=0:
                seq_transition(final,nn,actions[action][0])
        return sum(a==b for a,b in zip(final,target))
    best_score=evaluate(sequence)
    limit=color_bound(initial,target)
    if best_score==limit:
        return sequence
    rng=random.Random(sum((i+29)*v for i,v in enumerate(initial))+k*2281)
    best=sequence[:]
    width=n-d+1
    restarts=max(2,min(8,9000//(nn+6*k)))
    for restart in range(restarts):
        candidate=best+[-1]*min(8,k-len(best))
        positions=rng.sample(range(len(candidate)),min(len(candidate),2+restart%6))
        for position in positions:
            old=candidate[position]
            mode=rng.randrange(4)
            if old>=0 and mode<2:
                x,y,r=actions[old][1]
                x=max(0,min(width-1,x+rng.choice((-2,-1,0,1,2))))
                y=max(0,min(width-1,y+rng.choice((-2,-1,0,1,2))))
                candidate[position]=(x*width+y)*4+rng.randrange(4)
            elif mode==2:
                candidate[position]=-1
            else:
                candidate[position]=rng.randrange(len(actions))
        candidate=refine(n,d,k,initial,target,actions,candidate,passes=4,
                         seed_offset=37307*(restart+1))
        score=evaluate(candidate)
        if score>=best_score:
            best,best_score=candidate,score
            if score==limit:
                break
    return best
