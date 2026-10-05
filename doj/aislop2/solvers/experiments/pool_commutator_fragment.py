def commutator_word_gain(grid,target,stamp,indices,word,touched):
    before=sum(grid[p]==target[p] for p in touched)
    for aid in word:
        transition(grid,stamp,indices[aid])
    after=sum(grid[p]==target[p] for p in touched)
    for aid in reversed(word):
        transition(grid,stamp,indices[aid])
    return after-before


def commutator_tail(n,d,grid,target,stamp,indices,seed,pair_limit=20000):
    if pair_limit<=0:
        return None
    width=n-d+1
    missing=[p for p in range(n*n) if grid[p]!=target[p]]
    if not missing:
        return None
    initial=n*n-len(missing)
    possible=color_bound(grid+stamp,target)-initial
    if possible<=0:
        return None
    focused=set()
    for p in missing:
        x,y=divmod(p,n)
        for row in range(max(0,x-d+1),min(x,width-1)+1):
            for col in range(max(0,y-d+1),min(y,width-1)+1):
                base=(row*width+col)*4
                focused.update(range(base,base+4))
    firsts=sorted(focused)
    rng=random.Random(seed)
    rng.shuffle(firsts)
    best_gain=0
    best_word=None
    examined=0
    seen=set()
    touched_cache={}
    for first in firsts:
        row,col=divmod(first//4,width)
        seconds=[(x*width+y)*4+r
                 for x in range(max(0,row-d+1),min(width,row+d))
                 for y in range(max(0,col-d+1),min(width,col+d))
                 for r in range(4)]
        rng.shuffle(seconds)
        for second in seconds:
            if first==second:
                continue
            pair=(min(first,second),max(first,second))
            if pair in seen:
                continue
            if examined>=pair_limit:
                return best_word
            seen.add(pair)
            examined+=1
            regions=(min(first//4,second//4),max(first//4,second//4))
            touched=touched_cache.get(regions)
            if touched is None:
                touched=tuple(sorted(set(indices[first])|set(indices[second])))
                touched_cache[regions]=touched
            for left,right in ((first,second),(second,first)):
                word=(left,right,left,right)
                gain=commutator_word_gain(grid,target,stamp,indices,word,touched)
                if gain>best_gain:
                    best_gain,best_word=gain,word
                    if best_gain==possible:
                        return best_word
    return best_word


def solve(n,d,c,k,grid,target,stamp):
    reference=solve_without_commutator(n,d,c,k,grid,target,stamp)
    if n>16 or k-len(reference)<4:
        return reference
    indices,_,operations,_,_=build(n,d,target)
    width=n-d+1
    board,buffer=grid[:],stamp[:]
    for x,y,r in reference:
        transition(board,buffer,indices[(x*width+y)*4+r])
    matches=sum(a==b for a,b in zip(board,target))
    if not 1<=n*n-matches<=12 or matches>=color_bound(grid+stamp,target):
        return reference
    seed=sum((i+41)*v for i,v in enumerate(grid+target+stamp))+n*1009+d*9176+k*131
    word=commutator_tail(n,d,board,target,buffer,indices,seed)
    if word is None:
        return reference
    return reference+[operations[aid] for aid in word]

