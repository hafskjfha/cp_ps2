"""Exact packed weighted-region sums and refinement initialization."""

_M2_BYTE_GATHERS={}
_M2_PLANE_TABLES=[bytes(1 if value&(1<<plane) else 0 for value in range(256)) for plane in range(5)]
_M2_PLANE_TABLES_HIGH=[bytes(16 if value&(1<<plane) else 0 for value in range(256)) for plane in range(5)]
_M2_COST_TABLES={dd:bytes((2*dd-value)&255 for value in range(256)) for dd in (4,9)}


def m2_weighted_counts(n,d,grid,wishes,weights):
    key=n,d
    geometry=_M2_BYTE_GATHERS.get(key)
    side=n-d+1
    if geometry is None:
        span=1<<(side-1).bit_length()
        full=(1<<(8*n*span))-1
        anchors=sum(255<<(8*(x*n+y)) for x in range(side) for y in range(side))
        joins=[];block=1
        while block<span:
            lower=full//((1<<(16*n*block))-1)*((1<<(8*side*block))-1)
            joins.append((8*(d-1)*block,lower,lower<<(8*side*block)))
            block*=2
        shifts=[8*(u*n+v) for u in range(d) for v in range(d)]
        geometry=anchors,joins,shifts
        _M2_BYTE_GATHERS[key]=geometry
    anchors,joins,shifts=geometry
    packed=int.from_bytes(bytes(weight if a==b else 0 for a,b,weight in zip(grid,wishes,weights)),'little')
    values=sum((packed>>shift)&anchors for shift in shifts)
    for shift,lower,upper in joins:values=(values&lower)|((values>>shift)&upper)
    return list(values.to_bytes(side*side,'little'))


def m2_weighted_refine_init(self,n,d,initial,target,weights,actions,order):
    m2_refine_init(self,n,d,initial,target,actions,order)
    self.weights,self.wstamp_weights=weights[:],[0]*(d*d)
    self.weight_bits=[row[:3] for row in m2_value_bits(n,d,weights)]
    self.counts=m2_weighted_counts(n,d,self.grid,self.wishes,weights)
    costs=bytes(self.counts).translate(_M2_COST_TABLES[d*d])
    even,odd=costs[::2],costs[1::2]
    self.old_planes=[(int.from_bytes(even.translate(table),'little')|int.from_bytes(odd.translate(high),'little'))*15
                     for table,high in zip(_M2_PLANE_TABLES,_M2_PLANE_TABLES_HIGH)]+[0]
