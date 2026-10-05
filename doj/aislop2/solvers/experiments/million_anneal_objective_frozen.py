import random

def objective_walk(n, d, c, k, initial, target, indices, sequence, refine, weighted_refine, actions, trials=12, mode=0, passes=3):
    if k < 4:
        return sequence
    nn = n * n
    upper = sum((min(initial.count(v), target.count(v)) for v in range(c)))

    def evaluate(path):
        row = initial[:]
        for aid in path:
            for j, p in enumerate(indices[aid]):
                row[p], row[nn + j] = (row[nn + j], row[p])
        return (sum((a == b for a, b in zip(row, target))), row)
    best = sequence[:]
    best_score, final = evaluate(best)
    if best_score == upper:
        return best
    current = best[:]
    rng = random.Random(sum(((i + 101) * v for i, v in enumerate(initial))) + k * 2381)
    for trial in range(trials):
        rate = (0.08, 0.15, 0.3, 0.5)[trial % 4]
        weights = [1 + (rng.random() < rate) for _ in range(nn)]
        candidate = weighted_refine(n, d, k, initial, target, weights, actions, current, passes=1)
        candidate = refine(n, d, k, initial, target, actions, candidate, passes=passes, seed_offset=trial * 17981 + 80311)
        value, row = evaluate(candidate)
        if value >= best_score:
            best, best_score, final = (candidate[:], value, row)
            if value == upper:
                break
        current = candidate if value >= best_score - 1 else best[:]
        if trial % 4 == 3:
            current = best[:]
    return best
