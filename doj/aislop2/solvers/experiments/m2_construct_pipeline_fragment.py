def m2_quotient_construct(n, d, c, k, grid, target, stamp):
    nn = n * n
    indices, _, ops, _, _ = build(n, d, target)
    initial = ClusterState(n, d, c, grid[:], target, stamp[:])
    upper = color_bound(grid + stamp, target)
    rotations = []
    for r in range(4):
        rotations.append([((u, v), (v, d - 1 - u), (d - 1 - u, d - 1 - v), (d - 1 - v, u))[r][0] * d + ((u, v), (v, d - 1 - u), (d - 1 - u, d - 1 - v), (d - 1 - v, u))[r][1] for u in range(d) for v in range(d)])
    beam = [(initial, [])]
    best = []
    bestscore = initial.matches
    finalists = []
    rng = random.Random(sum(((i + 51) * v for i, v in enumerate(grid + stamp))) + k * 917 + 0 * 941)
    for depth in range(k):
        candidates = []
        seen = set()
        for state, path in beam:
            choices = million_choices(state, rng, 6)
            for aid, gain in choices:
                if path and aid == path[-1]:
                    continue
                child = clone_cluster_state(state)
                child.apply(aid)
                stampkey = min((bytes((child.stamp[p] for p in rotation)) for rotation in rotations))
                key = bytes(child.grid) + stampkey
                if key in seen:
                    continue
                seen.add(key)
                p2 = path + [aid]
                if child.matches > bestscore:
                    best, bestscore = (p2, child.matches)
                if bestscore == upper:
                    return [ops[x] for x in best]
                future = max(0, child.best()[0]) if depth + 1 < k else 0
                potential = 0
                priority = child.matches + 0.5 * future + 0 * potential
                candidates.append((priority, rng.random(), child, p2))
        if not candidates:
            break
        candidates.sort(key=lambda row: row[:2], reverse=True)
        beam = []
        counts = {}
        deferred = []
        for _, _, child, path in candidates:
            sig = tuple(child.stamp)
            if counts.get(sig, 0) >= max(2, 64 // 4):
                deferred.append((child, path))
                continue
            counts[sig] = counts.get(sig, 0) + 1
            beam.append((child, path))
            if len(beam) >= 64:
                break
        if len(beam) < 64:
            beam.extend(deferred[:64 - len(beam)])
    path = best
    actions = list(zip(indices, ops))
    path = refine(n, d, k, grid + stamp, target, actions, path, passes=6)
    path = pair_sweep(n, d, k, grid + stamp, target, actions, path, passes=2, width=24)
    return [ops[x] for x in path]

_m2_constructor_previous_retained=solve_retained_iterated
_m2_constructor_previous_beam=million_beam
_m2_constructor_domain_cache=None

def m2_constructor_domain(n,d,c,k,grid,target,stamp):
    global _m2_constructor_domain_cache
    if n<10 or k<12:return False
    key=(n,d,c,k,tuple(grid),tuple(target),tuple(stamp))
    if _m2_constructor_domain_cache is not None and _m2_constructor_domain_cache[0]==key:
        return _m2_constructor_domain_cache[1]
    result=False
    if 100*sum(a==b for a,b in zip(grid,target))<70*color_bound(grid+stamp,target):
        patterns=set()
        for x in range(n-d+1):
            for y in range(n-d+1):
                patterns.add(tuple(target[(x+i)*n+y+j]for i in range(d)for j in range(d)))
                if len(patterns)>4*c:result=True;break
            if result:break
    _m2_constructor_domain_cache=(key,result)
    return result

def solve_retained_iterated(n,d,c,k,grid,target,stamp):
    if not m2_constructor_domain(n,d,c,k,grid,target,stamp):
        return _m2_constructor_previous_retained(n,d,c,k,grid,target,stamp)
    result=m2_quotient_construct(n,d,c,k,grid,target,stamp)
    return cluster_improve(n,d,c,k,grid,target,stamp,result,width=16)

def million_beam(n,d,c,k,grid,target,stamp,reference,width=12,branch=6,future_weight=4,enhance=False):
    if m2_constructor_domain(n,d,c,k,grid,target,stamp):return reference
    return _m2_constructor_previous_beam(n,d,c,k,grid,target,stamp,reference,width,branch,future_weight,enhance)
