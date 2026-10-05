"""Exact joint spatial transformation of every temporal subsequence."""


def shift_refine(n,d,c,k,initial,target,indices,sequence,module,
                 rounds=2,blocks=(1,2,3),passes=1,reverse=True):
    nn,dd=n*n,d*d
    span=n-d+1
    pairs=[tuple((p,nn+j) for j,p in enumerate(idx)) for idx in indices]
    path=list(sequence)
    upper=sum(min(initial.count(v),target.count(v)) for v in range(c))

    def apply(row,aid):
        for p,q in pairs[aid]:
            row[p],row[q]=row[q],row[p]

    def snapshots():
        prefix=[bytearray(initial)]
        for aid in path:
            row=prefix[-1][:];apply(row,aid);prefix.append(row)
        wishes=[None]*(len(path)+1)
        wishes[-1]=bytearray(target+[6]*dd)
        for i in range(len(path)-1,-1,-1):
            row=wishes[i+1][:];apply(row,path[i]);wishes[i]=row
        return prefix,wishes,sum(a==b for a,b in zip(prefix[-1],target))

    offsets=[]
    for dist in blocks:
        for dx,dy in ((-dist,0),(dist,0),(0,-dist),(0,dist),(-dist,-dist),(-dist,dist),(dist,-dist),(dist,dist)):
            if abs(dx)<span and abs(dy)<span:offsets.append((dx,dy))
    transforms=[]
    for dx,dy in offsets:
        transforms.append([((a//4//span+dx)*span+a//4%span+dy)*4+a%4
                           if 0<=a//4//span+dx<span and 0<=a//4%span+dy<span else -1
                           for a in range(len(indices))])
    prefix,wishes,score=snapshots()
    if score==upper:return path
    for iteration in range(rounds):
        best_gain,best=0,None
        length=len(path)
        for mapping in transforms:
            shifted=[mapping[a] for a in path]
            for left in range(length):
                row=prefix[left][:];want=wishes[left][:];gain=0
                for right in range(left,length):
                    aid=shifted[right]
                    if aid<0:break
                    for p,q in pairs[path[right]]:
                        a,b=want[p],want[q];u,v=row[p],row[q]
                        gain+=(u==b)+(v==a)-(u==a)-(v==b)
                        want[p],want[q]=b,a
                    for p,q in pairs[aid]:
                        a,b=row[p],row[q];u,v=want[p],want[q]
                        gain+=(b==u)+(a==v)-(a==u)-(b==v)
                        row[p],row[q]=b,a
                    if gain>best_gain:
                        best_gain,best=gain,(left,right+1,shifted[left:right+1])
        if best is None:break
        left,right,block=best
        path[left:right]=block
        old_score=score
        prefix,wishes,score=snapshots()
        assert score==old_score+best_gain,(score,old_score,best_gain)
        if score==upper:break
    if passes:
        ops=[(a//4//span,a//4%span,a%4) for a in range(len(indices))]
        path=module['refine'](n,d,k,initial,target,list(zip(indices,ops)),path,passes=passes,seed_offset=163819)
    return path
