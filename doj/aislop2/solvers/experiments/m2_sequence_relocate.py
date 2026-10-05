"""Research helper: exact all-position relocation of short operation blocks."""


def relocate_refine(n, d, c, k, initial, target, indices, sequence, module,
                    rounds=2, blocks=(1, 2, 3), passes=1, reverse=True):
    nn, dd = n*n, d*d
    width = n-d+1
    pairs = [tuple((p, nn+j) for j, p in enumerate(idx)) for idx in indices]
    upper = sum(min(initial.count(v), target.count(v)) for v in range(c))
    path = list(sequence)

    def apply(row, action):
        for p, q in pairs[action]:
            row[p], row[q] = row[q], row[p]

    def snapshots():
        prefix = [bytearray(initial)]
        for aid in path:
            row = prefix[-1][:]
            apply(row, aid)
            prefix.append(row)
        wishes = [None]*(len(path)+1)
        wishes[-1] = bytearray(target+[6]*dd)
        for pos in range(len(path)-1, -1, -1):
            row = wishes[pos+1][:]
            apply(row, path[pos])
            wishes[pos] = row
        score = sum(a == b for a,b in zip(prefix[-1], target))
        return prefix, wishes, score

    def block_delta(row, want, block):
        gain = 0
        for aid in block:
            for p,q in pairs[aid]:
                a,b = row[p],row[q]
                u,v = want[p],want[q]
                gain += (b == u)+(a == v)-(a == u)-(b == v)
                row[p],row[q] = b,a
        for aid in reversed(block):
            apply(row, aid)
        return gain

    prefix,wishes,score = snapshots()
    if score == upper or len(path) < 2:
        return path
    for iteration in range(rounds):
        best_gain, best = 0, None
        size = len(path)
        for length in blocks:
            if length >= size:
                continue
            for left in range(size-length+1):
                right = left+length
                original = path[left:right]
                variants = [original]
                if reverse and length > 1 and original != original[::-1]:
                    variants.append(original[::-1])
                deletion = -block_delta(prefix[left], wishes[right], original)
                row = prefix[left][:]
                for pos in range(right, size+1):
                    for block in variants:
                        gain = deletion+block_delta(row, wishes[pos], block)
                        if gain > best_gain:
                            best_gain,best = gain,(left,right,pos,block)
                    if pos < size:
                        apply(row,path[pos])
                want = wishes[right][:]
                for pos in range(left-1,-1,-1):
                    apply(want,path[pos])
                    for block in variants:
                        gain = deletion+block_delta(prefix[pos],want,block)
                        if gain > best_gain:
                            best_gain,best = gain,(left,right,pos,block)
        if best is None:
            break
        left,right,pos,block = best
        if pos >= right:
            path = path[:left]+path[right:pos]+block+path[pos:]
        else:
            path = path[:pos]+block+path[pos:left]+path[right:]
        old_score = score
        prefix,wishes,score = snapshots()
        assert score == old_score+best_gain,(score,old_score,best_gain)
        if score == upper:
            break
    if passes:
        ops = [(a//4//width,a//4%width,a%4) for a in range(len(indices))]
        path = module['refine'](n,d,k,initial,target,list(zip(indices,ops)),path,
                                passes=passes,seed_offset=127801)
    return path
