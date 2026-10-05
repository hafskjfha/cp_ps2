import heapq
import random


def minimal_goals(initial, target, stamp, count=64):
    n = len(target)
    required = [initial.count(v) - target.count(v) for v in range(6)]
    if min(required) < 0 or sum(required) != len(stamp):
        return []
    todo = [tuple(stamp)]
    seen = set(todo)
    for _ in range(len(stamp)):
        next_layer = []
        complete = []
        for buf in todo:
            counts = [buf.count(v) for v in range(6)]
            want = next((v for v in range(6) if counts[v] < required[v]), -1)
            if want < 0:
                complete.append(buf)
                continue
            for j, old in enumerate(buf):
                if counts[old] > required[old]:
                    child = buf[:j] + (want,) + buf[j+1:]
                    if child not in seen:
                        seen.add(child)
                        next_layer.append(child)
        if complete:
            return [target + list(buf) for buf in complete[:count]]
        todo = next_layer[:count]
    return [target + list(buf) for buf in todo[:count]]


def bidirectional_finish(n, d, start, target, endstamp, k, expand, width=256, budget=600000, seed=123):
    if k <= 0:
        return None, 0
    pack = lambda a: sum(v << (3*i) for i,v in enumerate(a))
    first = pack(start)
    goals = [pack(x) for x in minimal_goals(start, target, endstamp)]
    if not goals:
        return None, 0
    nn = n*n
    mask = sum(1 << (3*i) for i in range(len(start)))
    boardmask = sum(1 << (3*i) for i in range(nn))
    front = [[(first, ())], [(state, ()) for state in goals]]
    seen = [{first: ()}, {state: () for state in goals}]
    rng = random.Random(seed)
    spent = 0
    levels = [0,0]
    for step in range(k):
        side = step % 2
        other = 1-side
        candidates = {}
        goal = goals[0] if side == 0 else first
        for state, path in front[side]:
            for aid, child in expand(state):
                spent += 1
                if spent >= budget:
                    return None, spent
                if child in seen[other] and len(path)+1+len(seen[other][child]) <= k:
                    near = path + (aid,)
                    far = seen[other][child]
                    return list(near + far[::-1]) if side==0 else list(far + near[::-1]), spent
                if (path and aid == path[-1]) or child in seen[side] or child in candidates:
                    continue
                diff = child ^ goal
                wrong = (diff | diff>>1 | diff>>2) & mask
                cost = wrong.bit_count() + (wrong & boardmask).bit_count()
                if side == 0:
                    cost = (wrong & boardmask).bit_count()*4 + wrong.bit_count()
                candidates[child] = (-cost, rng.getrandbits(32), path + (aid,))
        if not candidates:
            return None, spent
        chosen = heapq.nlargest(width, candidates, key=candidates.get)
        front[side] = [(state, candidates[state][2]) for state in chosen]
        seen[side].update(front[side])
        levels[side] += 1
    return None, spent


def finish_parent(parent, n,d,c,k,grid,target,stamp,reference,budget=600000,width=256):
    if not 4 <= n <= 9 or k < 4:
        return reference, 0
    nn=n*n
    actions,_,ops,_,_=parent.build(n,d,target)
    span=n-d+1
    seq=[(x*span+y)*4+r for x,y,r in reference]
    state=grid+stamp
    states=[state[:]]
    for aid in seq:
        parent._st(state,nn,actions[aid]); states.append(state[:])
    value=sum(a==b for a,b in zip(state,target))
    if not nn-2<=value<nn or parent.color_bound(grid+stamp,target)!=nn:
        return reference,0
    cut=max(0,len(seq)-8)
    start=states[cut]
    path,spent=bidirectional_finish(n,d,start,target,state[nn:],min(k-cut,20),parent.i1_packed_expand(n,d),width,budget)
    if path is None:
        return reference,spent
    candidate=seq[:cut]+path
    final=grid+stamp
    for aid in candidate:
        parent._st(final,nn,actions[aid])
    if sum(a==b for a,b in zip(final,target))>value:
        return [ops[aid] for aid in candidate],spent
    return reference,spent


def quotient_beam(parent,n,d,initial,target,depth,width=512,budget=800000,seed=941,weight=0):
    nn=n*n
    pack=lambda a:sum(v<<(3*i)for i,v in enumerate(a))
    first=pack(initial)
    goal=pack(target)
    mask=sum(1<<(3*i)for i in range(nn))
    boardmask=(1<<(3*nn))-1
    smask=(1<<(3*d*d))-1
    rots=[[p*d+q for u in range(d)for v in range(d)for p,q in [((u,v),(v,d-1-u),(d-1-u,d-1-v),(d-1-v,u))[r]]]for r in range(4)]
    lookup={}
    def canonical(state):
        stamp=state>>(3*nn)
        normal=lookup.get(stamp)
        if normal is None:
            vals=[sum((stamp>>(3*j)&7)<<(3*p)for j,p in enumerate(rot))for rot in rots]
            normal=min(vals)
            for v in vals:lookup[v]=normal
        return state&boardmask|normal<<(3*nn)
    rng=random.Random(seed)
    selectedmask=0
    if weight:
        selectedmask=sum(1<<(3*i)for i in range(nn)if rng.randrange(4)==0)
    expand=parent.i1_packed_expand(n,d)
    def matches(state):
        diff=state^goal
        return nn-((diff|diff>>1|diff>>2)&mask).bit_count()
    bestscore=matches(first);best=[]
    upper=parent.color_bound(initial,target)
    front=[(first,())];seen={canonical(first)};used=0
    for level in range(depth):
        candidates={}
        for state,path in front:
            for aid,child in expand(state):
                used+=1
                if used>budget:return best,bestscore,used
                if path and aid==path[-1]:continue
                key=canonical(child)
                if key in seen or key in candidates:continue
                diff=child^goal
                wrong=(diff|diff>>1|diff>>2)&mask
                score=nn-wrong.bit_count()
                if score>bestscore:
                    bestscore,best=score,list(path)+( [aid] )
                    if score==upper:return best,bestscore,used
                rank=score*8-(wrong&selectedmask).bit_count()*weight
                candidates[key]=(rank,rng.getrandbits(32),child,path+(aid,))
        if not candidates:break
        chosen=heapq.nlargest(width,candidates,key=candidates.get)
        front=[(candidates[key][2],candidates[key][3])for key in chosen]
        seen.update(chosen)
    return best,bestscore,used


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


def fast_quotient_beam(parent,n,d,initial,target,depth,width=512,budget=800000,seed=941,weight=1):
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
    upper=parent.color_bound(initial,target)
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


def small_beam_stage(parent,n,d,c,k,grid,target,stamp,reference):
    if not (4<=n<=12 and 4<=k<=16):
        return reference
    indices,_,ops,_,_=parent.build(n,d,target)
    span=n-d+1
    final=grid+stamp
    for x,y,r in reference:
        parent._st(final,n*n,indices[(x*span+y)*4+r])
    value=sum(a==b for a,b in zip(final,target))
    if value==parent.color_bound(grid+stamp,target):
        return reference
    width=2048 if d==3 and n<=6 else 512
    path,score,_=fast_quotient_beam(parent,n,d,grid+stamp,target,k,width,1000000,941,1)
    if score>value:
        candidate=[ops[aid]for aid in path]
        return candidate
    return reference
