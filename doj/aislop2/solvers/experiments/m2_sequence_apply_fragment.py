"""Exact transposed-geometry updates for refinement bit masks."""

_M2_POSITION_COLUMNS={}


def m2_column_apply(self,action,wishes=False):
    if wishes:
        grid,stamp,bits,opposite=self.wishes,self.wstamp,self.goals,self.grid
    else:
        grid,stamp,bits,opposite=self.grid,self.stamp,self.values,self.wishes
    key=self.nn,self.dd
    columns=_M2_POSITION_COLUMNS.get(key)
    if columns is None:
        columns=list(zip(*self.positions))
        _M2_POSITION_COLUMNS[key]=columns
    planes,cover_bits=self.old_planes,self.cover_bits
    for j,p in enumerate(self.actions[action][0]):
        old,new=grid[p],stamp[j]
        if old!=new:
            for row,mask in zip(bits,columns[p]):
                row[old]^=mask;row[new]^=mask
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
