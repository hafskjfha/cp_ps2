"""Experimental basin-hopping through exact coordinate refinement."""
import random


def improve(m, n, d, c, k, grid, target, stamp, reference, trials=24, passes=2):
    if k < 3 or n == d:
        return reference
    initial = grid + stamp
    indices, _, operations, _, _ = m.build(n, d, target)
    actions = list(zip(indices, operations))
    side = n-d+1
    nn = n*n
    best = [(x*side+y)*4+r for x,y,r in reference]
    def score(sequence):
        state = initial[:]
        for aid in sequence:
            if aid >= 0:
                m._st(state, nn, indices[aid])
        return sum(a == b for a,b in zip(state, target))
    best_score = score(best)
    upper = m.color_bound(initial, target)
    if best_score == upper:
        return reference
    rng = random.Random(sum((p+137)*v for p,v in enumerate(initial+target)) + k*911)
    current, current_score = best[:], best_score
    for trial in range(trials):
        candidate = current[:] + [-1]*min(8,k-len(current))
        if not candidate:
            candidate = [-1]*min(k,8)
        strength = (2,3,4,6,8,12)[trial % 6]
        positions = rng.sample(range(len(candidate)), min(strength,len(candidate)))
        for p in positions:
            old = candidate[p]
            mode = rng.randrange(5)
            if mode <= 1 and old >= 0:
                x,y,r = operations[old]
                x = max(0,min(side-1,x+rng.randrange(-2,3)))
                y = max(0,min(side-1,y+rng.randrange(-2,3)))
                candidate[p] = (x*side+y)*4 + rng.randrange(4)
            elif mode == 2:
                candidate[p] = -1
            else:
                candidate[p] = rng.randrange(len(actions))
        candidate = m.refine(n,d,k,initial,target,actions,candidate,passes=passes,seed_offset=7919*(trial+1))
        value = score(candidate)
        if value >= current_score or (trial % 9 == 8 and value >= best_score-2):
            current,current_score = candidate,value
        if value > best_score:
            best,best_score = candidate[:],value
            if value == upper:
                break
        if trial % 12 == 11:
            current,current_score = best[:],best_score
    return [operations[aid] for aid in best]
