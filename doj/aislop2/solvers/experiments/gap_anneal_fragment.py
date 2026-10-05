class GapWalker:
    def __init__(self,n,d,initial,target,actions,sequence,order,gap):
        self.sequence=sequence[:]
        self.actions=actions
        self.gap=gap
        self.position=0
        self.state=RefineState(n,d,initial,target,actions,order)
        final=initial[:]
        for aid in sequence:
            if aid>=0:
                seq_transition(final,n*n,actions[aid][0])
        self.score=sum(a==b for a,b in zip(final,target))
        for aid in reversed(sequence[gap+1:]):
            if aid>=0:
                self.state.apply(aid,wishes=True)
        state=self.state
        self.boundary_score=sum(a==b for a,b in zip(state.grid,state.wishes))
        self.boundary_score+=sum(a==b for a,b in zip(state.stamp,state.wstamp))

    def move(self,position):
        steps=(range(self.position,position) if position>self.position else
               range(self.position-1,position-1,-1))
        for i in steps:
            for aid,wished in ((self.sequence[i],False),
                               (self.sequence[i+self.gap+1],True)):
                if aid>=0:
                    self.boundary_score+=operation_gain(self.state,aid)
                    self.state.apply(aid,wishes=wished)
        self.position=position

    def propose(self,fixed,side):
        state=self.state
        block=self.sequence[self.position:self.position+self.gap+1]
        middle=block[1:-1]
        applied=[fixed]+(middle[::-1] if side else middle)
        gain=0
        for aid in applied:
            if aid>=0:
                gain+=operation_gain(state,aid)
                state.apply(aid,wishes=bool(side))
        other,extra=state.best()
        for aid in reversed(applied):
            if aid>=0:
                state.apply(aid,wishes=bool(side))
        pair=(other,fixed) if side else (fixed,other)
        return pair,self.boundary_score+gain+extra-self.score

    def accept(self,pair,delta):
        self.sequence[self.position]=pair[0]
        self.sequence[self.position+self.gap]=pair[1]
        self.score+=delta


def gap_anneal(n,d,k,initial,target,actions,sequence,proposals=None):
    import math
    if k<4:
        return sequence
    final=initial[:]
    for aid in sequence:
        if aid>=0:
            seq_transition(final,n*n,actions[aid][0])
    best_score=sum(a==b for a,b in zip(final,target))
    limit=color_bound(initial,target)
    if best_score==limit:
        return sequence
    best=sequence+[-1]*(k-len(sequence))
    rng=random.Random(sum((i+61)*v for i,v in enumerate(initial))+k*1117+99317)
    order=list(range(len(actions)))
    if proposals is None:
        proposals=min(1600,max(120,240000//(n*n)))
    period=max(1,proposals//4)
    size=n-d+1
    for step in range(proposals):
        if step%period==0:
            rng.shuffle(order)
            gap=rng.randrange(2,min(k,8))
            walker=GapWalker(n,d,initial,target,actions,best,order,gap)
            position=rng.randrange(k-gap)
            walker.move(position)
            direction=1
        side=step%2
        old=walker.sequence[position+side*gap]
        mode=rng.randrange(5)
        if mode==0 and old>=0:
            x,y,r=actions[old][1]
            x=min(size-1,max(0,x+rng.choice((-2,-1,0,0,1,2))))
            y=min(size-1,max(0,y+rng.choice((-2,-1,0,0,1,2))))
            fixed=(x*size+y)*4+rng.randrange(4)
        elif mode==1:
            fixed=walker.state.best()[0]
        elif mode==4:
            fixed=-1
        else:
            fixed=rng.randrange(len(actions))
        pair,delta=walker.propose(fixed,side)
        temperature=0.4*(1-(step%period)/period)**2+0.04
        if delta>=0 or rng.random()<math.exp(delta/temperature):
            walker.accept(pair,delta)
            if walker.score>=best_score:
                best_score,best=walker.score,walker.sequence[:]
                if best_score==limit:
                    break
        if k-gap>1:
            if rng.randrange(16)==0:
                direction=-direction
            if not 0<=position+direction<k-gap:
                direction=-direction
            position+=direction
            walker.move(position)
    return [aid for aid in best if aid>=0]


def solve(n,d,c,k,grid,target,stamp):
    operations=solve_without_gap(n,d,c,k,grid,target,stamp)
    if k<4:
        return operations
    indices,_,ops,_,_=build(n,d,target)
    actions=list(zip(indices,ops))
    width=n-d+1
    sequence=[((x*width+y)*4+r) for x,y,r in operations]
    candidate=gap_anneal(n,d,k,grid+stamp,target,actions,sequence)
    if candidate!=sequence:
        candidate=refine(n,d,k,grid+stamp,target,actions,candidate,passes=2)
    return [ops[aid] for aid in candidate]
