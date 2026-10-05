"""Private immutable stamp-plane cache shared by one cluster search's clones."""

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
