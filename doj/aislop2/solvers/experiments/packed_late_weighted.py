"""Packed comparisons and deterministic diversified greedy plateau search."""
import random
import sys

RUNS = 12
NEUTRAL = True


def color_bound(initial, target):
    available, needed = [0]*6,[0]*6
    for value in initial:
        available[value] += 1
    for value in target:
        needed[value] += 1
    return sum(min(a,b) for a,b in zip(available,needed))


def build(n, d, target):
    rotations = []
    for r in range(4):
        rotations.append([p*n+q for u in range(d) for v in range(d)
                          for p,q in [((u,v),(v,d-1-u),(d-1-u,d-1-v),(d-1-v,u))[r]]])
    indices, codes, operations = [], [], []
    coverage = [[] for _ in range(n*n)]
    patches = []
    for x in range(n-d+1):
        for y in range(n-d+1):
            patch = len(patches)
            positions = [x*n+y+v for v in rotations[0]]
            patches.append(positions)
            for pos in positions:
                coverage[pos].append(patch)
            for r in range(4):
                action = tuple(x*n+y+v for v in rotations[r])
                indices.append(action)
                codes.append(sum(1 << (6*j+target[pos]) for j,pos in enumerate(action)))
                operations.append((x,y,r))
    return indices, codes, operations, coverage, patches


def transition(grid, stamp, indices):
    for j,pos in enumerate(indices):
        stamp[j], grid[pos] = grid[pos], stamp[j]


def solve_plateau(n,d,c,k,initial,target,start_stamp):
    initial_score = sum(a == b for a,b in zip(initial,target))
    limit = color_bound(initial+start_stamp,target)
    if initial_score == limit:
        return []
    best_score, answer = initial_score, []
    seed = 917351
    for value in initial+target+start_stamp:
        seed = ((seed ^ value)*1000003) & 0xffffffff
    rng = random.Random(seed)
    order = list(range(4*(n-d+1)**2))
    for run in range(RUNS):
        if run:
            rng.shuffle(order)
        state = State(n,d,c,initial[:],target,start_stamp[:],order[:])
        score, path = initial_score, []
        seen = set()
        for step in range(k):
            seen.add(tuple(state.stamp))
            gain, candidates = state.best_candidates()
            if gain < 0 or (gain == 0 and (not NEUTRAL or run == 0)):
                break
            chosen = -1
            while candidates:
                bit = candidates & -candidates
                action = state.order[bit.bit_length()-1]
                if gain > 0 or tuple(state.grid[p] for p in state.actions[action][0]) not in seen:
                    chosen = action
                    break
                candidates ^= bit
            if chosen < 0:
                break
            if gain > 0:
                seen.clear()
            state.apply(chosen)
            score += gain
            path.append(state.actions[chosen][1])
            if score > best_score:
                best_score, answer = score, path[:]
            if best_score == limit:
                return answer
    return answer


class State:
    _geometry_cache = None
    def __init__(self, n, d, c, grid, target, stamp, order=None):
        self.n, self.d, self.c = n, d, c
        self.grid, self.target, self.stamp = grid, target, stamp
        self.matches = sum(a==b for a,b in zip(grid,target))
        self.limit = color_bound(grid+stamp,target)
        key = (n,d,c,tuple(target))
        cached = State._geometry_cache
        if cached is not None and cached[0]==key:
            self.regions,self.actions,self.masks,self.cover = cached[1:]
        else:
            self.regions = []
            self.actions = []
            self.masks = []
            self.cover = [[] for _ in grid]
            rotations = []
            for r in range(4):
                offsets = []
                for u in range(d):
                    for v in range(d):
                        p, q = ((u,v), (v,d-1-u), (d-1-u,d-1-v), (d-1-v,u))[r]
                        offsets.append(p*n+q)
                rotations.append(offsets)
            for x in range(n-d+1):
                for y in range(n-d+1):
                    base = x*n+y
                    indices = tuple(base+o for o in rotations[0])
                    region = len(self.regions)
                    self.regions.append(indices)
                    for p in indices:
                        self.cover[p].append(region)
                    for r in range(4):
                        indices = tuple(base+o for o in rotations[r])
                        self.actions.append((indices, (x,y,r)))
                        self.masks.append(sum(1 << (c*j+target[p]) for j,p in enumerate(indices)))
            State._geometry_cache = (key,self.regions,self.actions,self.masks,self.cover)
        self.order = list(range(len(self.actions))) if order is None else order
        self.counts = [sum(grid[p] == target[p] for p in indices) for indices in self.regions]
        self.stampmask = sum(1 << (c*j+value) for j,value in enumerate(stamp))
        self.size = d*d
        self.all_actions = (1 << len(self.actions)) - 1
        self.target_bits = [[0]*c for _ in stamp]
        self.region_bits = [0]*len(self.regions)
        for rank, action in enumerate(self.order):
            bit = 1 << rank
            self.region_bits[action >> 2] |= bit
            for j, p in enumerate(self.actions[action][0]):
                self.target_bits[j][target[p]] |= bit
        self.old_planes = [0]*4
        for region, count in enumerate(self.counts):
            value = self.size-count
            for plane in range(4):
                if value & (1 << plane):
                    self.old_planes[plane] |= self.region_bits[region]

    def gain(self, action):
        return (self.stampmask & self.masks[action]).bit_count() - self.counts[action >> 2]

    def apply(self,action):
        indices,_ = self.actions[action]
        grid,stamp,target = self.grid,self.stamp,self.target
        changed = {}
        for j,p in enumerate(indices):
            old,new = grid[p],stamp[j]
            stamp[j],grid[p] = old,new
            delta = (new==target[p])-(old==target[p])
            self.matches += delta
            if delta:
                for region in self.cover[p]:
                    changed[region] = changed.get(region,0)+delta
        counts,planes,region_bits = self.counts,self.old_planes,self.region_bits
        size = self.size
        for region,delta in changed.items():
            if not delta:
                continue
            old = counts[region]
            new = old+delta
            counts[region] = new
            changed_planes = (size-old)^(size-new)
            bits = region_bits[region]
            while changed_planes:
                bit = changed_planes&-changed_planes
                planes[bit.bit_length()-1] ^= bits
                changed_planes ^= bit
        c = self.c
        self.stampmask = sum(1<<(c*j+value) for j,value in enumerate(stamp))

    def best_candidates(self):
        planes = [0]*5
        for j, color in enumerate(self.stamp):
            carry = self.target_bits[j][color]
            plane = 0
            while carry:
                previous = planes[plane]
                planes[plane] = previous ^ carry
                carry &= previous
                plane += 1
        carry = 0
        for plane in range(4):
            a, b = planes[plane], self.old_planes[plane]
            different = a ^ b
            planes[plane] = different ^ carry
            carry = (a & b) | (different & carry)
        planes[4] = carry
        candidates, value = self.all_actions, 0
        for plane in range(4, -1, -1):
            hits = candidates & planes[plane]
            if hits:
                candidates = hits
                value |= 1 << plane
        return value-self.size, candidates

    def best(self):
        gain, candidates = self.best_candidates()
        rank = (candidates & -candidates).bit_length()-1
        return gain, self.order[rank]

    def escape(self, rng, width=64):
        mask, counts = self.stampmask, self.counts
        candidates = [(mask & m).bit_count() - counts[i >> 2]
                      for i,m in enumerate(self.masks)]
        eligible = [i for i,g in enumerate(candidates) if g >= -2]
        rng.shuffle(eligible)
        top = sorted(eligible, key=lambda i: candidates[i], reverse=True)[:8]
        ordered = top + eligible
        seen, tried = set(), set()
        best_total, pair = 0, None
        examined = 0
        for first in ordered:
            if first in tried:
                continue
            tried.add(first)
            indices, _ = self.actions[first]
            outgoing = tuple(self.grid[p] for p in indices)
            signature = (outgoing, candidates[first])
            if signature in seen:
                continue
            seen.add(signature)
            first_gain = candidates[first]
            self.apply(first)
            second_gain, second = self.best()
            total = first_gain + second_gain
            self.apply(first)
            if total > best_total:
                best_total, pair = total, (first, second)
            examined += 1
            if examined >= width:
                break
        return pair



def solve_lookahead(n, d, c, k, grid, target, stamp):
    seed = n*101+d*19+c*7+k
    for p in range(0, len(grid), 11):
        seed = (seed*131+grid[p]*7+target[p]) & 0xffffffff
    best_matches, best_operations = -1, []
    for restart in range(8):
        rng = random.Random(seed + restart*87917)
        order = list(range(4*(n-d+1)**2))
        if restart:
            rng.shuffle(order)
        state = State(n, d, c, grid.copy(), target, stamp.copy(), order)
        operations = []
        while len(operations) < k and state.matches < state.limit:
            gain, action = state.best()
            if gain > 0:
                state.apply(action)
                operations.append(state.actions[action][1])
            elif len(operations)+2 <= k:
                pair = state.escape(rng)
                if pair is None:
                    break
                for action in pair:
                    state.apply(action)
                    operations.append(state.actions[action][1])
            else:
                break
        matches = sum(a == t for a,t in zip(state.grid, target))
        if matches > best_matches:
            best_matches, best_operations = matches, operations
        if best_matches == state.limit:
            break
    return best_operations


def construct(n,d,c,k,grid,target,stamp):
    limit = color_bound(grid+stamp,target)
    if sum(a==b for a,b in zip(grid,target)) == limit:
        return []
    indices, codes, operations, coverage, patches = build(n,d,target)
    width = n-d+1
    best_matches = -1
    best_ops = []
    for search in (solve_plateau, solve_lookahead, solve_productive):
        ops = search(n,d,c,k,grid[:],target,stamp[:])
        final, buffer = grid[:],stamp[:]
        for x,y,r in ops:
            action = ((x*width+y)*4+r)
            transition(final,buffer,indices[action])
        matches = sum(a==b for a,b in zip(final,target))
        if matches > best_matches:
            best_matches,best_ops = matches,ops
        if matches == limit:
            break
    return best_ops


"""Packed greedy with exact positive-total two-move plateau escapes."""
import random
import sys


class ProductiveState(State):
    def escape(self, rng, width=64, min_gain=-2):
        mask, counts = self.stampmask, self.counts
        candidates = [(mask & m).bit_count() - counts[i >> 2]
                      for i,m in enumerate(self.masks)]
        eligible = [i for i,g in enumerate(candidates) if g >= min_gain]
        rng.shuffle(eligible)
        top = sorted(eligible, key=lambda i: candidates[i], reverse=True)[:8]
        ordered = top + eligible
        seen, tried = set(), set()
        best_total, pair = 0, None
        examined = 0
        for first in ordered:
            if first in tried:
                continue
            tried.add(first)
            indices, _ = self.actions[first]
            outgoing = tuple(self.grid[p] for p in indices)
            signature = (outgoing, candidates[first])
            if signature in seen:
                continue
            seen.add(signature)
            first_gain = candidates[first]
            self.apply(first)
            second_gain, second = self.best()
            total = first_gain + second_gain
            self.apply(first)
            if total > best_total:
                best_total, pair = total, (first, second)
            examined += 1
            if examined >= width:
                break
        return pair



def solve_productive(n, d, c, k, grid, target, stamp):
    state = ProductiveState(n, d, c, grid, target, stamp)
    seed = n*101+d*19+c*7+k
    for p in range(0, len(grid), 11):
        seed = (seed*131+grid[p]*7+target[p]) & 0xffffffff
    rng = random.Random(seed)
    operations = []
    while len(operations) < k and state.matches < state.limit:
        gain, action = state.best()
        if gain > 0:
            if len(operations)+2 <= k:
                pair = state.escape(rng, width=8, min_gain=max(1, gain-1))
                if pair is not None:
                    action = pair[0]
            state.apply(action)
            operations.append(state.actions[action][1])
        elif len(operations)+2 <= k:
            pair = state.escape(rng)
            if pair is None:
                break
            for action in pair:
                state.apply(action)
                operations.append(state.actions[action][1])
        else:
            break
    return operations


def seq_transition(state, nn, indices):
    for j,pos in enumerate(indices):
        state[nn+j],state[pos] = state[pos],state[nn+j]


def best_action(state, wishes, actions, nn, dd, current=-1, allow_zero=False):
    grid,wanted = state[:nn],wishes[:nn]
    losses = [value == goal for value,goal in zip(grid,wanted)]
    rows = []
    for j in range(dd):
        carried,goal = state[nn+j],wishes[nn+j]
        fixed_loss = carried == goal
        rows.append([(carried == desire)+(value == goal)-loss-fixed_loss
                     for value,desire,loss in zip(grid,wanted,losses)])
    best_id,best_gain = -1,0
    if current >= 0:
        old = sum(rows[j][pos] for j,pos in enumerate(actions[current][0]))
        if old >= 0:
            best_id,best_gain = current,old
    if dd == 4:
        g0,g1,g2,g3 = rows
        for aid,(p,_) in enumerate(actions):
            gain = g0[p[0]]+g1[p[1]]+g2[p[2]]+g3[p[3]]
            if gain > best_gain or (allow_zero and best_id < 0 and gain == best_gain):
                best_id,best_gain = aid,gain
    else:
        g0,g1,g2,g3,g4,g5,g6,g7,g8 = rows
        for aid,(p,_) in enumerate(actions):
            gain = (g0[p[0]]+g1[p[1]]+g2[p[2]]+g3[p[3]]+g4[p[4]]+
                    g5[p[5]]+g6[p[6]]+g7[p[7]]+g8[p[8]])
            if gain > best_gain or (allow_zero and best_id < 0 and gain == best_gain):
                best_id,best_gain = aid,gain
    return best_id,best_gain


def greedy(n,d,k,grid,target,stamp,actions):
    nn,dd = n*n,d*d
    state,wishes = grid+stamp,target+[-1]*dd
    sequence = []
    for _ in range(k):
        aid,gain = best_action(state,wishes,actions,nn,dd)
        if gain <= 0:
            break
        seq_transition(state,nn,actions[aid][0])
        sequence.append(aid)
    return sequence


_REFINE_GEOMETRY = {}

class RefineState:
    def __init__(self,n,d,initial,target,actions,order):
        nn,dd=n*n,d*d
        self.nn,self.dd=nn,dd
        self.grid,self.stamp=initial[:nn],initial[nn:]
        self.wishes,self.wstamp=target[:],[6]*dd
        self.actions,self.order=actions,order
        size=len(actions)
        self.all_bits=(1<<size)-1
        key=(n,d)
        geometry=_REFINE_GEOMETRY.get(key)
        if geometry is None:
            positions=[[0]*nn for _ in range(dd)]
            region_bits=[15<<(4*r) for r in range(size//4)]
            regions=[actions[i][0] for i in range(0,size,4)]
            cover=[[] for _ in range(nn)]
            for r,patch in enumerate(regions):
                for p in patch:
                    cover[p].append(r)
            for aid,(patch,_) in enumerate(actions):
                bit=1<<aid
                for j,p in enumerate(patch):
                    positions[j][p]|=bit
            geometry=positions,region_bits,regions,cover
            _REFINE_GEOMETRY[key]=geometry
        self.positions,self.region_bits,self.regions,self.cover=geometry
        self.values=[[0]*7 for _ in range(dd)]
        self.goals=[[0]*7 for _ in range(dd)]
        for j in range(dd):
            values,goals=self.values[j],self.goals[j]
            for p,mask in enumerate(self.positions[j]):
                values[self.grid[p]]|=mask
                goals[self.wishes[p]]|=mask
        self.tie_masks=[0]*size.bit_length()
        for rank,aid in enumerate(order):
            bit=1<<aid
            while rank:
                low=rank&-rank
                self.tie_masks[low.bit_length()-1]|=bit
                rank^=low
        self.counts=[sum(self.grid[p]==self.wishes[p] for p in patch) for patch in self.regions]
        self.old_planes=[0]*5
        for r,count in enumerate(self.counts):
            value=dd-count
            for plane in range(4):
                if value&(1<<plane):
                    self.old_planes[plane]|=self.region_bits[r]


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
        for mask in reversed(self.tie_masks):
            if not (candidates & (candidates-1)):
                break
            preferred=candidates & ~mask
            if preferred:
                candidates=preferred
        return (candidates & -candidates).bit_length()-1,gain



def refine(n,d,k,initial,target,actions,sequence,passes=8,offset=0,seed_offset=0):
    nn,dd=n*n,d*d
    limit=color_bound(initial,target)
    seed=sum((i+1)*v for i,v in enumerate(initial))+k*131+seed_offset
    rng=random.Random(seed)
    for _ in range(offset):
        rng.shuffle(list(range(len(actions))))
    for iteration in range(passes):
        sequence=sequence+[-1]*min(8,k-len(sequence))
        final=initial[:]
        for action in sequence:
            if action>=0:
                seq_transition(final,nn,actions[action][0])
        if sum(a==b for a,b in zip(final,target))==limit:
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



class SequenceState:
    def __init__(self,initial,target,actions,sequence,nn):
        self.nn=nn
        self.actions=actions
        self.sequence=sequence[:]
        self.prefix=[initial[:]]
        for aid in sequence:
            state=self.prefix[-1][:]
            if aid>=0:
                seq_transition(state,nn,actions[aid][0])
            self.prefix.append(state)
        self.wishes=[None]*(len(sequence)+1)
        self.wishes[-1]=target+[-1]*(len(initial)-nn)
        for i in range(len(sequence)-1,-1,-1):
            wanted=self.wishes[i+1][:]
            if sequence[i]>=0:
                seq_transition(wanted,nn,actions[sequence[i]][0])
            self.wishes[i]=wanted
        self.score=sum(x==y for x,y in zip(self.prefix[-1],target))

    def delta(self,i,replacements):
        nn,actions=self.nn,self.actions
        outgoing=self.prefix[i][:]
        affected=set(range(nn,len(outgoing)))
        for old,new in zip(self.sequence[i:i+len(replacements)],replacements):
            if old>=0:
                affected.update(actions[old][0])
            if new>=0:
                indices=actions[new][0]
                affected.update(indices)
                seq_transition(outgoing,nn,indices)
        previous=self.prefix[i+len(replacements)]
        wishes=self.wishes[i+len(replacements)]
        return sum((outgoing[p]==wishes[p])-(previous[p]==wishes[p]) for p in affected)

    def accept(self,i,replacements,delta):
        nn,actions=self.nn,self.actions
        self.sequence[i:i+len(replacements)]=replacements
        for j in range(i,len(self.sequence)):
            state=self.prefix[j][:]
            aid=self.sequence[j]
            if aid>=0:
                seq_transition(state,nn,actions[aid][0])
            self.prefix[j+1]=state
        for j in range(i+len(replacements)-1,-1,-1):
            wanted=self.wishes[j+1][:]
            aid=self.sequence[j]
            if aid>=0:
                seq_transition(wanted,nn,actions[aid][0])
            self.wishes[j]=wanted
        self.score+=delta


def pair_repair(n,d,k,initial,target,actions,sequence,proposals=None):
    if k<2:
        return sequence
    nn,dd=n*n,d*d
    state=SequenceState(initial,target,actions,sequence+[-1]*(k-len(sequence)),nn)
    if state.score==color_bound(initial,target):
        return sequence
    rng=random.Random(sum((i+7)*v for i,v in enumerate(initial))+k*977+9167)
    width=n-d+1
    if proposals is None:
        proposals=min(2400,max(160,450000//nn))
    for step in range(proposals):
        i=rng.randrange(k-1)
        fixed_slot=step%2
        old=state.sequence[i+fixed_slot]
        mode=rng.randrange(5)
        if mode<2 and old>=0:
            x,y,r=actions[old][1]
            x=min(width-1,max(0,x+rng.choice((-2,-1,0,0,1,2))))
            y=min(width-1,max(0,y+rng.choice((-2,-1,0,0,1,2))))
            action=((x*width+y)*4+rng.randrange(4))
        elif mode==4:
            action=-1
        else:
            action=rng.randrange(len(actions))
        if fixed_slot==0:
            before=state.prefix[i][:]
            if action>=0:
                seq_transition(before,nn,actions[action][0])
            second,_=best_action(before,state.wishes[i+2],actions,nn,dd,
                                 current=state.sequence[i+1],allow_zero=True)
            replacements=[action,second]
        else:
            wished=state.wishes[i+2][:]
            if action>=0:
                seq_transition(wished,nn,actions[action][0])
            first,_=best_action(state.prefix[i],wished,actions,nn,dd,
                                current=state.sequence[i],allow_zero=True)
            replacements=[first,action]
        if state.sequence[i:i+2]==replacements:
            continue
        delta=state.delta(i,replacements)
        if delta>0 or (delta==0 and rng.randrange(8)==0):
            state.accept(i,replacements,delta)
            if state.score==color_bound(initial,target):
                break
    return [aid for aid in state.sequence if aid>=0]


def operation_gain(state,action):
    if action<0:
        return 0
    gain=0
    for j,p in enumerate(state.actions[action][0]):
        v,w=state.stamp[j],state.grid[p]
        a,b=state.wishes[p],state.wstamp[j]
        gain+=(v==a)+(w==b)-(w==a)-(v==b)
    return gain


def optimize_pair(state,first,second,candidates):
    best=operation_gain(state,first)
    if first>=0:
        state.apply(first)
    best+=operation_gain(state,second)
    if first>=0:
        state.apply(first)
    answer=(first,second)
    if best<0:
        best,answer=0,(-1,-1)
    for fixed,side in candidates:
        gain=operation_gain(state,fixed)
        if fixed>=0:
            state.apply(fixed,wishes=bool(side))
        chosen,other=state.best()
        if fixed>=0:
            state.apply(fixed,wishes=bool(side))
        total=gain+other
        if total>=best:
            best=total
            answer=(chosen,fixed) if side else (fixed,chosen)
    return answer


def pair_sweep(n,d,k,initial,target,actions,sequence,passes=4,width=32):
    nn=n*n
    side_len=n-d+1
    rng=random.Random(sum((i+13)*v for i,v in enumerate(initial))+k*691+7147)
    for iteration in range(passes):
        sequence=sequence+[-1]*min(8,k-len(sequence))
        final=initial[:]
        for action in sequence:
            if action>=0:
                seq_transition(final,nn,actions[action][0])
        if sum(a==b for a,b in zip(final,target))==color_bound(initial,target):
            return [action for action in sequence if action>=0]
        order=list(range(len(actions)))
        rng.shuffle(order)
        state=RefineState(n,d,final,target,actions,order)
        i=len(sequence)-1
        if iteration%2 and i>=0:
            old=sequence[i]
            if old>=0:
                state.apply(old)
            chosen,_=state.best()
            sequence[i]=chosen
            if chosen>=0:
                state.apply(chosen,wishes=True)
            i-=1
        while i>=1:
            first,second=sequence[i-1],sequence[i]
            if second>=0:
                state.apply(second)
            if first>=0:
                state.apply(first)
            candidates=[(first,0),(second,1),(-1,0),(-1,1)]
            for _ in range(width):
                side=rng.randrange(2)
                old=second if side else first
                mode=rng.randrange(4)
                if mode==0 and old>=0:
                    x,y,r=actions[old][1]
                    x=min(side_len-1,max(0,x+rng.choice((-1,0,1))))
                    y=min(side_len-1,max(0,y+rng.choice((-1,0,1))))
                    candidate=((x*side_len+y)*4+rng.randrange(4))
                elif mode==1:
                    candidate=rng.choice(sequence)
                else:
                    candidate=rng.randrange(len(actions))
                candidates.append((candidate,side))
            first,second=optimize_pair(state,first,second,candidates)
            sequence[i-1],sequence[i]=first,second
            if second>=0:
                state.apply(second,wishes=True)
            if first>=0:
                state.apply(first,wishes=True)
            i-=2
        if i==0:
            old=sequence[0]
            if old>=0:
                state.apply(old)
            sequence[0],_=state.best()
        sequence=[action for action in sequence if action>=0]
    return sequence


def iterated_refine(n,d,k,initial,target,actions,sequence):
    if n>16:
        return sequence
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
        changed = {}
        for j,p in enumerate(indices):
            old,new = grid[p],stamp[j]
            stamp[j],grid[p] = old,new
            delta = (new==target[p])-(old==target[p])
            self.matches += delta
            if delta:
                delta *= self.weights[p]
                for region in self.cover[p]:
                    changed[region] = changed.get(region,0)+delta
        counts,planes,region_bits = self.counts,self.old_planes,self.region_bits
        size = self.size
        for region,delta in changed.items():
            if not delta:
                continue
            old = counts[region]
            new = old+delta
            counts[region] = new
            changed_planes = (size-old)^(size-new)
            bits = region_bits[region]
            while changed_planes:
                bit = changed_planes&-changed_planes
                planes[bit.bit_length()-1] ^= bits
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
    limit = color_bound(initial+start_stamp,target)
    if best_score==limit:
        return answer
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
            if best_score==limit:
                return answer
    return answer


def construct_pool(n,d,c,k,grid,target,stamp):
    limit = color_bound(grid+stamp,target)
    initial_score = sum(a==b for a,b in zip(grid,target))
    if initial_score==limit:
        return [(limit,[])]
    indices, codes, operations, coverage, patches = build(n,d,target)
    width = n-d+1
    candidates = []
    for search in (solve_plateau, solve_lookahead, solve_productive, solve_weighted):
        ops = search(n,d,c,k,grid[:],target,stamp[:])
        final, buffer = grid[:],stamp[:]
        for x,y,r in ops:
            action = ((x*width+y)*4+r)
            transition(final,buffer,indices[action])
        matches = sum(a==b for a,b in zip(final,target))
        candidates.append((matches,ops))
        if matches == limit:
            break
    candidates.sort(key=lambda row: row[0], reverse=True)
    return candidates


def solve_parent(n,d,c,k,grid,target,stamp):
    pool = construct_pool(n,d,c,k,grid[:],target,stamp[:])
    if pool[0][0] == color_bound(grid+stamp,target):
        return pool[0][1]
    indices,_,ops,_,_ = build(n,d,target)
    actions = list(zip(indices,ops))
    width = n-d+1
    initial = grid+stamp
    best_score,best_sequence = -1,[]
    for _,operations in pool[:4]:
        sequence = [(x*width+y)*4+r for x,y,r in operations]
        sequence = refine(n,d,k,initial,target,actions,sequence,passes=2)
        state = initial[:]
        for aid in sequence:
            seq_transition(state,n*n,actions[aid][0])
        score = sum(a==b for a,b in zip(state,target))
        if score > best_score:
            best_score,best_sequence = score,sequence
    sequence = refine(n,d,k,initial,target,actions,best_sequence,passes=6,offset=2)
    sequence = pair_sweep(n,d,k,initial,target,actions,sequence)
    sequence = pair_repair(n,d,k,initial,target,actions,sequence)
    sequence = refine(n,d,k,initial,target,actions,sequence,passes=2)
    sequence = iterated_refine(n,d,k,initial,target,actions,sequence)
    return [actions[aid][1] for aid in sequence]


def clone_state(state):
    child = object.__new__(State)
    child.__dict__ = state.__dict__.copy()
    child.grid = state.grid[:]
    child.stamp = state.stamp[:]
    child.counts = state.counts[:]
    child.old_planes = state.old_planes[:]
    return child


def beam_actions(state,rng):
    mask,counts = state.stampmask,state.counts
    gains = [(mask&m).bit_count()-counts[i>>2] for i,m in enumerate(state.masks)]
    best = max(gains)
    groups = [[],[],[]]
    for action,gain in enumerate(gains):
        distance = best-gain
        if distance < 3:
            groups[distance].append(action)
    selected = []
    for group,limit in zip(groups,(4,3,1)):
        rng.shuffle(group)
        seen = {}
        for action in group:
            outgoing = tuple(state.grid[p] for p in state.actions[action][0])
            if seen.get(outgoing,0) >= 2:
                continue
            seen[outgoing] = seen.get(outgoing,0)+1
            selected.append((action,gains[action]))
            limit -= 1
            if limit == 0:
                break
    return selected


def finite_beam(n,d,c,k,grid,target,stamp,width=24):
    initial = State(n,d,c,grid[:],target,stamp[:])
    base_score = sum(a==b for a,b in zip(grid,target))
    supply = [0]*c
    wanted = [0]*c
    for color in grid+stamp:
        supply[color] += 1
    for color in target:
        wanted[color] += 1
    upper_gain = sum(min(a,b) for a,b in zip(supply,wanted))-base_score
    if upper_gain <= 0:
        return []
    seed = 47893+k*1009+n*79+d*13+c
    for value in grid+stamp:
        seed = (seed*131+value)&0xffffffff
    rng = random.Random(seed)
    beam = [(initial,0,[])]
    best_gain,best_path = 0,[]
    for depth in range(k):
        children = []
        seen_states = set()
        for state,gain,path in beam:
            for action,delta in beam_actions(state,rng):
                if path and action == path[-1]:
                    continue
                child = clone_state(state)
                child.apply(action)
                signature = bytes(child.grid)+bytes(child.stamp)
                if signature in seen_states:
                    continue
                seen_states.add(signature)
                total = gain+delta
                new_path = path+[action]
                if total > best_gain:
                    best_gain,best_path = total,new_path
                    if best_gain == upper_gain:
                        return [initial.actions[aid][1] for aid in best_path]
                future = max(0,child.best()[0]) if depth+1 < k else 0
                priority = total*2+future
                children.append((priority,total,child,new_path))
        if not children:
            break
        children.sort(key=lambda item:(item[0],item[1]),reverse=True)
        beam = []
        carried_counts = {}
        deferred = []
        for priority,gain,state,path in children:
            key = tuple(state.stamp)
            if carried_counts.get(key,0) >= 3:
                deferred.append((state,gain,path))
                continue
            carried_counts[key] = carried_counts.get(key,0)+1
            beam.append((state,gain,path))
            if len(beam) == width:
                break
        if len(beam) < width:
            beam.extend(deferred[:width-len(beam)])
    return [initial.actions[aid][1] for aid in best_path]


def exact_two(n,d,c,k,grid,target,stamp):
    state = State(n,d,c,grid[:],target,stamp[:])
    gain,action = state.best()
    best_gain,best_path = max(0,gain),([action] if gain > 0 else [])
    if k == 1:
        return [state.actions[aid][1] for aid in best_path]
    ranked = [(state.gain(aid),aid) for aid in range(len(state.actions))]
    ranked.sort(reverse=True)
    for first_gain,first in ranked:
        if first_gain+d*d <= best_gain:
            break
        state.apply(first)
        second_gain,second = state.best()
        total = first_gain+second_gain
        state.apply(first)
        if total > best_gain:
            best_gain,best_path = total,[first,second]
    return [state.actions[aid][1] for aid in best_path]


def construct_all(n,d,c,k,grid,target,stamp):
    if k <= 2:
        return exact_two(n,d,c,k,grid,target,stamp)
    reference = solve_parent(n,d,c,k,grid[:],target,stamp[:])
    if k > 24:
        return reference
    candidate = finite_beam(n,d,c,k,grid,target,stamp,width=24 if k<=12 else 12)
    indices,_,ops,_,_ = build(n,d,target)
    actions = list(zip(indices,ops))
    width = n-d+1
    sequence = [((x*width+y)*4+r) for x,y,r in candidate]
    sequence = refine(n,d,k,grid+stamp,target,actions,sequence)
    candidate = [actions[aid][1] for aid in sequence]
    best_score,best_ops = -1,[]
    for operations in (reference,candidate):
        final,buffer = grid[:],stamp[:]
        for x,y,r in operations:
            transition(final,buffer,indices[(x*width+y)*4+r])
        score = sum(a==b for a,b in zip(final,target))
        if score > best_score:
            best_score,best_ops = score,operations
    return best_ops


def optimize_triple(state,first,middle,last,left,right):
    best=operation_gain(state,first)
    if first>=0:
        state.apply(first)
    best+=operation_gain(state,middle)
    if middle>=0:
        state.apply(middle)
    best+=operation_gain(state,last)
    if middle>=0:
        state.apply(middle)
    if first>=0:
        state.apply(first)
    answer=(first,middle,last)
    for first in left:
        base=operation_gain(state,first)
        if first>=0:
            state.apply(first)
        for last in right:
            extra=operation_gain(state,last)
            if last>=0:
                state.apply(last,wishes=True)
            middle,gain=state.best()
            if last>=0:
                state.apply(last,wishes=True)
            total=base+extra+gain
            if total>=best:
                best=total
                answer=(first,middle,last)
        if first>=0:
            state.apply(first)
    return answer


def triple_refine(n,d,k,initial,target,actions,sequence,passes=2):
    if k<3:
        return sequence
    nn=n*n
    limit=color_bound(initial,target)
    size=n-d+1
    rng=random.Random(sum((i+17)*v for i,v in enumerate(initial))+k*1777+71983)
    for iteration in range(passes):
        sequence=sequence+[-1]*min(6,k-len(sequence))
        final=initial[:]
        for aid in sequence:
            if aid>=0:
                seq_transition(final,nn,actions[aid][0])
        if sum(a==b for a,b in zip(final,target))==limit:
            return [aid for aid in sequence if aid>=0]
        order=list(range(len(actions)))
        rng.shuffle(order)
        state=RefineState(n,d,final,target,actions,order)
        i=len(sequence)-1
        for _ in range(iteration%3):
            if i<0:
                break
            old=sequence[i]
            if old>=0:
                state.apply(old)
            chosen,_=state.best()
            sequence[i]=chosen
            if chosen>=0:
                state.apply(chosen,wishes=True)
            i-=1
        while i>=2:
            first,middle,last=sequence[i-2:i+1]
            for aid in (last,middle,first):
                if aid>=0:
                    state.apply(aid)
            preferred,_=state.best()
            pools=[]
            for old in (first,last):
                mode=rng.randrange(3)
                if mode==0 and old>=0:
                    x,y,r=actions[old][1]
                    x=min(size-1,max(0,x+rng.choice((-1,0,1))))
                    y=min(size-1,max(0,y+rng.choice((-1,0,1))))
                    trial=((x*size+y)*4+rng.randrange(4))
                elif mode==1:
                    p=rng.randrange(nn)
                    for _ in range(10):
                        p=rng.randrange(nn)
                        if state.wishes[p]<6 and state.grid[p]!=state.wishes[p]:
                            break
                    x=min(size-1,max(0,p//n-rng.randrange(d)))
                    y=min(size-1,max(0,p%n-rng.randrange(d)))
                    trial=((x*size+y)*4+rng.randrange(4))
                else:
                    trial=rng.randrange(len(actions))
                pools.append(list(dict.fromkeys((old,-1,preferred,trial))))
            for ending in pools[1]:
                if ending>=0:
                    state.apply(ending,wishes=True)
                starting,_=state.best()
                if ending>=0:
                    state.apply(ending,wishes=True)
                if starting not in pools[0]:
                    pools[0].append(starting)
            first,middle,last=optimize_triple(state,first,middle,last,*pools)
            sequence[i-2:i+1]=first,middle,last
            for aid in (last,middle,first):
                if aid>=0:
                    state.apply(aid,wishes=True)
            i-=3
        while i>=0:
            old=sequence[i]
            if old>=0:
                state.apply(old)
            chosen,_=state.best()
            sequence[i]=chosen
            if chosen>=0:
                state.apply(chosen,wishes=True)
            i-=1
        sequence=[aid for aid in sequence if aid>=0]
    return sequence


def solve_original_iterated(n,d,c,k,grid,target,stamp):
    operations=construct_all(n,d,c,k,grid[:],target,stamp[:])
    if k<=2:
        return operations
    indices,_,ops,_,_=build(n,d,target)
    actions=list(zip(indices,ops))
    side=n-d+1
    sequence=[((x*side+y)*4+r) for x,y,r in operations]
    sequence=triple_refine(n,d,k,grid+stamp,target,actions,sequence)
    sequence=refine(n,d,k,grid+stamp,target,actions,sequence,passes=2)
    return [actions[aid][1] for aid in sequence]


def solve_retained_iterated(n,d,c,k,grid,target,stamp):
    if n>16 or k<=2:
        return solve_original_iterated(n,d,c,k,grid,target,stamp)
    initial=grid+stamp
    indices,_,ops,_,_=build(n,d,target)
    actions=list(zip(indices,ops))
    width=n-d+1
    def evaluate(sequence):
        final=initial[:]
        for aid in sequence:
            seq_transition(final,n*n,indices[aid])
        return sum(a==b for a,b in zip(final,target))
    operations=construct(n,d,c,k,grid[:],target,stamp[:])
    base=[((x*width+y)*4+r) for x,y,r in operations]
    base=refine(n,d,k,initial,target,actions,base)
    base=pair_sweep(n,d,k,initial,target,actions,base)
    base=pair_repair(n,d,k,initial,target,actions,base)
    base=refine(n,d,k,initial,target,actions,base,passes=2)
    perturbed=iterated_refine(n,d,k,initial,target,actions,base)
    if k<=24:
        beam=finite_beam(n,d,c,k,grid,target,stamp,width=24 if k<=12 else 12)
        beam=[((x*width+y)*4+r) for x,y,r in beam]
        beam=refine(n,d,k,initial,target,actions,beam)
        beam_score=evaluate(beam)
        if beam_score>evaluate(base):
            base=beam
        if beam_score>evaluate(perturbed):
            perturbed=beam
    choices=[base]
    if perturbed!=base:
        choices.append(perturbed)
    best_score,best=-1,None
    for candidate in choices:
        candidate=triple_refine(n,d,k,initial,target,actions,candidate)
        candidate=refine(n,d,k,initial,target,actions,candidate,passes=2)
        candidate=anneal_walk(n,d,k,initial,target,actions,candidate)
        candidate=refine(n,d,k,initial,target,actions,candidate,passes=2)
        score=evaluate(candidate)
        if score>best_score:
            best_score,best=score,candidate
    return [ops[aid] for aid in best]


def solve_before_pair_annealing(n,d,c,k,grid,target,stamp):
    reference=solve_retained_iterated(n,d,c,k,grid,target,stamp)
    if n>6 or k<=24:
        return reference
    indices,_,ops,_,_=build(n,d,target)
    actions=list(zip(indices,ops))
    width=n-d+1
    def evaluate(operations):
        final,buffer=grid[:],stamp[:]
        for x,y,r in operations:
            transition(final,buffer,indices[(x*width+y)*4+r])
        return sum(a==b for a,b in zip(final,target))
    reference_score=evaluate(reference)
    if reference_score==color_bound(grid+stamp,target):
        return reference
    candidate=finite_beam(n,d,c,min(k,60),grid,target,stamp,width=96)
    sequence=[((x*width+y)*4+r) for x,y,r in candidate]
    sequence=refine(n,d,k,grid+stamp,target,actions,sequence)
    sequence=anneal_walk(n,d,k,grid+stamp,target,actions,sequence)
    sequence=refine(n,d,k,grid+stamp,target,actions,sequence,passes=2)
    candidate=[actions[aid][1] for aid in sequence]
    return candidate if evaluate(candidate)>reference_score else reference


class PairWalker:
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
        for aid in reversed(sequence[2:]):
            if aid>=0:
                self.state.apply(aid,wishes=True)

    def move(self,position):
        if position>self.position:
            steps=range(self.position,position)
        else:
            steps=range(self.position-1,position-1,-1)
        for i in steps:
            a,b=self.sequence[i],self.sequence[i+2]
            if a>=0:
                self.state.apply(a)
            if b>=0:
                self.state.apply(b,wishes=True)
        self.position=position

    def propose(self,fixed,side):
        state=self.state
        first,second=self.sequence[self.position:self.position+2]
        old=operation_gain(state,first)
        if first>=0:
            state.apply(first)
        old+=operation_gain(state,second)
        if first>=0:
            state.apply(first)
        gain=operation_gain(state,fixed)
        if fixed>=0:
            state.apply(fixed,wishes=bool(side))
        other,extra=state.best()
        if fixed>=0:
            state.apply(fixed,wishes=bool(side))
        pair=(other,fixed) if side else (fixed,other)
        return pair,gain+extra-old

    def accept(self,pair,delta):
        self.sequence[self.position:self.position+2]=pair
        self.score+=delta


def anneal_walk(n,d,k,initial,target,actions,sequence,proposals=None):
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
    rng=random.Random(sum((i+23)*v for i,v in enumerate(initial))+k*1357+7751)
    order=list(range(len(actions)))
    rng.shuffle(order)
    sequence=sequence+[-1]*(k-len(sequence))
    walker=PairWalker(n,d,initial,target,actions,sequence,order)
    if walker.score==limit:
        return [aid for aid in sequence if aid>=0]
    if proposals is None:
        proposals=min(4000,max(300,900000//(n*n)))
    best_score,best=walker.score,walker.sequence[:]
    period=max(1,proposals//4)
    position=rng.randrange(k-1)
    walker.move(position)
    direction=1
    size=n-d+1
    for step in range(proposals):
        if step and step%period==0:
            rng.shuffle(order)
            walker=PairWalker(n,d,initial,target,actions,best,order)
            position=rng.randrange(k-1)
            walker.move(position)
        side=step%2
        old=walker.sequence[position+side]
        mode=rng.randrange(5)
        if mode==0 and old>=0:
            x,y,r=actions[old][1]
            x=min(size-1,max(0,x+rng.choice((-2,-1,0,0,1,2))))
            y=min(size-1,max(0,y+rng.choice((-2,-1,0,0,1,2))))
            fixed=((x*size+y)*4+rng.randrange(4))
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
        if rng.randrange(16)==0:
            direction=-direction
        if not 0<=position+direction<k-1:
            direction=-direction
        position+=direction
        walker.move(position)
    return [aid for aid in best if aid>=0]


def solve_without_binary(n,d,c,k,grid,target,stamp):
    operations=solve_before_pair_annealing(n,d,c,k,grid[:],target,stamp[:])
    if k<=2 or n<=16:
        return operations
    indices,_,ops,_,_=build(n,d,target)
    actions=list(zip(indices,ops))
    size=n-d+1
    sequence=[((x*size+y)*4+r) for x,y,r in operations]
    sequence=anneal_walk(n,d,k,grid+stamp,target,actions,sequence)
    sequence=refine(n,d,k,grid+stamp,target,actions,sequence,passes=2)
    return [actions[aid][1] for aid in sequence]


def binary_transitions():
    rotations=[]
    for r in range(4):
        table=[]
        for value in range(512):
            result=0
            for u in range(3):
                for v in range(3):
                    x,y=((u,v),(v,2-u),(2-u,2-v),(2-v,u))[r]
                    result|=((value>>(u*3+v))&1)<<(x*3+y)
            table.append(result)
        rotations.append(table)
    patches=[]
    for x in range(2):
        for y in range(2):
            base=4*x+y
            scatter=[((v&7)<<base)|((v&56)<<(base+1))|((v&448)<<(base+2)) for v in range(512)]
            paint=[[scatter[v] for v in rotations[r]] for r in range(4)]
            patches.append((base,65535^scatter[511],paint))
    def expand(state):
        board,stamp=state&65535,state>>16
        for position,(base,mask,paint) in enumerate(patches):
            patch=((board>>base)&7)|((board>>(base+1))&56)|((board>>(base+2))&448)
            retained=board&mask
            for rotation in range(4):
                child=retained|paint[rotation][stamp]|(rotations[(-rotation)&3][patch]<<16)
                yield position*4+rotation,child
    return expand


def binary_bfs(grid,target,stamp,k):
    initial=sum(v<<i for i,v in enumerate(grid+stamp))
    wanted=sum(v<<i for i,v in enumerate(target))
    if initial&65535==wanted:
        return []
    required=initial.bit_count()-wanted.bit_count()
    if not 0<=required<=9:
        return None
    expand=binary_transitions()
    forward={initial:(None,None)}
    frontier=[initial]
    first_depth=min(3,k)
    def prefix(state):
        path=[]
        while forward[state][0] is not None:
            state,action=forward[state]
            path.append(action)
        return path[::-1]
    for _ in range(first_depth):
        next_layer=[]
        for state in frontier:
            for action,child in expand(state):
                if child in forward:
                    continue
                forward[child]=(state,action)
                if child&65535==wanted:
                    return prefix(child)
                next_layer.append(child)
        frontier=next_layer
    goals=[wanted|(v<<16) for v in range(512) if v.bit_count()==required]
    backward={state:(None,None) for state in goals}
    frontier=goals
    for _ in range(min(2,k-first_depth)):
        next_layer=[]
        for state in frontier:
            for action,child in expand(state):
                if child in backward:
                    continue
                backward[child]=(state,action)
                if child in forward:
                    answer=prefix(child)
                    while backward[child][0] is not None:
                        child,action=backward[child]
                        answer.append(action)
                    return answer
                next_layer.append(child)
        frontier=next_layer
    return None


def solve_weighted_parent(n,d,c,k,grid,target,stamp):
    if n==4 and d==3 and c==2:
        path=binary_bfs(grid,target,stamp,k)
        if path is not None:
            return [(aid//8,(aid//4)%2,aid%4) for aid in path]
    return solve_without_binary(n,d,c,k,grid,target,stamp)



class WeightedRefineState:
    def __init__(self,n,d,initial,target,weights,actions,order):
        nn,dd = n*n,d*d
        self.nn,self.dd = nn,dd
        self.grid,self.stamp = initial[:nn],initial[nn:]
        self.wishes,self.wstamp = target[:],[6]*dd
        self.weights,self.wstamp_weights = weights[:],[0]*dd
        self.actions,self.order = actions,order
        self.all_bits = (1<<len(actions))-1
        key = (n,d)
        geometry = _REFINE_GEOMETRY.get(key)
        if geometry is None:
            positions = [[0]*nn for _ in range(dd)]
            region_bits = [15<<(4*r) for r in range(len(actions)//4)]
            regions = [actions[i][0] for i in range(0,len(actions),4)]
            cover = [[] for _ in range(nn)]
            for region,patch in enumerate(regions):
                for p in patch:
                    cover[p].append(region)
            for aid,(patch,_) in enumerate(actions):
                bit = 1<<aid
                for j,p in enumerate(patch):
                    positions[j][p] |= bit
            geometry = positions,region_bits,regions,cover
            _REFINE_GEOMETRY[key] = geometry
        self.positions,self.region_bits,self.regions,self.cover = geometry
        self.values = [[0]*7 for _ in range(dd)]
        self.goals = [[0]*7 for _ in range(dd)]
        self.weight_bits = [[0]*3 for _ in range(dd)]
        for j in range(dd):
            values,goals,importance = self.values[j],self.goals[j],self.weight_bits[j]
            for p,mask in enumerate(self.positions[j]):
                values[self.grid[p]] |= mask
                goals[self.wishes[p]] |= mask
                importance[self.weights[p]] |= mask
        self.tie_masks = [0]*len(actions).bit_length()
        for rank,aid in enumerate(order):
            bit = 1<<aid
            while rank:
                low = rank&-rank
                self.tie_masks[low.bit_length()-1] |= bit
                rank ^= low
        self.counts = [sum(self.weights[p]*(self.grid[p]==self.wishes[p]) for p in positions)
                       for positions in self.regions]
        self.old_planes = [0]*6
        for region,count in enumerate(self.counts):
            value = 2*dd-count
            for plane in range(5):
                if value & (1<<plane):
                    self.old_planes[plane] |= self.region_bits[region]

    def apply(self,action,wishes=False):
        changed = {}
        positions,cover,counts = self.positions,self.cover,self.counts
        if wishes:
            grid,stamp = self.wishes,self.wstamp
            weights,stamp_weights = self.weights,self.wstamp_weights
            for j,p in enumerate(self.actions[action][0]):
                old,new = grid[p],stamp[j]
                old_weight,new_weight = weights[p],stamp_weights[j]
                if old != new:
                    for ref in range(self.dd):
                        mask = positions[ref][p]
                        self.goals[ref][old] ^= mask
                        self.goals[ref][new] ^= mask
                if old_weight != new_weight:
                    for ref in range(self.dd):
                        mask = positions[ref][p]
                        self.weight_bits[ref][old_weight] ^= mask
                        self.weight_bits[ref][new_weight] ^= mask
                actual = self.grid[p]
                delta = new_weight*(actual==new)-old_weight*(actual==old)
                if delta:
                    for region in cover[p]:
                        changed[region] = changed.get(region,0)+delta
                stamp[j],grid[p] = old,new
                stamp_weights[j],weights[p] = old_weight,new_weight
        else:
            grid,stamp = self.grid,self.stamp
            for j,p in enumerate(self.actions[action][0]):
                old,new = grid[p],stamp[j]
                if old == new:
                    continue
                for ref in range(self.dd):
                    mask = positions[ref][p]
                    self.values[ref][old] ^= mask
                    self.values[ref][new] ^= mask
                delta = self.weights[p]*((new==self.wishes[p])-(old==self.wishes[p]))
                if delta:
                    for region in cover[p]:
                        changed[region] = changed.get(region,0)+delta
                stamp[j],grid[p] = old,new
        for region,delta in changed.items():
            if not delta:
                continue
            previous = counts[region]
            counts[region] += delta
            change = (2*self.dd-previous)^(2*self.dd-counts[region])
            while change:
                bit = change&-change
                self.old_planes[bit.bit_length()-1] ^= self.region_bits[region]
                change ^= bit

    def best(self):
        planes = [0]*6
        for j in range(self.dd):
            match = self.goals[j][self.stamp[j]]
            parts = [(match&self.weight_bits[j][1],0),
                     (match&self.weight_bits[j][2],1)]
            weight = self.wstamp_weights[j]
            if weight:
                parts.append((self.values[j][self.wstamp[j]],weight-1))
            for carry,plane in parts:
                while carry:
                    old = planes[plane]
                    planes[plane] = old^carry
                    carry &= old
                    plane += 1
        carry = 0
        for plane in range(6):
            a,b = planes[plane],self.old_planes[plane]
            different = a^b
            planes[plane] = different^carry
            carry = (a&b)|(different&carry)
        candidates,value = self.all_bits,0
        for plane in range(5,-1,-1):
            hits = candidates&planes[plane]
            if hits:
                candidates = hits
                value |= 1<<plane
        stamp_loss = sum(w*(a==b) for w,a,b in zip(self.wstamp_weights,self.stamp,self.wstamp))
        gain = value-2*self.dd-stamp_loss
        if gain < 0:
            return -1,0
        for mask in reversed(self.tie_masks):
            if not (candidates&(candidates-1)):
                break
            preferred = candidates&~mask
            if preferred:
                candidates = preferred
        return (candidates&-candidates).bit_length()-1,gain


def weighted_refine(n,d,k,initial,target,weights,actions,sequence,passes=1):
    nn,dd = n*n,d*d
    seed = sum((i+1)*v for i,v in enumerate(initial))+k*131
    seed += sum((i+7)*weight for i,weight in enumerate(weights))*17
    rng = random.Random(seed)
    for iteration in range(passes):
        sequence = sequence+[-1]*min(8,k-len(sequence))
        final = initial[:]
        for action in sequence:
            if action >= 0:
                seq_transition(final,nn,actions[action][0])
        if all(a==b for a,b in zip(final,target)):
            return [action for action in sequence if action>=0]
        order = list(range(len(actions)))
        rng.shuffle(order)
        state = WeightedRefineState(n,d,final,target,weights,actions,order)
        for i in range(len(sequence)-1,-1,-1):
            old = sequence[i]
            if old >= 0:
                state.apply(old)
            chosen,_ = state.best()
            sequence[i] = chosen
            if chosen >= 0:
                state.apply(chosen,wishes=True)
        sequence = [action for action in sequence if action>=0]
    return sequence


def solve_without_late_beam(n,d,c,k,grid,target,stamp):
    reference = solve_weighted_parent(n,d,c,k,grid[:],target,stamp[:])
    if k <= 2:
        return reference
    nn,dd = n*n,d*d
    indices,_,ops,_,_ = build(n,d,target)
    actions = list(zip(indices,ops))
    side = n-d+1
    sequence = [((x*side+y)*4+r) for x,y,r in reference]
    initial,final = grid+stamp,grid+stamp
    for aid in sequence:
        seq_transition(final,nn,indices[aid])
    best_score = sum(a==b for a,b in zip(final,target))
    best_sequence = sequence
    supply,wanted = [0]*c,[0]*c
    for color in initial:
        supply[color] += 1
    for color in target:
        wanted[color] += 1
    upper = sum(min(a,b) for a,b in zip(supply,wanted))
    if best_score == upper:
        return reference
    coverage = [min(p,n-d)-max(0,p-d+1)+1 for p in range(n)]
    maximum = max(coverage)**2
    boundary = [1+(coverage[row]*coverage[col]<maximum)
                for row in range(n) for col in range(n)]
    unresolved = [1+(a!=b) for a,b in zip(final,target)]
    seen_weights = set()
    for weights in (unresolved,boundary):
        signature = tuple(weights)
        if min(weights)==max(weights) or signature in seen_weights:
            continue
        seen_weights.add(signature)
        candidate = weighted_refine(n,d,k,initial,target,weights,actions,sequence)
        candidate = refine(n,d,k,initial,target,actions,candidate,passes=2)
        final = initial[:]
        for aid in candidate:
            seq_transition(final,nn,indices[aid])
        score = sum(a==b for a,b in zip(final,target))
        if score > best_score:
            best_score,best_sequence = score,candidate
            if score == upper:
                break
    return [ops[aid] for aid in best_sequence]


def packed_transitions():
    rotations=[]
    for r in range(4):
        rows=[]
        for u in range(3):
            table=[]
            for value in range(512):
                result=0
                for v in range(3):
                    x,y=((u,v),(v,2-u),(2-u,2-v),(2-v,u))[r]
                    result|=((value>>(3*v))&7)<<(3*(x*3+y))
                table.append(result)
            rows.append(table)
        rotations.append(rows)
    board_mask=(1<<48)-1
    patches=[]
    for x in range(2):
        for y in range(2):
            shift=3*(4*x+y)
            mask=board_mask^((511|(511<<12)|(511<<24))<<shift)
            patches.append((shift,mask))
    def rotate(value,r):
        tables=rotations[r]
        return tables[0][value&511]|tables[1][(value>>9)&511]|tables[2][value>>18]
    def expand(state):
        board,stamp=state&board_mask,state>>48
        rotated=[rotate(stamp,r) for r in range(4)]
        scatter=[(v&511)|((v&261632)<<3)|((v&133955584)<<6) for v in rotated]
        for p,(shift,mask) in enumerate(patches):
            shifted=board>>shift
            patch=(shifted&511)|((shifted>>3)&261632)|((shifted>>6)&133955584)
            retained=board&mask
            for r in range(4):
                child=retained|(scatter[r]<<shift)|(rotate(patch,(-r)&3)<<48)
                yield p*4+r,child
    return expand


def packed_late_beam(grid,target,stamp,k,width=512):
    if k<=0:
        return []
    import heapq
    initial=sum(v<<(3*i) for i,v in enumerate(grid+stamp))
    wanted=sum(v<<(3*i) for i,v in enumerate(target))
    comparison_mask=sum(1<<(3*i) for i in range(16))
    def matches(state):
        diff=state^wanted
        return 16-((diff|(diff>>1)|(diff>>2))&comparison_mask).bit_count()
    best_score=matches(initial)
    upper=color_bound(grid+stamp,target)
    if best_score==upper:
        return []
    best=[]
    expand=packed_transitions()
    rng=random.Random(initial+k*8819)
    frontier=[(initial,b'')]
    visited={initial}
    for depth in range(min(k,80)):
        candidates={}
        for state,path in frontier:
            for aid,child in expand(state):
                if child in visited or child in candidates:
                    continue
                score=matches(child)
                new_path=path+bytes((aid,))
                if score>best_score:
                    best_score,best=score,new_path
                    if score==upper:
                        return list(best)
                candidates[child]=(score,rng.getrandbits(32),new_path)
        if not candidates:
            break
        chosen=heapq.nlargest(width,candidates,key=candidates.get)
        frontier=[(state,candidates[state][2]) for state in chosen]
        visited.update(chosen)
    return list(best)


def solve(n,d,c,k,grid,target,stamp):
    reference=solve_without_late_beam(n,d,c,k,grid,target,stamp)
    if n!=4 or d!=3 or len(reference)>=k:
        return reference
    indices,_,ops,_,_=build(n,d,target)
    board,buffer=grid[:],stamp[:]
    for x,y,r in reference:
        transition(board,buffer,indices[(x*2+y)*4+r])
    tail=packed_late_beam(board,target,buffer,k-len(reference))
    return reference+[ops[aid] for aid in tail]


def main():
    data = list(map(int,sys.stdin.buffer.read().split()))
    n,d,c,k = data[:4]
    nn = n*n
    operations = solve(n,d,c,k,data[4:4+nn],data[4+nn:4+2*nn],data[4+2*nn:])
    print(len(operations))
    for operation in operations:
        print(*operation)


if __name__ == '__main__':
    main()
