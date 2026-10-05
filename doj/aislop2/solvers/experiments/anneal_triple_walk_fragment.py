class TripleWalker:
    def __init__(self,n,d,initial,target,actions,sequence,order):
        self.sequence=sequence[:]
        self.actions=actions
        self.position=0
        self.state=RefineState(n,d,initial,target,actions,order)
        final=initial[:]
        for aid in sequence:
            if aid>=0:
                seq_transition(final,n*n,actions[aid][0])
        self.score=sum(a==b for a,b in zip(final,target))
        for aid in reversed(sequence[3:]):
            if aid>=0:
                self.state.apply(aid,wishes=True)

    def move(self,position):
        if position>self.position:
            steps=range(self.position,position)
        else:
            steps=range(self.position-1,position-1,-1)
        for i in steps:
            a,b=self.sequence[i],self.sequence[i+3]
            if a>=0:
                self.state.apply(a)
            if b>=0:
                self.state.apply(b,wishes=True)
        self.position=position

    def propose(self,first,last):
        state=self.state
        a,b,c=self.sequence[self.position:self.position+3]
        old=operation_gain(state,a)
        if a>=0:
            state.apply(a)
        old+=operation_gain(state,b)
        if b>=0:
            state.apply(b)
        old+=operation_gain(state,c)
        if b>=0:
            state.apply(b)
        if a>=0:
            state.apply(a)
        gain=operation_gain(state,first)
        if first>=0:
            state.apply(first)
        gain+=operation_gain(state,last)
        if last>=0:
            state.apply(last,wishes=True)
        middle,extra=state.best()
        if last>=0:
            state.apply(last,wishes=True)
        if first>=0:
            state.apply(first)
        return (first,middle,last),gain+extra-old

    def accept(self,triple,delta):
        self.sequence[self.position:self.position+3]=triple
        self.score+=delta


def anneal_triples(n,d,k,initial,target,actions,sequence,proposals=None):
    import math
    if k<3:
        return sequence
    limit=color_bound(initial,target)
    final=initial[:]
    for aid in sequence:
        if aid>=0:
            seq_transition(final,n*n,actions[aid][0])
    if sum(a==b for a,b in zip(final,target))==limit:
        return [aid for aid in sequence if aid>=0]
    rng=random.Random(sum((i+31)*v for i,v in enumerate(initial))+k*1123+19271)
    order=list(range(len(actions)))
    rng.shuffle(order)
    sequence=sequence+[-1]*(k-len(sequence))
    walker=TripleWalker(n,d,initial,target,actions,sequence,order)
    if proposals is None:
        proposals=min(1600,max(200,360000//(n*n)))
    best_score,best=walker.score,walker.sequence[:]
    period=max(1,proposals//3)
    position=rng.randrange(k-2)
    walker.move(position)
    direction=1
    size=n-d+1
    for step in range(proposals):
        if step and step%period==0:
            rng.shuffle(order)
            walker=TripleWalker(n,d,initial,target,actions,best,order)
            position=rng.randrange(k-2)
            walker.move(position)
        first,last=walker.sequence[position],walker.sequence[position+2]
        side=step%2
        old=last if side else first
        mode=rng.randrange(5)
        if mode<2 and old>=0:
            x,y,r=actions[old][1]
            x=min(size-1,max(0,x+rng.choice((-2,-1,0,0,1,2))))
            y=min(size-1,max(0,y+rng.choice((-2,-1,0,0,1,2))))
            fixed=((x*size+y)*4+rng.randrange(4))
        elif mode==4:
            fixed=-1
        else:
            fixed=rng.randrange(len(actions))
        if side:
            last=fixed
        else:
            first=fixed
        triple,delta=walker.propose(first,last)
        temperature=0.4*(1-(step%period)/period)**2+0.04
        if delta>=0 or rng.random()<math.exp(delta/temperature):
            walker.accept(triple,delta)
            if walker.score>=best_score:
                best_score,best=walker.score,walker.sequence[:]
                if best_score==limit:
                    break
        if k>3:
            if rng.randrange(16)==0:
                direction=-direction
            if not 0<=position+direction<k-2:
                direction=-direction
            position+=direction
            walker.move(position)
    return [aid for aid in best if aid>=0]


def solve(n,d,c,k,grid,target,stamp):
    operations=solve_before_triple_walking(n,d,c,k,grid[:],target,stamp[:])
    if k<=2:
        return operations
    indices,_,ops,_,_=build(n,d,target)
    actions=list(zip(indices,ops))
    size=n-d+1
    sequence=[((x*size+y)*4+r) for x,y,r in operations]
    sequence=anneal_triples(n,d,k,grid+stamp,target,actions,sequence)
    sequence=refine(n,d,k,grid+stamp,target,actions,sequence,passes=2)
    return [actions[aid][1] for aid in sequence]
