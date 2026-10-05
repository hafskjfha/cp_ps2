def m2_fast_million_beam(n, d, c, k, grid, target, stamp, reference, width=12, branch=6, future_weight=4, enhance=False):
    if k < 3 or n == d:
        return reference
    base = sum((a == b for a, b in zip(grid, target)))
    upper = color_bound(grid + stamp, target)
    indices, _, operations, _, _ = build(n, d, target)
    actions = list(zip(indices, operations))
    side = n - d + 1
    initial = grid + stamp

    def score(path):
        state = initial[:]
        for aid in path:
            _st(state, n * n, indices[aid])
        return sum((a == b for a, b in zip(state, target)))
    best = [(x * side + y) * 4 + r for x, y, r in reference]
    best_score = score(best)
    if best_score == upper:
        return reference
    state = ClusterState(n, d, c, grid[:], target, stamp[:])
    rng = random.Random(sum(((i + 51) * v for i, v in enumerate(grid + stamp))) + k * 917)
    beam = [(state, [])]
    beam_best, beam_score = ([], base)
    for depth in range(k):
        candidates = []
        seen = set()
        for state, path in beam:
            for aid, gain in million_choices(state, rng, branch):
                if path and aid == path[-1]:
                    continue
                child = clone_cluster_state(state)
                child.apply(aid)
                key = bytes(child.grid + child.stamp)
                if key in seen:
                    continue
                seen.add(key)
                path2 = path + [aid]
                if child.matches > beam_score:
                    beam_best, beam_score = (path2, child.matches)
                if beam_score == upper:
                    return [operations[x] for x in beam_best]
                future = max(0, child.best()[0]) if depth + 1 < k else 0
                priority = child.matches * 8 + future_weight * future
                candidates.append((priority, rng.random(), child, path2))
        if not candidates:
            break
        candidates.sort(key=lambda x: (x[0], x[1]), reverse=True)
        beam = []
        stamp_counts = {}
        deferred = []
        for _, _, state, path in candidates:
            sig = tuple(state.stamp)
            if stamp_counts.get(sig, 0) >= max(2, width // 4):
                deferred.append((state, path))
                continue
            stamp_counts[sig] = stamp_counts.get(sig, 0) + 1
            beam.append((state, path))
            if len(beam) >= width:
                break
        if len(beam) < width:
            beam.extend(deferred[:width - len(beam)])
    candidate = refine(n, d, k, initial, target, actions, beam_best, passes=6)
    candidate = pair_sweep(n, d, k, initial, target, actions, candidate, passes=2, width=24)
    if enhance:
        candidate = anneal_walk(n, d, k, initial, target, actions, candidate)
        candidate = refine(n, d, k, initial, target, actions, candidate, passes=2)
        candidate = triple_refine(n, d, k, initial, target, actions, candidate, passes=2)
        candidate = refine(n, d, k, initial, target, actions, candidate, passes=2)
    value = score(candidate)
    if value > best_score:
        best = candidate
    return [operations[x] for x in best]

_cluster_original_million_beam=m2_fast_million_beam
