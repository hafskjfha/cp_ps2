"""Select uniformly among tied actions instead of weighting preceding gaps."""
_M2_LOWER_MASKS = [(1 << (1 << i)) - 1 for i in range(13)]


def m2_uniform_pick(candidates, rng):
    count = candidates.bit_count()
    ordinal = rng.randrange(count)
    if ordinal == count - 1:
        return candidates.bit_length() - 1
    offset = 0
    while ordinal:
        level = (candidates.bit_length() - 1).bit_length() - 1
        step = 1 << level
        low = candidates & _M2_LOWER_MASKS[level]
        count = low.bit_count()
        if ordinal < count:
            candidates = low
        else:
            candidates >>= step
            offset += step
            ordinal -= count
    return offset + (candidates & -candidates).bit_length() - 1
