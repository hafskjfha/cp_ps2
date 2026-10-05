"""Diagnostic construction beam with residual-shape and demand potentials."""
import random


def diverse_choices(state,rng,branch):
    planes=[0]*5
    for j,color in enumerate(state.stamp):
        carry=state.target_bits[j][color];plane=0
        while carry:
            old=planes[plane];planes[plane]=old^carry;carry&=old;plane+=1
    carry=0
    for plane in range(4):
        a,b=planes[plane],state.old_planes[plane]
        diff=a^b;planes[plane]=diff^carry;carry=a&b|diff&carry
    planes[4]=carry
    remaining=state.all_actions;out=[];count=len(state.actions);seen={};top=None
    while len(out)<branch and remaining:
        candidates,value=remaining,0
        for plane in range(4,-1,-1):
            hits=candidates&planes[plane]
            if hits:candidates=hits;value|=1<<plane
        if top is None:top=value
        if value<top-3:break
        remaining^=candidates
        take=min(branch-len(out),max(2,branch//4))
        while candidates and take:
            offset=rng.randrange(count);after=candidates>>offset
            rank=(after&-after).bit_length()-1+offset if after else (candidates&-candidates).bit_length()-1
            candidates^=1<<rank;aid=state.order[rank]
            outgoing=tuple(state.grid[p] for p in state.actions[aid][0])
            if seen.get(outgoing,0)>=2:continue
            seen[outgoing]=seen.get(outgoing,0)+1
            out.append((aid,value-state.size));take-=1
    return out


def construct(m, n, d, c, k, grid, target, stamp, mode=1, width=24,
              branch=8, strength=0.15, seed=0):
    if k < 3 or n == d:
        return []
    base = sum(a == b for a, b in zip(grid, target))
    upper = m.color_bound(grid + stamp, target)
    if base == upper:
        return []
    initial = m.State(n, d, c, grid[:], target, stamp[:])
    state_seed = sum((i + 51) * v for i, v in enumerate(grid + stamp)) + k * 917
    rng = random.Random(state_seed + seed * 98879)
    if mode == 1:
        weights = [max(0, d - min(p // n, p % n, n-1-p//n, n-1-p%n)) for p in range(n*n)]
    elif mode == 3:
        supply = [0] * c
        demand = [0] * c
        for value in grid + stamp:
            supply[value] += 1
        for value in target:
            demand[value] += 1
        weights = [demand[v] / max(1, supply[v]) for v in target]
    else:
        weights = [1] * (n*n)
    edges = [[] for _ in grid]
    for p in range(n*n):
        if p % n:
            edges[p].append((p-1, p))
        if p // n:
            edges[p].append((p-n, p))
        if p % n < n-1:
            edges[p].append((p, p+1))
        if p // n < n-1:
            edges[p].append((p, p+n))
    action_edges = [set(e for p in positions for e in edges[p]) for positions in initial.regions]
    def aux_value(state):
        if mode == 2:
            return sum(state.grid[a] != target[a] and state.grid[b] != target[b]
                       for a in range(n*n) for b in (a+1,a+n)
                       if b < n*n and (b == a+n or a//n == b//n))
        return sum(w for p,w in enumerate(weights) if state.grid[p] == target[p])
    beam = [(initial, [], aux_value(initial))]
    best, best_score = [], base
    for depth in range(k):
        candidates, seen = [], set()
        for parent_id,(state, path, auxiliary) in enumerate(beam):
            for aid,gain in (diverse_choices if mode==4 else m.million_choices)(state, rng, branch):
                if path and aid == path[-1]:
                    continue
                child = m.clone_state(state)
                child.apply(aid)
                key = bytes(child.grid + child.stamp)
                if key in seen:
                    continue
                seen.add(key)
                if mode == 2:
                    change = sum((child.grid[a] != target[a] and child.grid[b] != target[b]) -
                                 (state.grid[a] != target[a] and state.grid[b] != target[b])
                                 for a,b in action_edges[aid >> 2])
                else:
                    change = sum(weights[p] * ((child.grid[p] == target[p]) - (state.grid[p] == target[p]))
                                 for p in state.actions[aid][0])
                new_auxiliary = auxiliary + change
                path2 = path + [aid]
                if child.matches > best_score:
                    best_score, best = child.matches, path2
                if best_score == upper:
                    return best
                future = max(0, child.best()[0]) if depth+1 < k else 0
                priority = child.matches + 0.5*future + strength*new_auxiliary
                candidates.append((priority, rng.random(), child, path2, new_auxiliary,parent_id))
        if not candidates:
            break
        candidates.sort(key=lambda row: (row[0], row[1]), reverse=True)
        beam, stamp_counts, deferred = [], {}, []
        parent_counts={}
        for _, _, state, path, auxiliary,parent_id in candidates:
            sig = tuple(state.stamp)
            if stamp_counts.get(sig,0) >= max(2,width//4) or (mode==6 and parent_counts.get(parent_id,0)>=2):
                deferred.append((state,path,auxiliary))
                continue
            stamp_counts[sig] = stamp_counts.get(sig,0)+1
            parent_counts[parent_id]=parent_counts.get(parent_id,0)+1
            beam.append((state,path,auxiliary))
            if len(beam) >= width:
                break
        if len(beam) < width:
            beam.extend(deferred[:width-len(beam)])
    indices, _, ops, _, _ = m.build(n,d,target)
    actions = list(zip(indices,ops))
    initial_grid = grid + stamp
    best = m.refine(n,d,k,initial_grid,target,actions,best,passes=6)
    best = m.pair_sweep(n,d,k,initial_grid,target,actions,best,passes=2,width=24)
    return best
