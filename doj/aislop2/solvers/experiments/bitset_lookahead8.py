"""Bit-sliced full-action gain evaluation with deterministic two-ply search."""
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


def solve(n, d, c, k, grid, target, stamp):
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


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n,d,c,k = data[:4]
    size = n*n
    operations = solve(n,d,c,k,data[4:4+size],data[4+size:4+2*size],data[4+2*size:])
    print(len(operations))
    for operation in operations:
        print(*operation)


if __name__ == '__main__':
    main()
