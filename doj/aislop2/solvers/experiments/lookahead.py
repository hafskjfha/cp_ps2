"""Packed greedy with exact positive-total two-move plateau escapes."""
import random
import sys


class State:
    def __init__(self, n, d, c, grid, target, stamp):
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
        self.counts = [sum(grid[p] == target[p] for p in indices) for indices in self.regions]
        self.stampmask = sum(1 << (c*j+value) for j,value in enumerate(stamp))

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
            self.counts[region] = sum(grid[p] == target[p] for p in self.regions[region])
        c = self.c
        self.stampmask = sum(1 << (c*j+value) for j,value in enumerate(stamp))

    def best(self):
        mask, masks, counts = self.stampmask, self.masks, self.counts
        best_gain, best_action = -100, -1
        for action, targetmask in enumerate(masks):
            gain = (mask & targetmask).bit_count() - counts[action >> 2]
            if gain > best_gain:
                best_gain, best_action = gain, action
        return best_gain, best_action

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


def solve(n, d, c, k, grid, target, stamp):
    state = State(n, d, c, grid, target, stamp)
    seed = n*101+d*19+c*7+k
    for p in range(0, len(grid), 11):
        seed = (seed*131+grid[p]*7+target[p]) & 0xffffffff
    rng = random.Random(seed)
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
    return operations


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
