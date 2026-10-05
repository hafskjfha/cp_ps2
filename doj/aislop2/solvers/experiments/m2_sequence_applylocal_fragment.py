def m2_local_apply(self, action, wishes=False):
    if wishes:
        grid, stamp, bits, opposite = (self.wishes, self.wstamp, self.goals, self.grid)
    else:
        grid, stamp, bits, opposite = (self.grid, self.stamp, self.values, self.wishes)
    planes, cover_bits = self.old_planes, self.cover_bits
    if self.dd == 4:
        r0,r1,r2,r3=bits
        p0,p1,p2,p3=self.positions
        for j, p in enumerate(self.actions[action][0]):
            old, new = (grid[p], stamp[j])
            if old != new:
                mask=p0[p];r0[old]^=mask;r0[new]^=mask
                mask=p1[p];r1[old]^=mask;r1[new]^=mask
                mask=p2[p];r2[old]^=mask;r2[new]^=mask
                mask=p3[p];r3[old]^=mask;r3[new]^=mask
                delta = (new == opposite[p]) - (old == opposite[p])
                if delta:
                    carry = cover_bits[p]
                    plane = 0
                    if delta > 0:
                        while carry:
                            previous = planes[plane]
                            planes[plane] = previous ^ carry
                            carry &= ~previous
                            plane += 1
                    else:
                        while carry:
                            previous = planes[plane]
                            planes[plane] = previous ^ carry
                            carry &= previous
                            plane += 1
                stamp[j], grid[p] = (old, new)
    else:
        r0,r1,r2,r3,r4,r5,r6,r7,r8=bits
        p0,p1,p2,p3,p4,p5,p6,p7,p8=self.positions
        for j, p in enumerate(self.actions[action][0]):
            old, new = (grid[p], stamp[j])
            if old != new:
                mask=p0[p];r0[old]^=mask;r0[new]^=mask
                mask=p1[p];r1[old]^=mask;r1[new]^=mask
                mask=p2[p];r2[old]^=mask;r2[new]^=mask
                mask=p3[p];r3[old]^=mask;r3[new]^=mask
                mask=p4[p];r4[old]^=mask;r4[new]^=mask
                mask=p5[p];r5[old]^=mask;r5[new]^=mask
                mask=p6[p];r6[old]^=mask;r6[new]^=mask
                mask=p7[p];r7[old]^=mask;r7[new]^=mask
                mask=p8[p];r8[old]^=mask;r8[new]^=mask
                delta = (new == opposite[p]) - (old == opposite[p])
                if delta:
                    carry = cover_bits[p]
                    plane = 0
                    if delta > 0:
                        while carry:
                            previous = planes[plane]
                            planes[plane] = previous ^ carry
                            carry &= ~previous
                            plane += 1
                    else:
                        while carry:
                            previous = planes[plane]
                            planes[plane] = previous ^ carry
                            carry &= previous
                            plane += 1
                stamp[j], grid[p] = (old, new)
