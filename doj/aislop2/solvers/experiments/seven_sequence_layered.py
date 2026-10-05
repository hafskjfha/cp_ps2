"""Experimental shifted patch-permutation layers; standard-library only.

Each disjoint-patch cycle restores the stamp, optionally up to rotation.
Alternating assignments optimize overlapping tilings against exact suffix labels.
"""
import random
import sys


def hungarian(cost):
    n = len(cost)
    u, v, owner, way = ([0]*(n+1) for _ in range(4))
    for i in range(1, n+1):
        owner[0] = i
        j0 = 0
        minimum = [10**9]*(n+1)
        used = [False]*(n+1)
        while True:
            used[j0] = True
            row_id = owner[j0]
            row = cost[row_id-1]
            potential = u[row_id]
            delta, j1 = 10**9, 0
            for j in range(1, n+1):
                if not used[j]:
                    value = row[j-1]-potential-v[j]
                    if value < minimum[j]:
                        minimum[j], way[j] = value, j0
                    if minimum[j] < delta:
                        delta, j1 = minimum[j], j
            for j in range(n+1):
                if used[j]:
                    u[owner[j]] += delta
                    v[j] -= delta
                else:
                    minimum[j] -= delta
            j0 = j1
            if owner[j0] == 0:
                break
        while j0:
            j1 = way[j0]
            owner[j0] = owner[j1]
            j0 = j1
    result = [0]*n
    for j in range(1, n+1):
        result[owner[j]-1] = j-1
    return result


def geometry(n, d):
    indices, ops = [], []
    for x in range(n-d+1):
        for y in range(n-d+1):
            for r in range(4):
                patch = []
                for u in range(d):
                    for v in range(d):
                        p, q = ((u, v), (v, d-1-u), (d-1-u, d-1-v), (d-1-v, u))[r]
                        patch.append((x+p)*n+y+q)
                indices.append(tuple(patch))
                ops.append((x, y, r))
    return indices, ops


def apply(state, aid, indices, nn):
    for j, p in enumerate(indices[aid]):
        state[p], state[nn+j] = state[nn+j], state[p]


def layer(prefix, wanted, patches, frames, budget, indices, nn, penalties=(0, 2, 4), free_rotations=False):
    """Optimize a stamp-neutral layer; return legal actions and exact objective."""
    baseline = sum(a == b for a, b in zip(prefix, wanted))
    if budget < (2 if free_rotations else 3) or not patches:
        return [], baseline
    aids = [a+r for a, r in zip(patches, frames)]
    outgoing = [[prefix[p] for p in indices[a]] for a in aids]
    desired = [[wanted[p] for p in indices[a]] for a in aids]
    count = len(aids)
    scores = [[sum(a == b for a, b in zip(source, goal)) for goal in desired] for source in outgoing]
    keep = [scores[i][i] for i in range(count)]
    rotations = None
    if free_rotations:
        # Closed cycles affect the buffer only by rotation. Its colors are never
        # left on the board, so this mode requires unconstrained stamp wishes.
        assert all(v == 6 for v in wanted[nn:])
        outgoing = [[prefix[p] for p in indices[a]] for a in patches]
        desired = [[[wanted[p] for p in indices[a+r]] for r in range(4)] for a in patches]
        scores, rotations = [], []
        for source in outgoing:
            row, angles = [], []
            for goals in desired:
                options = [sum(a == b for a, b in zip(source, goal)) for goal in goals]
                angle = max(range(4), key=options.__getitem__)
                row.append(options[angle])
                angles.append(angle)
            scores.append(row)
            rotations.append(angles)
        keep = [sum(a == b for a, b in zip(source, desired[i][0])) for i, source in enumerate(outgoing)]
    best, best_score = [], baseline
    for penalty in penalties:
        permutation = hungarian([[-4*scores[i][j]+penalty*(i != j or free_rotations and rotations[i][j] != 0) for j in range(count)] for i in range(count)])
        visited = set()
        cycles = []
        for start in range(count):
            if start in visited:
                continue
            nodes = []
            p = start
            while p not in visited:
                visited.add(p)
                nodes.append(p)
                p = permutation[p]
            if len(nodes) < 2 and not free_rotations:
                continue
            gain = sum(scores[p][permutation[p]]-keep[p] for p in nodes)
            if gain > 0 and len(nodes)+1 <= budget:
                cycles.append((nodes, gain))
        values = [-1]*(budget+1)
        masks = [0]*(budget+1)
        values[0] = 0
        for i, (nodes, gain) in enumerate(cycles):
            cost = len(nodes)+1
            for used in range(budget, cost-1, -1):
                if values[used-cost] >= 0 and values[used-cost]+gain > values[used]:
                    values[used] = values[used-cost]+gain
                    masks[used] = masks[used-cost] | (1 << i)
        used = max(range(budget+1), key=lambda amount: (values[amount], -amount))
        if baseline+values[used] <= best_score:
            continue
        path = []
        for i, (nodes, _) in enumerate(cycles):
            if masks[used] >> i & 1:
                if free_rotations:
                    path.append(patches[nodes[0]])
                    theta = 0
                    for source, destination in zip(nodes, nodes[1:]+nodes[:1]):
                        angle = (rotations[source][destination]-theta) % 4
                        path.append(patches[destination]+angle)
                        theta = -angle % 4
                else:
                    path.append(aids[nodes[0]])
                    path.extend(aids[p] for p in nodes[1:])
                    path.append(aids[nodes[0]])
        actual = prefix[:]
        for aid in path:
            apply(actual, aid, indices, nn)
        score = sum(a == b for a, b in zip(actual, wanted))
        assert sorted(actual[nn:]) == sorted(prefix[nn:]) if free_rotations else actual[nn:] == prefix[nn:]
        assert len(path) == used and score == baseline+values[used]
        best, best_score = path, score
    return best, best_score


def improve(n, d, c, k, grid, target, stamp, reference=(), rounds=3, starts=2, density=1.25, free_rotations=False):
    nn, dd = n*n, d*d
    if k < 8 or n == d or k*dd < density*nn:
        return list(reference)
    indices, ops = geometry(n, d)
    side = n-d+1
    initial = grid+stamp
    final_wishes = target+[6]*dd
    best = [(x*side+y)*4+r for x, y, r in reference]

    def state_after(path, source=initial):
        state = source[:]
        for aid in path:
            apply(state, aid, indices, nn)
        return state

    best_score = sum(a == b for a, b in zip(state_after(best), final_wishes))
    bound = sum(min(initial.count(v), target.count(v)) for v in range(c))
    if best_score == bound:
        return list(reference)
    seed = sum((i+151)*v for i, v in enumerate(initial+target))+k*22343
    rng = random.Random(seed)
    for restart in range(starts):
        offsets = [(0, 0), (max(1, d//2), max(1, d//2))]
        if restart % 2:
            offsets.reverse()
        patches = [[(x*side+y)*4 for x in range(ox, side, d) for y in range(oy, side, d)] for ox, oy in offsets]
        if free_rotations and restart:
            for row in patches:
                rng.shuffle(row)
        paths = [[], []]
        frames = [[0]*len(row) if restart == 0 else [rng.randrange(4) for _ in row] for row in patches]
        for iteration in range(rounds):
            for slot in range(2):
                prefix = state_after(paths[0]) if slot else initial[:]
                wanted = final_wishes[:]
                if slot == 0:
                    for aid in reversed(paths[1]):
                        apply(wanted, aid, indices, nn)
                budget = k-len(paths[1-slot])
                if iteration == 0:
                    budget = min(budget, k//2 if slot == 0 else k-k//2)
                if iteration:
                    frames[slot] = [rng.randrange(4) if rng.random() < .35 else r for r in frames[slot]]
                candidate, score = layer(prefix, wanted, patches[slot], frames[slot], budget, indices, nn, free_rotations=free_rotations)
                incumbent = sum(a == b for a, b in zip(state_after(paths[slot], prefix), wanted))
                if score >= incumbent:
                    paths[slot] = candidate
                path = paths[0]+paths[1]
                actual = sum(a == b for a, b in zip(state_after(path), final_wishes))
                assert len(path) <= k
                if actual > best_score:
                    best, best_score = path[:], actual
                    if actual == bound:
                        return [ops[a] for a in best]
    return [ops[a] for a in best]


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n, d, c, k = data[:4]
    nn = n*n
    result = improve(n, d, c, k, data[4:4+nn], data[4+nn:4+2*nn], data[4+2*nn:])
    print(len(result))
    for operation in result:
        print(*operation)


if __name__ == '__main__':
    main()
