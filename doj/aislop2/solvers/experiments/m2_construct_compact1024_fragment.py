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


def m2_quotient_construct(n, d, c, k, grid, target, stamp):
    beam_width=1024 if d==3 and n<=16 and 20<=k<=48 else 512 if d==3 and n<=16 and 49<=k<=80 else 64
    packed=beam_width>64
    clone=clone_packed_cluster_state if packed else clone_cluster_state
    choose=packed_cluster_choices if packed else million_choices
    nn = n * n
    indices, _, ops, _, _ = build(n, d, target)
    initial = (PackedClusterState if packed else ClusterState)(n, d, c, grid[:], target, stamp[:])
    upper = color_bound(grid + stamp, target)
    rotations = []
    for r in range(4):
        rotations.append([((u, v), (v, d - 1 - u), (d - 1 - u, d - 1 - v), (d - 1 - v, u))[r][0] * d + ((u, v), (v, d - 1 - u), (d - 1 - u, d - 1 - v), (d - 1 - v, u))[r][1] for u in range(d) for v in range(d)])
    beam = [(initial, [])]
    best = []
    bestscore = initial.matches
    rotation_cache = {}
    rng = random.Random(sum(((i + 51) * v for i, v in enumerate(grid + stamp))) + k * 917 + 0 * 941)
    for depth in range(k):
        candidates = []
        seen = set()
        for state, path in beam:
            choices = choose(state, rng, 6)
            for aid, gain in choices:
                if path and aid == path[-1]:
                    continue
                child = clone(state)
                child.apply(aid)
                rawstamp=bytes(child.stamp)
                stampkey=rotation_cache.get(rawstamp)
                if stampkey is None:
                    stampkey=min(bytes(child.stamp[p]for p in rotation)for rotation in rotations)
                    if len(rotation_cache)>=16384:rotation_cache.clear()
                    rotation_cache[rawstamp]=stampkey
                key = bytes(child.grid) + stampkey
                if key in seen:
                    continue
                seen.add(key)
                p2 = path + [aid]
                if child.matches > bestscore:
                    best, bestscore = (p2, child.matches)
                if bestscore == upper:
                    return [ops[x] for x in best]
                future = max(0, child.best()[0]) if depth + 1 < k else 0
                potential = 0
                priority = child.matches + 0.5 * future + 0 * potential
                candidates.append((priority, rng.random(), child, p2))
        if not candidates:
            break
        candidates.sort(key=lambda row: row[:2], reverse=True)
        beam = []
        counts = {}
        deferred = []
        for _, _, child, path in candidates:
            sig = tuple(child.stamp)
            if counts.get(sig, 0) >= max(2, beam_width // 4):
                deferred.append((child, path))
                continue
            counts[sig] = counts.get(sig, 0) + 1
            beam.append((child, path))
            if len(beam) >= beam_width:
                break
        if len(beam) < beam_width:
            beam.extend(deferred[:beam_width - len(beam)])
    path = best
    actions = list(zip(indices, ops))
    path = refine(n, d, k, grid + stamp, target, actions, path, passes=6)
    path = pair_sweep(n, d, k, grid + stamp, target, actions, path, passes=2, width=24)
    return [ops[x] for x in path]

_m2_constructor_previous_retained=solve_retained_iterated
_m2_constructor_previous_beam=million_beam
_m2_constructor_domain_cache=None

def m2_constructor_domain(n,d,c,k,grid,target,stamp):
    global _m2_constructor_domain_cache
    if n<10 or k<12:return False
    key=(n,d,c,k,tuple(grid),tuple(target),tuple(stamp))
    if _m2_constructor_domain_cache is not None and _m2_constructor_domain_cache[0]==key:
        return _m2_constructor_domain_cache[1]
    result=False
    if 100*sum(a==b for a,b in zip(grid,target))<70*color_bound(grid+stamp,target):
        patterns=set()
        for x in range(n-d+1):
            for y in range(n-d+1):
                patterns.add(tuple(target[(x+i)*n+y+j]for i in range(d)for j in range(d)))
                if len(patterns)>4*c:result=True;break
            if result:break
    _m2_constructor_domain_cache=(key,result)
    return result

def solve_retained_iterated(n,d,c,k,grid,target,stamp):
    if not m2_constructor_domain(n,d,c,k,grid,target,stamp):
        return _m2_constructor_previous_retained(n,d,c,k,grid,target,stamp)
    result=m2_quotient_construct(n,d,c,k,grid,target,stamp)
    return cluster_improve(n,d,c,k,grid,target,stamp,result,width=16)

def million_beam(n,d,c,k,grid,target,stamp,reference,width=12,branch=6,future_weight=4,enhance=False):
    if m2_constructor_domain(n,d,c,k,grid,target,stamp):return reference
    return _m2_constructor_previous_beam(n,d,c,k,grid,target,stamp,reference,width,branch,future_weight,enhance)
