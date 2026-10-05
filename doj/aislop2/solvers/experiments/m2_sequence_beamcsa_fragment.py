def m2_stamp_planes(bits,stamp):

    if len(stamp)==4:

        a0=bits[0][stamp[0]]

        a1=bits[1][stamp[1]]

        a2=bits[2][stamp[2]]

        a3=bits[3][stamp[3]]

        s1=a0^a1;c1=(a0&a1)|(s1&a2);s1^=a2

        s2=a3^s1;c2=a3&s1

        s3=c1^c2;c3=c1&c2

        return [s2,s3,c3,0,0]

    else:

        a0=bits[0][stamp[0]]

        a1=bits[1][stamp[1]]

        a2=bits[2][stamp[2]]

        a3=bits[3][stamp[3]]

        a4=bits[4][stamp[4]]

        a5=bits[5][stamp[5]]

        a6=bits[6][stamp[6]]

        a7=bits[7][stamp[7]]

        a8=bits[8][stamp[8]]

        s1=a0^a1;c1=(a0&a1)|(s1&a2);s1^=a2

        s2=a3^a4;c2=(a3&a4)|(s2&a5);s2^=a5

        s3=a6^a7;c3=(a6&a7)|(s3&a8);s3^=a8

        s4=s1^s2;c4=(s1&s2)|(s4&s3);s4^=s3

        s5=c1^c2;c5=(c1&c2)|(s5&c3);s5^=c3

        s6=c4^s5;c6=c4&s5

        s7=c5^c6;c7=c5&c6

        return [s4,s6,s7,c7,0]

def m2_state_best_candidates(self):
    planes=m2_stamp_planes(self.target_bits,self.stamp)
    carry = 0
    for plane in range(4):
        a, b = (planes[plane], self.old_planes[plane])
        different = a ^ b
        planes[plane] = different ^ carry
        carry = a & b | different & carry
    planes[4] = carry
    candidates, value = (self.all_actions, 0)
    for plane in range(4, -1, -1):
        hits = candidates & planes[plane]
        if hits:
            candidates = hits
            value |= 1 << plane
    return (value - self.size, candidates)


def million_choices(state, rng, branch=6):
    planes=m2_stamp_planes(state.target_bits,state.stamp)
    carry = 0
    for plane in range(4):
        a, b = (planes[plane], state.old_planes[plane])
        different = a ^ b
        planes[plane] = different ^ carry
        carry = a & b | different & carry
    planes[4] = carry
    remaining = state.all_actions
    out = []
    count = len(state.actions)
    seen = {}
    while len(out) < branch and remaining:
        candidates, value = (remaining, 0)
        for plane in range(4, -1, -1):
            hits = candidates & planes[plane]
            if hits:
                candidates = hits
                value |= 1 << plane
        remaining ^= candidates
        take = min(branch - len(out), 4)
        while candidates and take:
            offset = rng.randrange(count)
            after = candidates >> offset
            rank = (after & -after).bit_length() - 1 + offset if after else (candidates & -candidates).bit_length() - 1
            candidates ^= 1 << rank
            aid = state.order[rank]
            outgoing = tuple((state.grid[p] for p in state.actions[aid][0]))
            if seen.get(outgoing, 0) >= 2:
                continue
            seen[outgoing] = seen.get(outgoing, 0) + 1
            out.append((aid, value - state.size))
            take -= 1
        if out and value - state.size < out[0][1] - 1:
            break
    return out


def m2_fastback_scoreplanes(self,state):

    planes=m2_stamp_planes(self.columns,state[1])

    carry=0

    for plane in range(5):

        a,b=planes[plane],state[2][plane]

        different=a^b;planes[plane]=different^carry;carry=a&b|different&carry

    return planes

State.best_candidates=m2_state_best_candidates

FastBack.scoreplanes=m2_fastback_scoreplanes
