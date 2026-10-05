"""Exact packed spatial gathers for refinement-state initialization."""

_M2_SPATIAL={}
_M2_COLOR_TABLES=[bytes(1 if value==color else 0 for value in range(256)) for color in range(7)]
_M2_COLOR_TABLES_HIGH=[bytes(16 if value==color else 0 for value in range(256)) for color in range(7)]


def m2_pack_colors(grid):
    data=bytes(grid);even,odd=data[::2],data[1::2]
    return [int.from_bytes(even.translate(table),'little')|int.from_bytes(odd.translate(high),'little')
            for table,high in zip(_M2_COLOR_TABLES,_M2_COLOR_TABLES_HIGH)]


def m2_spatial(n,d):
    key=n,d
    geometry=_M2_SPATIAL.get(key)
    if geometry is not None:return geometry
    side=n-d+1
    span=1<<(side-1).bit_length()
    full=(1<<(4*n*span))-1
    joins=[];block=1
    while block<span:
        mask=full//((1<<(8*n*block))-1)*((1<<(4*side*block))-1)
        joins.append((4*(d-1)*block,mask,mask<<(4*side*block)))
        block*=2
    anchors=sum(1<<(4*(x*n+y)) for x in range(side) for y in range(side))
    low=sum(1<<(4*p) for p in range(side*side))
    shifts=[4*(u*n+v) for u in range(d) for v in range(d)]
    rotations=[]
    for u in range(d):
        for v in range(d):
            rotations.append([u*d+v,v*d+d-1-u,(d-1-u)*d+d-1-v,(d-1-v)*d+u])
    geometry=anchors,low,joins,shifts,rotations
    _M2_SPATIAL[key]=geometry
    return geometry


def m2_compact(value,anchors,joins):
    value&=anchors
    for shift,lower,upper in joins:value=(value&lower)|((value>>shift)&upper)
    return value


def m2_value_bits(n,d,grid):
    anchors,low,joins,shifts,rotations=m2_spatial(n,d)
    packed=m2_pack_colors(grid)
    compacts=[]
    for shift in shifts:
        compacts.append([m2_compact(value>>shift,anchors,joins) if value else 0 for value in packed])
    values=[]
    for a,b,c,e in rotations:
        aa,bb,cc,ee=compacts[a],compacts[b],compacts[c],compacts[e]
        values.append([aa[color]|bb[color]<<1|cc[color]<<2|ee[color]<<3 for color in range(7)])
    return values


def m2_old_planes(n,d,grid,wishes):
    anchors,low,joins,shifts,rotations=m2_spatial(n,d)
    a,b=m2_pack_colors(grid),m2_pack_colors(wishes)
    mismatch=0
    for value,want in zip(a,b):mismatch|=value&~want
    counts=sum(m2_compact(mismatch>>shift,anchors,joins) for shift in shifts)
    return [((counts>>plane)&low)*15 for plane in range(4)]+[0]


def m2_refine_init(self,n,d,initial,target,actions,order):
    nn,dd=n*n,d*d
    self.nn,self.dd=nn,dd
    self.grid,self.stamp=initial[:nn],initial[nn:]
    self.wishes,self.wstamp=target[:],[6]*dd
    self.actions,self.order=actions,order
    size=len(actions);self.all_bits=(1<<size)-1
    key=n,d
    geometry=_REFINE_GEOMETRY.get(key)
    if geometry is None:
        positions=[[0]*nn for _ in range(dd)]
        region_bits=[15<<4*r for r in range(size//4)]
        regions=[actions[i][0] for i in range(0,size,4)]
        cover=[[] for _ in range(nn)]
        for r,patch in enumerate(regions):
            for p in patch:cover[p].append(r)
        for aid,(patch,_) in enumerate(actions):
            bit=1<<aid
            for j,p in enumerate(patch):positions[j][p]|=bit
        geometry=positions,region_bits,regions,cover
        _REFINE_GEOMETRY[key]=geometry
    self.positions,self.region_bits,self.regions,self.cover=geometry
    cover_bits=_REFINE_COVER_BITS.get(key)
    if cover_bits is None:
        cover_bits=[sum(self.region_bits[r] for r in ids) for ids in self.cover]
        _REFINE_COVER_BITS[key]=cover_bits
    self.cover_bits=cover_bits
    self.values=m2_value_bits(n,d,self.grid)
    goal_key=n,d,tuple(target)
    cached_goals=_REFINE_GOALS.get(goal_key)
    if cached_goals is None:
        cached_goals=m2_value_bits(n,d,target)
        _REFINE_GOALS[goal_key]=cached_goals
    self.goals=[row[:] for row in cached_goals]
    self.tie_masks=m2_tie_masks(order) if order else [0]*size.bit_length()
    self.old_planes=m2_old_planes(n,d,self.grid,self.wishes)
    self.counts=None
