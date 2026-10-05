"""Research helper: exact conditional distant-pair operation optimization."""
import random


def spaced_refine(n, d, c, k, initial, target, indices, sequence, module,
                  pairs=64, alternatives=12, passes=1, seed_offset=0):
    nn, dd = n*n, d*d
    upper = sum(min(initial.count(v), target.count(v)) for v in range(c))
    q = len(indices)
    side = n-d+1
    ops = [(a//4//side, a//4%side, a%4) for a in range(q)]
    actions = list(zip(indices, ops))
    rng = random.Random(sum((i+117)*v for i,v in enumerate(initial))+k*6311+seed_offset)
    path = list(sequence) + [-1]*min(6,k-len(sequence))

    def swap(row, aid):
        if aid >= 0:
            for j,p in enumerate(indices[aid]):
                row[p],row[nn+j]=row[nn+j],row[p]

    def snapshots():
        prefix=[initial[:]]
        for aid in path:
            row=prefix[-1][:];swap(row,aid);prefix.append(row)
        wishes=[None]*(len(path)+1)
        wishes[-1]=target+[6]*dd
        for i in range(len(path)-1,-1,-1):
            row=wishes[i+1][:];swap(row,path[i]);wishes[i]=row
        return prefix,wishes,sum(a==b for a,b in zip(prefix[-1],target))

    def change(state,p,new):
        if p>=nn:
            old=state.stamp[p-nn]
            state.stamp[p-nn]=new
            return old
        old=state.grid[p]
        if old==new:return old
        for ref in range(dd):
            mask=state.positions[ref][p]
            state.values[ref][old]^=mask
            state.values[ref][new]^=mask
        delta=(new==state.wishes[p])-(old==state.wishes[p])
        if delta:
            carry=state.cover_bits[p];plane=0
            while carry:
                before=state.old_planes[plane]
                state.old_planes[plane]=before^carry
                carry&=~before if delta>0 else before
                plane+=1
        state.grid[p]=new
        return old

    def ranked(state,number):
        planes=[0]*5
        for jj in range(dd):
            for carry in (state.values[jj][state.wstamp[jj]],state.goals[jj][state.stamp[jj]]):
                plane=0
                while carry:
                    old=planes[plane];planes[plane]=old^carry;carry&=old;plane+=1
        carry=0
        for plane in range(5):
            a,b=planes[plane],state.old_planes[plane]
            diff=a^b;planes[plane]=diff^carry;carry=(a&b)|(diff&carry)
        remaining=state.all_bits;out=[]
        while remaining and len(out)<number:
            candidates=remaining
            for plane in reversed(planes):
                hits=candidates&plane
                if hits:candidates=hits
            remaining^=candidates
            for _ in range(min(8,number-len(out))):
                if not candidates:break
                offset=rng.randrange(q);after=candidates>>offset
                aid=(after&-after).bit_length()-1+offset if after else (candidates&-candidates).bit_length()-1
                candidates^=1<<aid;out.append(aid)
        return out

    prefix,wishes,score=snapshots()
    if score==upper or len(path)<3:return [a for a in path if a>=0]
    length=len(path)
    order=list(range(q));rng.shuffle(order)
    for trial in range(pairs):
        gap=min(length-1,(2,3,4,6,9,14,23,37,61,100,179)[trial%11])
        i=rng.randrange(length-gap);j=i+gap
        labels=list(range(nn+dd))
        for aid in path[i+1:j]:swap(labels,aid)
        destinations=[0]*(nn+dd)
        for p,v in enumerate(labels):destinations[v]=p
        state=module['RefineState'](n,d,prefix[j],wishes[j+1][:nn],actions,order)
        state.wstamp=wishes[j+1][nn:]
        old_i,old_j=path[i],path[j]
        oldgain=module['_og'](state,old_j)
        base=score-oldgain
        candidates=[-1]
        if old_i>=0:
            x,y,r=ops[old_i]
            for rr in range(4):candidates.append((x*side+y)*4+rr)
            for _ in range(alternatives//2):
                xx=min(side-1,max(0,x+rng.choice((-2,-1,0,1,2))))
                yy=min(side-1,max(0,y+rng.choice((-2,-1,0,1,2))))
                candidates.append((xx*side+yy)*4+rng.randrange(4))
        candidates.extend(rng.randrange(q) for _ in range(alternatives))
        early=module['RefineState'](n,d,prefix[i],wishes[i+1][:nn],actions,order)
        early.wstamp=wishes[i+1][nn:]
        candidates=ranked(early,alternatives*2)+candidates
        chosen=None
        for new_i in dict.fromkeys(candidates):
            if new_i==old_i:continue
            outgoing=prefix[i][:]
            swap(outgoing,new_i)
            touched=set(range(nn,nn+dd))
            if old_i>=0:touched.update(indices[old_i])
            if new_i>=0:touched.update(indices[new_i])
            updates=[];delta=0
            for p in touched:
                v=outgoing[p]
                if v!=prefix[i+1][p]:
                    dest=destinations[p]
                    old=change(state,dest,v)
                    updates.append((dest,old))
                    delta+=(v==wishes[j+1][dest])-(old==wishes[j+1][dest])
            new_j,gain=state.best()
            value=base+delta+gain
            if value>score:
                chosen=(new_i,new_j,value)
                break
            for p,old in updates:change(state,p,old)
        if chosen is not None:
            path[i],path[j],expected=chosen
            prefix,wishes,score=snapshots()
            assert score==expected,(score,expected)
            if score==upper:break
    candidate=[a for a in path if a>=0]
    if passes:
        candidate=module['refine'](n,d,k,initial,target,actions,candidate,passes=passes,seed_offset=901117+seed_offset)
    return candidate
