"""Exact-output-preserving grouped geometry updates for refinement states."""

_M2_GROUP_GEOMETRY={}


def m2_group_apply(self,action,wishes=False):
    if wishes:
        grid,stamp,bits,opposite=self.wishes,self.wstamp,self.goals,self.grid
    else:
        grid,stamp,bits,opposite=self.grid,self.stamp,self.values,self.wishes
    patch=self.actions[action][0]
    changed=[0]*7
    planes,cover_bits=self.old_planes,self.cover_bits
    for j,p in enumerate(patch):
        old,new=grid[p],stamp[j]
        if old!=new:
            bit=1<<j
            changed[old]^=bit;changed[new]^=bit
            delta=(new==opposite[p])-(old==opposite[p])
            if delta:
                carry=cover_bits[p];plane=0
                if delta>0:
                    while carry:
                        previous=planes[plane];planes[plane]=previous^carry
                        carry&=~previous;plane+=1
                else:
                    while carry:
                        previous=planes[plane];planes[plane]=previous^carry
                        carry&=previous;plane+=1
            stamp[j],grid[p]=old,new
    geometry_key=self.nn,self.dd
    geometry=_M2_GROUP_GEOMETRY.get(geometry_key)
    if geometry is None:
        geometry=[{} for _ in self.actions]
        _M2_GROUP_GEOMETRY[geometry_key]=geometry
    cache=geometry[action]
    positions=self.positions
    for color,subset in enumerate(changed):
        if not subset:continue
        masks=cache.get(subset)
        if masks is None:
            points=[];left=subset
            while left:
                bit=left&-left;left-=bit
                points.append(patch[bit.bit_length()-1])
            masks=[]
            for row in positions:
                mask=0
                for p in points:mask|=row[p]
                masks.append(mask)
            cache[subset]=masks
        for row,mask in zip(bits,masks):row[color]^=mask
