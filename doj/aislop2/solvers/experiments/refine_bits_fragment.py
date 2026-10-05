class RefineState:
    def __init__(self, n, d, initial, target, actions, order):
        nn, dd = n*n,d*d
        self.nn,self.dd = nn,dd
        self.grid,self.stamp = initial[:nn],initial[nn:]
        self.wishes,self.wstamp = target[:],[6]*dd
        self.actions,self.order = actions,order
        self.all_bits = (1<<len(actions))-1
        self.positions = [[0]*nn for _ in range(dd)]
        self.values = [[0]*7 for _ in range(dd)]
        self.goals = [[0]*7 for _ in range(dd)]
        self.region_bits = [0]*(len(actions)//4)
        self.regions = [actions[i][0] for i in range(0,len(actions),4)]
        self.cover = [[] for _ in range(nn)]
        for r,positions in enumerate(self.regions):
            for p in positions:
                self.cover[p].append(r)
        for rank,action in enumerate(order):
            bit = 1<<rank
            self.region_bits[action>>2] |= bit
            for j,p in enumerate(actions[action][0]):
                self.positions[j][p] |= bit
                self.values[j][self.grid[p]] |= bit
                self.goals[j][self.wishes[p]] |= bit
        self.counts = [sum(self.grid[p]==self.wishes[p] for p in positions) for positions in self.regions]
        self.old_planes = [0]*5
        for r,count in enumerate(self.counts):
            value = dd-count
            for plane in range(4):
                if value & (1<<plane):
                    self.old_planes[plane] |= self.region_bits[r]

    def apply(self, action, wishes=False):
        if wishes:
            grid,stamp,bits,opposite = self.wishes,self.wstamp,self.goals,self.grid
        else:
            grid,stamp,bits,opposite = self.grid,self.stamp,self.values,self.wishes
        previous = self.counts[:]
        changed = set()
        positions,cover,counts = self.positions,self.cover,self.counts
        for j,p in enumerate(self.actions[action][0]):
            old,new = grid[p],stamp[j]
            if old != new:
                for ref in range(self.dd):
                    mask = positions[ref][p]
                    bits[ref][old] ^= mask
                    bits[ref][new] ^= mask
                delta = (new==opposite[p])-(old==opposite[p])
                if delta:
                    changed.update(cover[p])
                    for region in cover[p]:
                        counts[region] += delta
                stamp[j],grid[p] = old,new
        for region in changed:
            change = (self.dd-previous[region])^(self.dd-counts[region])
            while change:
                bit = change & -change
                self.old_planes[bit.bit_length()-1] ^= self.region_bits[region]
                change ^= bit

    def best(self):
        planes = [0]*5
        for j in range(self.dd):
            for carry in (self.values[j][self.wstamp[j]],self.goals[j][self.stamp[j]]):
                plane=0
                while carry:
                    old=planes[plane]
                    planes[plane]=old^carry
                    carry &= old
                    plane += 1
        carry=0
        for plane in range(5):
            a,b = planes[plane],self.old_planes[plane]
            different=a^b
            planes[plane]=different^carry
            carry=(a&b)|(different&carry)
        candidates,value=self.all_bits,0
        for plane in range(4,-1,-1):
            hits=candidates&planes[plane]
            if hits:
                candidates=hits
                value |= 1<<plane
        gain=value-self.dd-sum(a==b for a,b in zip(self.stamp,self.wstamp))
        if gain < 0:
            return -1,0
        rank=(candidates & -candidates).bit_length()-1
        return self.order[rank],gain


def refine(n,d,k,initial,target,actions,sequence,passes=8):
    nn,dd=n*n,d*d
    seed=sum((i+1)*v for i,v in enumerate(initial))+k*131
    rng=random.Random(seed)
    for iteration in range(passes):
        sequence=sequence+[-1]*min(8,k-len(sequence))
        final=initial[:]
        for action in sequence:
            if action>=0:
                seq_transition(final,nn,actions[action][0])
        if sum(a==b for a,b in zip(final,target))==nn:
            return [action for action in sequence if action>=0]
        order=list(range(len(actions)))
        rng.shuffle(order)
        state=RefineState(n,d,final,target,actions,order)
        for i in range(len(sequence)-1,-1,-1):
            old=sequence[i]
            if old>=0:
                state.apply(old)
            chosen,_=state.best()
            sequence[i]=chosen
            if chosen>=0:
                state.apply(chosen,wishes=True)
        sequence=[action for action in sequence if action>=0]
    return sequence
