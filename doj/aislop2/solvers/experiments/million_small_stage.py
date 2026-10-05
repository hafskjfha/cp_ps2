import heapq
import random

def quotient_expander(n,d):
    rowbits=3*d
    rowmask=(1<<rowbits)-1
    rotations=[]
    for r in range(4):
        tables=[]
        for u in range(d):
            table=[]
            for value in range(1<<rowbits):
                out=0
                for v in range(d):
                    x,y=((u,v),(v,d-1-u),(d-1-u,d-1-v),(d-1-v,u))[r]
                    out|=(value>>3*v&7)<<3*(d*x+y)
                table.append(out)
            tables.append(table)
        rotations.append(tables)
    stamp_shift=3*n*n
    board_mask=(1<<stamp_shift)-1
    stride=3*n
    if d==2:
        def rotate(value,r):
            t=rotations[r]
            return t[0][value&63]|t[1][value>>6]
        def gather(value):
            return value&63|(value>>stride&63)<<6
        def scatter(value):
            return value&63|value>>6<<stride
    else:
        def rotate(value,r):
            t=rotations[r]
            return t[0][value&511]|t[1][value>>9&511]|t[2][value>>18]
        def gather(value):
            return value&511|(value>>stride&511)<<9|(value>>2*stride&511)<<18
        def scatter(value):
            return value&511|(value>>9&511)<<stride|value>>18<<2*stride
    patch_mask=sum(rowmask<<stride*u for u in range(d))
    patches=[(3*(n*x+y),board_mask^(patch_mask<<(3*(n*x+y))))for x in range(n-d+1)for y in range(n-d+1)]
    norms={}
    def normal(stamp):
        if stamp not in norms:
            variants=[rotate(stamp,r)for r in range(4)]
            value=min(variants)
            turn=variants.index(value)
            for r,variant in enumerate(variants):
                if variant not in norms:
                    norms[variant]=(value,(turn-r)&3)
        return norms[stamp]
    def expand(state):
        board,stamp=state&board_mask,state>>stamp_shift
        paints=[scatter(rotate(stamp,r))for r in range(4)]
        for p,(shift,mask)in enumerate(patches):
            patch=gather(board>>shift)
            picked,turn=normal(patch)
            retained=board&mask|picked<<stamp_shift
            for r in range(4):
                yield 4*p+r,retained|paints[r]<<shift,(turn+r)&3
    expand.normal=normal
    return expand

def fast_quotient_beam(n,d,initial,target,depth,width=512,budget=800000,seed=941,weight=1):
    nn=n*n
    pack=lambda a:sum(v<<(3*i)for i,v in enumerate(a))
    expand=quotient_expander(n,d)
    buf,phase=expand.normal(pack(initial[nn:]))
    first=pack(initial[:nn])|buf<<(3*nn)
    goal=pack(target)
    mask=sum(1<<(3*i)for i in range(nn))
    rng=random.Random(seed)
    selectedmask=sum(1<<(3*i)for i in range(nn)if rng.randrange(4)==0)if weight else 0
    def matches(state):
        diff=state^goal
        return nn-((diff|diff>>1|diff>>2)&mask).bit_count()
    bestscore=matches(first);best=[]
    upper=color_bound(initial,target)
    front=[(first,(),phase)];seen={first};used=0
    for level in range(depth):
        candidates={}
        for state,path,phase in front:
            for aid,child,turn in expand(state):
                used+=1
                if used>budget:return best,bestscore,used
                if child in seen or child in candidates:continue
                diff=child^goal
                wrong=(diff|diff>>1|diff>>2)&mask
                score=nn-wrong.bit_count()
                actual=aid//4*4+(aid+phase)%4
                if score>bestscore:
                    bestscore,best=score,list(path)+[actual]
                    if score==upper:return best,bestscore,used
                rank=score*8-(wrong&selectedmask).bit_count()*weight
                candidates[child]=(rank,rng.getrandbits(32),path+(actual,),(phase+turn)&3)
        if not candidates:break
        chosen=heapq.nlargest(width,candidates,key=candidates.get)
        front=[(state,candidates[state][2],candidates[state][3])for state in chosen]
        seen.update(chosen)
    return best,bestscore,used

def small_beam_stage(n,d,c,k,grid,target,stamp,reference):
    if not (4<=n<=12 and 4<=k<=16):
        return reference
    indices,_,ops,_,_=build(n,d,target)
    span=n-d+1
    final=grid+stamp
    for x,y,r in reference:
        _st(final,n*n,indices[(x*span+y)*4+r])
    value=sum(a==b for a,b in zip(final,target))
    if value==color_bound(grid+stamp,target):
        return reference
    width=2048 if d==3 and n<=6 else 512
    path,score,_=fast_quotient_beam(n,d,grid+stamp,target,k,width,1000000,941,1)
    if score>value:
        candidate=[ops[aid]for aid in path]
        return candidate
    return reference
