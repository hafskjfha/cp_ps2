"""Bit-parallel replacement for the scalar best_action scan."""


def m2_best_action(state,wishes,actions,nn,dd,current=-1,allow_zero=False):
    n=int(nn**0.5);d=2 if dd==4 else 3
    grid=state[:nn];wanted=[x if x>=0 else 6 for x in wishes[:nn]]
    stamp=state[nn:];wstamp=[x if x>=0 else 6 for x in wishes[nn:]]
    values=m2_value_bits(n,d,grid);goals=m2_value_bits(n,d,wanted)
    old_planes=m2_old_planes(n,d,grid,wanted)
    planes=[0]*5
    for j in range(dd):
        for carry in (values[j][wstamp[j]],goals[j][stamp[j]]):
            plane=0
            while carry:
                old=planes[plane];planes[plane]=old^carry;carry&=old;plane+=1
    carry=0
    for plane in range(5):
        a,b=planes[plane],old_planes[plane]
        different=a^b;planes[plane]=different^carry;carry=a&b|different&carry
    candidates=(1<<len(actions))-1;value=0
    for plane in range(4,-1,-1):
        hits=candidates&planes[plane]
        if hits:candidates=hits;value|=1<<plane
    gain=value-dd-sum(a==b for a,b in zip(stamp,wstamp))
    if gain<0:return -1,0
    if current>=0 and candidates&(1<<current):return current,gain
    if not gain and not allow_zero:return -1,0
    return (candidates&-candidates).bit_length()-1,gain
