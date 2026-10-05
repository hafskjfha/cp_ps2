"""Packed comparisons and deterministic diversified greedy plateau search."""
import random
import sys

RUNS = 12
NEUTRAL = True


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
    indices, codes, operations, coverage, patches = build(n,d,target)
    size = d*d
    mask = sum(1 << (3*j) for j in range(size))
    initial_counts = [sum(initial[p] == target[p] for p in patch) for patch in patches]
    initial_score = sum(a == b for a,b in zip(initial,target))
    best_score, answer = initial_score, []
    seed = 917351
    for value in initial+target+start_stamp:
        seed = ((seed ^ value)*1000003) & 0xffffffff
    rng = random.Random(seed)
    order = list(range(len(codes)))
    for run in range(RUNS):
        if run:
            rng.shuffle(order)
        grid, stamp, counts = initial[:], start_stamp[:], initial_counts[:]
        score, path = initial_score, []
        seen = set()
        for step in range(k):
            packed = sum(1 << (6*j+value) for j,value in enumerate(stamp))
            seen.add(packed)
            gain_best, chosen = -1, -1
            for action in order:
                gain = (packed & codes[action]).bit_count() - counts[action >> 2]
                if gain > gain_best:
                    if gain == 0:
                        if not NEUTRAL or run == 0:
                            continue
                        pickup = sum(1 << (6*j+grid[p]) for j,p in enumerate(indices[action]))
                        if pickup in seen:
                            continue
                    gain_best, chosen = gain, action
            if chosen < 0:
                break
            if gain_best > 0:
                seen.clear()
            for j,pos in enumerate(indices[chosen]):
                change = (stamp[j] == target[pos]) - (grid[pos] == target[pos])
                if change:
                    for patch in coverage[pos]:
                        counts[patch] += change
                stamp[j], grid[pos] = grid[pos], stamp[j]
            score += gain_best
            path.append(operations[chosen])
            if score > best_score:
                best_score, answer = score, path[:]
            if best_score == n*n:
                return answer
    return answer


"""Packed greedy with exact positive-total two-move plateau escapes."""
import random
import sys


class State:
    def __init__(self, n, d, c, grid, target, stamp, order=None):
        self.n, self.d, self.c = n, d, c
        self.grid, self.target, self.stamp = grid, target, stamp
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

    def apply(self, action):
        indices, _ = self.actions[action]
        grid, stamp, target = self.grid, self.stamp, self.target
        changed = set()
        for j, p in enumerate(indices):
            old, new = grid[p], stamp[j]
            stamp[j], grid[p] = old, new
            if (old == target[p]) != (new == target[p]):
                changed.update(self.cover[p])
        for region in changed:
            old = self.counts[region]
            new = sum(grid[p] == target[p] for p in self.regions[region])
            self.counts[region] = new
            changed_planes = (self.size-old) ^ (self.size-new)
            while changed_planes:
                bit = changed_planes & -changed_planes
                self.old_planes[bit.bit_length()-1] ^= self.region_bits[region]
                changed_planes ^= bit
        c = self.c
        self.stampmask = sum(1 << (c*j+value) for j,value in enumerate(stamp))

    def best(self):
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
        rank = (candidates & -candidates).bit_length()-1
        return value-self.size, self.order[rank]

    def escape(self, rng, width=32):
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
    for restart in range(4):
        rng = random.Random(seed + restart*87917)
        order = list(range(4*(n-d+1)**2))
        if restart:
            rng.shuffle(order)
        state = State(n, d, c, grid.copy(), target, stamp.copy(), order)
        operations = []
        while len(operations) < k:
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
        if best_matches == n*n:
            break
    return best_operations


def construct(n,d,c,k,grid,target,stamp):
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
        if matches == n*n:
            break
    return best_ops


"""Packed greedy with exact positive-total two-move plateau escapes."""
import random
import sys


class ProductiveState(State):
    def escape(self, rng, width=32, min_gain=-2):
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
    while len(operations) < k:
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


def refine(n,d,k,initial,target,actions,sequence,passes=4):
    nn,dd = n*n,d*d
    seed = sum((i+1)*v for i,v in enumerate(initial))+k*131
    rng = random.Random(seed)
    for iteration in range(passes):
        sequence = sequence+[-1]*min(8,k-len(sequence))
        states = [initial[:]]
        for aid in sequence:
            state = states[-1][:]
            if aid >= 0:
                seq_transition(state,nn,actions[aid][0])
            states.append(state)
        if sum(a == b for a,b in zip(states[-1],target)) == nn:
            return [aid for aid in sequence if aid >= 0]
        wishes = target+[-1]*dd
        order = list(range(len(actions)))
        rng.shuffle(order)
        ordered = [actions[aid] for aid in order]
        for i in range(len(sequence)-1,-1,-1):
            chosen,_ = best_action(states[i],wishes,ordered,nn,dd,allow_zero=True)
            chosen = order[chosen] if chosen >= 0 else -1
            sequence[i] = chosen
            if chosen >= 0:
                seq_transition(wishes,nn,actions[chosen][0])
        sequence = [aid for aid in sequence if aid >= 0]
    return sequence

def solve(n,d,c,k,grid,target,stamp):
    operations = construct(n,d,c,k,grid[:],target,stamp[:])
    indices,_,ops,_,_ = build(n,d,target)
    actions = list(zip(indices,ops))
    width = n-d+1
    sequence = [((x*width+y)*4+r) for x,y,r in operations]
    sequence = refine(n,d,k,grid+stamp,target,actions,sequence)
    return [actions[aid][1] for aid in sequence]

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
