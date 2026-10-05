import random
def construct(m, n, d, c, k, grid, target, stamp, width=48, branch=6, strength=0, seed=0, mode=4):
    nn = n * n
    indices, _, ops, _, _ = m.build(n, d, target)
    actions = list(zip(indices, ops))
    initial = grid + stamp
    engine = m.FastBack(n, d, grid, target, stamp, indices)
    base = sum((a == b for a, b in zip(grid, target)))
    upper = m.color_bound(initial, target)
    beam = [(engine.first, [], base)]
    finalists=[]
    future_weight=3
    best, bestscore = ([], base)
    rng = random.Random(sum(((i + 83) * v for i, v in enumerate(initial))) + k * 1709)
    for depth in range(k):
        candidates = []
        seen = set()
        for state, path, score in beam:
            for aid, gain in engine.choices(state, rng, branch):
                if path and aid == path[-1]:
                    continue
                child = engine.apply(state, aid)
                key = bytes(child[0] + child[1])
                if key in seen:
                    continue
                seen.add(key)
                path2 = path + [aid]
                value = score + gain
                if value > bestscore:
                    best, bestscore = (path2, value)
                if value == upper:
                    return [ops[x] for x in reversed(best)]
                future = max(0, engine.best(child)) if future_weight and depth + 1 < k else 0
                candidates.append((value * 8 + future_weight * future, rng.random(), child, path2, value))
        if not candidates:
            break
        candidates.sort(key=lambda row: row[:2], reverse=True)
        beam = [(child, path, value) for _, _, child, path, value in candidates[:width]]
        if depth >= k-4:finalists.extend((value,path) for _,path,value in beam)
    path = list(reversed(best))
    path = m.refine(n, d, k, initial, target, actions, path, passes=6)
    path = m.pair_sweep(n, d, k, initial, target, actions, path, passes=2, width=24)
    def score(seq):
        final=initial[:]
        for aid in seq:m._st(final,nn,indices[aid])
        return sum(a==b for a,b in zip(final,target))
    result=path;bestvalue=score(path);selected=[best]
    pool=[row for row in finalists if row[0]>=bestscore-2]
    trials=2 if n>=24 and k>=120 else mode
    for _ in range(trials):
        if not pool:break
        _,candidate=max(pool,key=lambda row:(min(sum(a!=b for a,b in zip(row[1],old))+abs(len(row[1])-len(old))for old in selected),row[0]))
        selected.append(candidate);pool=[row for row in pool if row[1]!=candidate]
        candidate=list(reversed(candidate))
        candidate=m.refine(n,d,k,initial,target,actions,candidate,passes=6)
        candidate=m.pair_sweep(n,d,k,initial,target,actions,candidate,passes=2,width=24)
        value=score(candidate)
        if value>bestvalue:result,bestvalue=candidate,value
    return [ops[x]for x in result]
