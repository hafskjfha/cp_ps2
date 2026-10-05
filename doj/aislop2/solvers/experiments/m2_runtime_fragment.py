"""Exact rank-mask transpose using packed 16-bit ranks and cached gathers."""
import struct

_M2_RANK_GATHERS = {}


def m2_tie_masks(order):
    size = len(order)
    ranks = [0] * size
    for rank, aid in enumerate(order):
        ranks[aid] = rank
    packed = int.from_bytes(struct.pack('<%dH' % size, *ranks), 'little')
    geometry = _M2_RANK_GATHERS.get(size)
    if geometry is None:
        span = 1 << (size - 1).bit_length()
        full = (1 << (16 * span)) - 1
        collect = full // 65535
        joins = []
        block = 1
        while block < span:
            joins.append((15 * block, full // ((1 << (32 * block)) - 1) * ((1 << (2 * block)) - 1)))
            block *= 2
        geometry = collect, joins
        _M2_RANK_GATHERS[size] = geometry
    collect, joins = geometry
    result = []
    for bit in range(size.bit_length()):
        value = (packed >> bit) & collect
        for shift, mask in joins:
            value = (value | (value >> shift)) & mask
        result.append(value)
    return result
