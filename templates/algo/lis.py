from bisect import *

def lis_reconstruct(a):
    n = len(a)
    tails = []
    tails_idx = []
    prev = [-1] * n

    for i, x in enumerate(a):
        # strict lis, non-decreasing -> bisect_right
        k = bisect_left(tails, x)
        
        if k == len(tails):
            tails.append(x)
            tails_idx.append(i)
        else:
            tails[k] = x
            tails_idx[k] = i
        if k > 0:
            prev[i] = tails_idx[k - 1]

    cur = tails_idx[-1]
    seq = []
    while cur != -1:
        seq.append(a[cur])
        cur = prev[cur]
    seq.reverse()
    return len(tails), seq