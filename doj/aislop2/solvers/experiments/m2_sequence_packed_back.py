"""Private five-bit-field replacement for FastBack, preserving beam choices."""


class PackedFastBack:
    __slots__=('indices','grid','stamp','dd','columns','pickup','cover','guards','first','count')

    def __init__(self,n,d,grid,target,stamp,indices):
        dd=d*d;nn=n*n
        self.indices=indices;self.grid=grid;self.stamp=stamp;self.dd=dd
        self.count=len(indices)
        self.columns=[[0]*7 for _ in range(dd)]
        self.pickup=[[0]*7 for _ in range(nn)]
        self.cover=[0]*nn
        field=0;low=0
        for aid,patch in enumerate(indices):
            bit=1<<(5*aid);low|=bit;value=dd
            for j,p in enumerate(patch):
                self.columns[j][grid[p]]|=bit
                self.pickup[p][stamp[j]]|=bit
                self.cover[p]|=bit
                value+=(target[p]==stamp[j])-(target[p]==grid[p])
            field|=value<<(5*aid)
        self.guards=low<<4
        self.first=[bytearray(target),bytearray([6])*dd,field,None,None,dd]

    def apply(self,state,aid):
        board=state[0][:];stamp=state[1][:];field=state[2]
        grid,original_stamp=self.grid,self.stamp
        pickup,cover=self.pickup,self.cover
        subtract=self.dd
        for j,p in enumerate(self.indices[aid]):
            old,new=board[p],stamp[j]
            if old!=new:
                field+=pickup[p][new]-pickup[p][old]
                delta=(new==grid[p])-(old==grid[p])
                if delta:field-=delta*cover[p]
                board[p]=new
            stamp[j]=old
            subtract+=old==original_stamp[j]
        return [board,stamp,field,None,None,subtract]

    def scorefield(self,state):
        if state[3] is not None:return state[3]
        columns=self.columns;stamp=state[1]
        if self.dd==4:
            value=state[2]+columns[0][stamp[0]]+columns[1][stamp[1]]+columns[2][stamp[2]]+columns[3][stamp[3]]
        else:
            value=(state[2]+columns[0][stamp[0]]+columns[1][stamp[1]]+columns[2][stamp[2]]+
                   columns[3][stamp[3]]+columns[4][stamp[4]]+columns[5][stamp[5]]+
                   columns[6][stamp[6]]+columns[7][stamp[7]]+columns[8][stamp[8]])
        state[3]=value
        return value

    def best(self,state):
        if state[4] is None:
            field=self.scorefield(state);candidates=self.guards;value=0
            for plane in range(4,-1,-1):
                hits=candidates&(field<<(4-plane))
                if hits:candidates=hits;value|=1<<plane
            state[4]=value,candidates
        else:value,candidates=state[4]
        return value-state[5]

    def choices(self,state,rng,branch=6):
        field=self.scorefield(state);remaining=self.guards;out=[]
        subtract=state[5]
        while remaining and len(out)<branch:
            if remaining==self.guards and state[4] is not None:
                value,candidates=state[4]
            else:
                candidates,value=remaining,0
                for plane in range(4,-1,-1):
                    hits=candidates&(field<<(4-plane))
                    if hits:candidates=hits;value|=1<<plane
            remaining^=candidates
            for _ in range(min(branch-len(out),4)):
                if not candidates:break
                offset=rng.randrange(self.count)
                after=candidates>>(5*offset)
                aid=((after&-after).bit_length()-1)//5+offset if after else ((candidates&-candidates).bit_length()-1)//5
                candidates^=16<<(5*aid)
                out.append((aid,value-subtract))
            if out and value-subtract<out[0][1]-1:break
        return out
