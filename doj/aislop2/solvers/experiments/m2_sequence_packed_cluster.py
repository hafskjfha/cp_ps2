"""Private six-bit action fields for the deterministic clustered beam."""


class PackedClusterEngine:
    __slots__=('actions','indices','target','columns','cover','guards','size','count')

    def __init__(self,n,d,c,target,actions):
        self.actions=actions
        self.indices=[action[0] for action in actions]
        self.target=target
        self.size=d*d
        self.count=len(actions)
        self.columns=[[0]*c for _ in range(d*d)]
        self.cover=[0]*(n*n)
        low=0
        for aid,(patch,_) in enumerate(actions):
            bit=1<<(6*aid)
            low|=bit
            for j,p in enumerate(patch):
                self.columns[j][target[p]]|=bit
                self.cover[p]|=bit
        self.guards=low<<5


class PackedClusterState:
    __slots__=('engine','grid','stamp','matches','oldfield','_cluster_wrong','_scores','_best')

    def __init__(self,n,d,c,grid,target,stamp,actions=None,engine=None):
        if actions is None:
            indices,_,ops,_,_=build(n,d,target)
            actions=list(zip(indices,ops))
        self.engine=engine or PackedClusterEngine(n,d,c,target,actions)
        self.grid=bytearray(grid)
        self.stamp=bytearray(stamp)
        self.matches=sum(a==b for a,b in zip(grid,target))
        self.oldfield=sum(self.engine.cover[p] for p in range(n*n) if grid[p]!=target[p])
        self._cluster_wrong=0
        self._scores=None
        self._best=None

    def apply(self,action):
        grid,stamp=self.grid,self.stamp
        engine=self.engine
        field=self.oldfield;matches=self.matches
        for j,p in enumerate(engine.indices[action]):
            old,new=grid[p],stamp[j]
            stamp[j],grid[p]=old,new
            delta=(new==engine.target[p])-(old==engine.target[p])
            if delta:
                matches+=delta
                field-=delta*engine.cover[p]
        self.matches,self.oldfield=matches,field
        self._scores=None
        self._best=None

    def scores(self):
        if self._scores is not None:return self._scores
        columns=self.engine.columns;stamp=self.stamp
        if len(stamp)==4:
            value=self.oldfield+columns[0][stamp[0]]+columns[1][stamp[1]]+columns[2][stamp[2]]+columns[3][stamp[3]]
        else:value=(self.oldfield+columns[0][stamp[0]]+columns[1][stamp[1]]+
                columns[2][stamp[2]]+columns[3][stamp[3]]+columns[4][stamp[4]]+
                columns[5][stamp[5]]+columns[6][stamp[6]]+columns[7][stamp[7]]+
                columns[8][stamp[8]])
        self._scores=value
        return value

    def best(self):
        if self._best is None:
            field=self.scores();candidates=self.engine.guards;value=0
            for plane in range(4,-1,-1):
                hits=candidates&(field<<(5-plane))
                if hits:candidates=hits;value|=1<<plane
            self._best=value,candidates
        else:value,candidates=self._best
        rank=((candidates&-candidates).bit_length()-1)//6
        return value-self.engine.size,rank


def clone_packed_cluster_state(state):
    child=object.__new__(PackedClusterState)
    child.engine=state.engine
    child.grid=state.grid[:]
    child.stamp=state.stamp[:]
    child.matches=state.matches
    child.oldfield=state.oldfield
    child._cluster_wrong=state._cluster_wrong
    child._scores=state._scores
    child._best=state._best
    return child


def packed_cluster_choices(state,rng,branch=6):
    field=state.scores()
    engine=state.engine
    remaining=engine.guards
    out=[];seen={}
    while len(out)<branch and remaining:
        if remaining==engine.guards and state._best is not None:
            value,candidates=state._best
        else:
            candidates,value=remaining,0
            for plane in range(4,-1,-1):
                hits=candidates&(field<<(5-plane))
                if hits:candidates=hits;value|=1<<plane
        remaining^=candidates
        take=min(branch-len(out),4)
        while candidates and take:
            offset=rng.randrange(engine.count)
            after=candidates>>(6*offset)
            rank=((after&-after).bit_length()-1)//6+offset if after else ((candidates&-candidates).bit_length()-1)//6
            candidates^=32<<(6*rank)
            outgoing=tuple(state.grid[p] for p in engine.indices[rank])
            if seen.get(outgoing,0)>=2:continue
            seen[outgoing]=seen.get(outgoing,0)+1
            out.append((rank,value-engine.size))
            take-=1
        if out and value-engine.size<out[0][1]-1:break
    return out
