"""Bit-parallel backward construction with static pickup-match masks."""
import random

def addmask(planes,carry,increment):
    level=0
    if increment:
        while carry:
            old=planes[level];planes[level]=old^carry;carry&=old;level+=1
    else:
        while carry:
            old=planes[level];planes[level]=old^carry;carry&=~old;level+=1

class FastBack:
    def __init__(self,n,d,grid,target,stamp,indices):
        dd=d*d;nn=n*n;size=len(indices)
        self.indices=indices;self.grid=grid;self.stamp=stamp;self.dd=dd
        self.columns=[[0]*7 for _ in range(dd)]
        self.pickup=[[0]*7 for _ in range(nn)]
        self.cover=[0]*nn
        self.allbits=(1<<size)-1
        planes=[0]*5
        for aid,patch in enumerate(indices):
            bit=1<<aid
            value=dd
            for j,p in enumerate(patch):
                self.columns[j][grid[p]]|=bit
                self.pickup[p][stamp[j]]|=bit
                self.cover[p]|=bit
                value+=(target[p]==stamp[j])-(target[p]==grid[p])
            for level in range(5):
                if value>>level&1:planes[level]|=bit
        self.first=(bytearray(target),bytearray([6])*dd,planes)

    def apply(self,state,aid):
        board,stamp,planes=state
        board=board[:];stamp=stamp[:];planes=planes[:]
        for j,p in enumerate(self.indices[aid]):
            old,new=board[p],stamp[j]
            if old!=new:
                om,nm=self.pickup[p][old],self.pickup[p][new]
                addmask(planes,nm&~om,True)
                addmask(planes,om&~nm,False)
                delta=(new==self.grid[p])-(old==self.grid[p])
                if delta:addmask(planes,self.cover[p],delta<0)
                board[p]=new
            stamp[j]=old
        return board,stamp,planes

    def scoreplanes(self,state):
        planes=state[2][:]
        for j,color in enumerate(state[1]):
            addmask(planes,self.columns[j][color],True)
        return planes

    def best(self,state):
        planes=self.scoreplanes(state)
        candidates,value=self.allbits,0
        for level in range(4,-1,-1):
            hits=candidates&planes[level]
            if hits:candidates=hits;value|=1<<level
        return value-self.dd-sum(a==b for a,b in zip(state[1],self.stamp))

    def choices(self,state,rng,branch=6):
        planes=self.scoreplanes(state)
        remaining=self.allbits
        out=[]
        subtract=self.dd+sum(a==b for a,b in zip(state[1],self.stamp))
        count=len(self.indices)
        while remaining and len(out)<branch:
            candidates,value=remaining,0
            for level in range(4,-1,-1):
                hits=candidates&planes[level]
                if hits:candidates=hits;value|=1<<level
            remaining^=candidates
            for _ in range(min(branch-len(out),4)):
                if not candidates:break
                offset=rng.randrange(count)
                after=candidates>>offset
                aid=(after&-after).bit_length()-1+offset if after else (candidates&-candidates).bit_length()-1
                candidates^=1<<aid
                out.append((aid,value-subtract))
            if out and value-subtract<out[0][1]-1:break
        return out

def construct(m,n,d,c,k,grid,target,stamp,width=24,branch=6,future_weight=3,mixed=0):
    nn=n*n
    indices,_,ops,_,_=m.build(n,d,target)
    actions=list(zip(indices,ops))
    initial=grid+stamp
    engine=FastBack(n,d,grid,target,stamp,indices)
    base=sum(a==b for a,b in zip(grid,target))
    upper=m.color_bound(initial,target)
    beam=[(engine.first,[],base)]
    best,bestscore=[],base
    rng=random.Random(sum((i+83)*v for i,v in enumerate(initial))+k*1709)
    for depth in range(k):
        candidates=[];seen=set()
        for state,path,score in beam:
            for aid,gain in engine.choices(state,rng,branch):
                if path and aid==path[-1]:continue
                child=engine.apply(state,aid)
                key=bytes(child[0]+child[1])
                if key in seen:continue
                seen.add(key)
                path2=path+[aid]
                value=score+gain
                if value>bestscore:best,bestscore=path2,value
                if value==upper:return [ops[x] for x in reversed(best)]
                future=max(0,engine.best(child)) if future_weight and depth+1<k else 0
                candidates.append((value*8+future_weight*future,rng.random(),child,path2,value))
        if not candidates:break
        candidates.sort(key=lambda row:row[:2],reverse=True)
        beam=[(child,path,value)for _,_,child,path,value in candidates[:width]]
    path=list(reversed(best))
    path=m.refine(n,d,k,initial,target,actions,path,passes=6)
    path=m.pair_sweep(n,d,k,initial,target,actions,path,passes=2,width=24)
    return [ops[x] for x in path]
