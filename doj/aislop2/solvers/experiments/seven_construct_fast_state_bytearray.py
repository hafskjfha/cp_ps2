"""Private beam state: mutable score planes, immutable unused count metadata."""

class ClusterState(State):
    def __init__(self,n,d,c,grid,target,stamp):
        super().__init__(n,d,c,grid,target,stamp)
        self.grid=bytearray(self.grid)
        self.stamp=bytearray(self.stamp)
        region_bits=self.region_bits
        self._runtime_cover_bits=[sum(region_bits[r]for r in ids)for ids in self.cover]

    def apply(self,action):
        grid,stamp,target=self.grid,self.stamp,self.target
        planes=self.old_planes
        cover_bits=self._runtime_cover_bits
        for j,p in enumerate(self.actions[action][0]):
            old,new=grid[p],stamp[j]
            stamp[j],grid[p]=old,new
            delta=(new==target[p])-(old==target[p])
            self.matches+=delta
            if delta:
                carry=cover_bits[p];plane=0
                if delta>0:
                    while carry:
                        previous=planes[plane]
                        planes[plane]=previous^carry
                        carry&=~previous;plane+=1
                else:
                    while carry:
                        previous=planes[plane]
                        planes[plane]=previous^carry
                        carry&=previous;plane+=1


def clone_cluster_state(state):
    child=object.__new__(ClusterState)
    child.__dict__=state.__dict__.copy()
    child.grid=state.grid[:]
    child.stamp=state.stamp[:]
    child.old_planes=state.old_planes[:]
    return child
