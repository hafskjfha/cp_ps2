class CachedClusterState(ClusterState):
    cache_limit=8192

    def __init__(self,n,d,c,grid,target,stamp):
        super().__init__(n,d,c,grid,target,stamp)
        self._stamp_score_cache={}

    def _target_score_planes(self):
        key=bytes(self.stamp)
        cache=self._stamp_score_cache
        planes=cache.get(key)
        if planes is None:
            values=[0]*5
            for j,color in enumerate(self.stamp):
                carry=self.target_bits[j][color];plane=0
                while carry:
                    old=values[plane];values[plane]=old^carry;carry&=old;plane+=1
            planes=tuple(values)
            limit=self.cache_limit
            if limit:
                if len(cache)>=limit:cache.clear()
                cache[key]=planes
        return planes

    def _combined_score_planes(self):
        planes=list(self._target_score_planes())
        carry=0
        for plane in range(4):
            a,b=planes[plane],self.old_planes[plane]
            different=a^b;planes[plane]=different^carry;carry=a&b|different&carry
        planes[4]=carry
        return planes

    def best_candidates(self):
        planes=self._combined_score_planes()
        candidates,value=self.all_actions,0
        for plane in range(4,-1,-1):
            hits=candidates&planes[plane]
            if hits:candidates=hits;value|=1<<plane
        return value-self.size,candidates

def clone_cached_cluster_state(state):
    child=object.__new__(CachedClusterState)
    child.__dict__=state.__dict__.copy()
    child.grid=state.grid[:]
    child.stamp=state.stamp[:]
    child.old_planes=state.old_planes[:]
    return child

def cached_cluster_choices(state,rng,branch=6):
    planes=state._combined_score_planes()
    remaining = state.all_actions
    out = []
    count = len(state.actions)
    seen = {}
    while len(out) < branch and remaining:
        candidates, value = (remaining, 0)
        for plane in range(4, -1, -1):
            hits = candidates & planes[plane]
            if hits:
                candidates = hits
                value |= 1 << plane
        remaining ^= candidates
        take = min(branch - len(out), 4)
        while candidates and take:
            offset = rng.randrange(count)
            after = candidates >> offset
            rank = (after & -after).bit_length() - 1 + offset if after else (candidates & -candidates).bit_length() - 1
            candidates ^= 1 << rank
            aid = state.order[rank]
            outgoing = tuple((state.grid[p] for p in state.actions[aid][0]))
            if seen.get(outgoing, 0) >= 2:
                continue
            seen[outgoing] = seen.get(outgoing, 0) + 1
            out.append((aid, value - state.size))
            take -= 1
        if out and value - state.size < out[0][1] - 1:
            break
    return out

CachedClusterState.cache_limit=16384
M2BeamState=CachedClusterState
M2BeamClone=clone_cached_cluster_state
M2BeamChoices=cached_cluster_choices
