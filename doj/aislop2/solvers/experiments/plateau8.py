"""Packed comparisons and deterministic diversified greedy plateau search."""
import random
import sys

RUNS = 8
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
                codes.append(sum(target[pos] << (3*j) for j,pos in enumerate(action)))
                operations.append((x,y,r))
    return indices, codes, operations, coverage, patches


def transition(grid, stamp, indices):
    for j,pos in enumerate(indices):
        stamp[j], grid[pos] = grid[pos], stamp[j]


def solve(n,d,c,k,initial,target,start_stamp):
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
            packed = sum(value << (3*j) for j,value in enumerate(stamp))
            seen.add(packed)
            gain_best, chosen = -1, -1
            for action in order:
                diff = packed ^ codes[action]
                gain = size - ((diff | (diff >> 1) | (diff >> 2)) & mask).bit_count() - counts[action >> 2]
                if gain > gain_best:
                    if gain == 0:
                        if not NEUTRAL or run == 0:
                            continue
                        pickup = sum(grid[p] << (3*j) for j,p in enumerate(indices[action]))
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


def main():
    data = list(map(int,sys.stdin.buffer.read().split()))
    n,d,c,k = data[:4]
    size = n*n
    operations = solve(n,d,c,k,data[4:4+size],data[4+size:4+2*size],data[4+2*size:])
    print(len(operations))
    for operation in operations:
        print(*operation)


if __name__ == '__main__':
    main()
