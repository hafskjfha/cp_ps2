# Inlined into pool_weighted.py; not a standalone submission.
class WeightedState(State):
    def __init__(self,n,d,c,grid,target,stamp,order=None):
        super().__init__(n,d,c,grid,target,stamp,order)
        self.weights = [2 if min(p//n,p%n,n-1-p//n,n-1-p%n)<d-1 else 1
                        for p in range(n*n)]
        self.size = 2*d*d
        self.heavy_bits = [[0]*c for _ in stamp]
        for rank,action in enumerate(self.order):
            bit = 1<<rank
            for j,p in enumerate(self.actions[action][0]):
                if self.weights[p]==2:
                    self.heavy_bits[j][target[p]] |= bit
        self.counts = [sum(self.weights[p] for p in positions if grid[p]==target[p])
                       for positions in self.regions]
        self.old_planes = [0]*6
        for region,count in enumerate(self.counts):
            value = self.size-count
            for plane in range(6):
                if value & (1<<plane):
                    self.old_planes[plane] |= self.region_bits[region]

    def gain(self,action):
        return sum(self.weights[p] for j,p in enumerate(self.actions[action][0])
                   if self.stamp[j]==self.target[p])-self.counts[action>>2]

    def apply(self,action):
        indices,_ = self.actions[action]
        grid,stamp,target = self.grid,self.stamp,self.target
        changed = set()
        for j,p in enumerate(indices):
            old,new = grid[p],stamp[j]
            stamp[j],grid[p] = old,new
            if (old==target[p]) != (new==target[p]):
                changed.update(self.cover[p])
        for region in changed:
            old = self.counts[region]
            new = sum(self.weights[p] for p in self.regions[region] if grid[p]==target[p])
            self.counts[region] = new
            changed_planes = (self.size-old)^(self.size-new)
            while changed_planes:
                bit = changed_planes & -changed_planes
                self.old_planes[bit.bit_length()-1] ^= self.region_bits[region]
                changed_planes ^= bit
        c = self.c
        self.stampmask = sum(1<<(c*j+value) for j,value in enumerate(stamp))

    def best_candidates(self):
        planes = [0]*6
        for j,color in enumerate(self.stamp):
            heavy = self.heavy_bits[j][color]
            for plane,carry in ((0,self.target_bits[j][color]^heavy),(1,heavy)):
                while carry:
                    previous = planes[plane]
                    planes[plane] = previous^carry
                    carry &= previous
                    plane += 1
        carry = 0
        for plane in range(6):
            a,b = planes[plane],self.old_planes[plane]
            different = a^b
            planes[plane] = different^carry
            carry = (a&b)|(different&carry)
        candidates,value = self.all_actions,0
        for plane in range(5,-1,-1):
            hits = candidates&planes[plane]
            if hits:
                candidates = hits
                value |= 1<<plane
        return value-self.size,candidates


def solve_weighted(n,d,c,k,initial,target,start_stamp):
    seed = 7418729
    for value in initial+target+start_stamp:
        seed = ((seed^value)*1000003)&0xffffffff
    rng = random.Random(seed)
    order = list(range(4*(n-d+1)**2))
    initial_score = sum(a==b for a,b in zip(initial,target))
    best_score,answer = initial_score,[]
    for restart in range(4):
        if restart:
            rng.shuffle(order)
        state = WeightedState(n,d,c,initial[:],target,start_stamp[:],order[:])
        path,seen,score = [],set(),initial_score
        for _ in range(k):
            seen.add(tuple(state.stamp))
            gain,candidates = state.best_candidates()
            if gain<0:
                break
            chosen = -1
            while candidates:
                bit = candidates&-candidates
                action = state.order[bit.bit_length()-1]
                if gain>0 or tuple(state.grid[p] for p in state.actions[action][0]) not in seen:
                    chosen = action
                    break
                candidates ^= bit
            if chosen<0:
                break
            if gain>0:
                seen.clear()
            score += sum((state.stamp[j]==target[p])-(state.grid[p]==target[p])
                         for j,p in enumerate(state.actions[chosen][0]))
            state.apply(chosen)
            path.append(state.actions[chosen][1])
            if score>best_score:
                best_score,answer = score,path[:]
            if best_score==n*n:
                return answer
    return answer

