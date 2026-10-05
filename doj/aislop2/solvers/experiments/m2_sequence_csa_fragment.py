def m2_csa_best(self):
    if self.dd==4:
        values,goals,stamp,wstamp=self.values,self.goals,self.stamp,self.wstamp
        a0,a1=values[0][wstamp[0]],goals[0][stamp[0]]
        a2,a3=values[1][wstamp[1]],goals[1][stamp[1]]
        a4,a5=values[2][wstamp[2]],goals[2][stamp[2]]
        a6,a7=values[3][wstamp[3]],goals[3][stamp[3]]
        s1=a0^a1;c1=(a0&a1)|(s1&a2);s1^=a2
        s2=a3^a4;c2=(a3&a4)|(s2&a5);s2^=a5
        s3=a6^a7;c3=(a6&a7)|(s3&s1);s3^=s1
        s4=s2^s3;c4=s2&s3
        s5=c1^c2;c5=(c1&c2)|(s5&c3);s5^=c3
        s6=c4^s5;c6=c4&s5
        s7=c5^c6;c7=c5&c6
        planes=[s4,s6,s7,c7,0]
    else:
        values,goals,stamp,wstamp=self.values,self.goals,self.stamp,self.wstamp
        a0,a1=values[0][wstamp[0]],goals[0][stamp[0]]
        a2,a3=values[1][wstamp[1]],goals[1][stamp[1]]
        a4,a5=values[2][wstamp[2]],goals[2][stamp[2]]
        a6,a7=values[3][wstamp[3]],goals[3][stamp[3]]
        a8,a9=values[4][wstamp[4]],goals[4][stamp[4]]
        a10,a11=values[5][wstamp[5]],goals[5][stamp[5]]
        a12,a13=values[6][wstamp[6]],goals[6][stamp[6]]
        a14,a15=values[7][wstamp[7]],goals[7][stamp[7]]
        a16,a17=values[8][wstamp[8]],goals[8][stamp[8]]
        s1=a0^a1;c1=(a0&a1)|(s1&a2);s1^=a2
        s2=a3^a4;c2=(a3&a4)|(s2&a5);s2^=a5
        s3=a6^a7;c3=(a6&a7)|(s3&a8);s3^=a8
        s4=a9^a10;c4=(a9&a10)|(s4&a11);s4^=a11
        s5=a12^a13;c5=(a12&a13)|(s5&a14);s5^=a14
        s6=a15^a16;c6=(a15&a16)|(s6&a17);s6^=a17
        s7=s1^s2;c7=(s1&s2)|(s7&s3);s7^=s3
        s8=s4^s5;c8=(s4&s5)|(s8&s6);s8^=s6
        s9=s7^s8;c9=s7&s8
        s10=c1^c2;c10=(c1&c2)|(s10&c3);s10^=c3
        s11=c4^c5;c11=(c4&c5)|(s11&c6);s11^=c6
        s12=c7^c8;c12=(c7&c8)|(s12&c9);s12^=c9
        s13=s10^s11;c13=(s10&s11)|(s13&s12);s13^=s12
        s14=c10^c11;c14=(c10&c11)|(s14&c12);s14^=c12
        s15=c13^s14;c15=c13&s14
        s16=c14^c15;c16=c14&c15
        planes=[s9,s13,s15,s16,c16]
    carry = 0
    for plane in range(5):
        a, b = (planes[plane], self.old_planes[plane])
        different = a ^ b
        planes[plane] = different ^ carry
        carry = a & b | different & carry
    candidates, value = (self.all_bits, 0)
    for plane in range(4, -1, -1):
        hits = candidates & planes[plane]
        if hits:
            candidates = hits
            value |= 1 << plane
    gain = value - self.dd - sum((a == b for a, b in zip(self.stamp, self.wstamp)))
    if gain < 0:
        return (-1, 0)
    for mask in reversed(self.tie_masks):
        if not candidates & candidates - 1:
            break
        preferred = candidates & ~mask
        if preferred:
            candidates = preferred
    return ((candidates & -candidates).bit_length() - 1, gain)
