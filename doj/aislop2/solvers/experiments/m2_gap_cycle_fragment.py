"""Generalized three-cycle repair by conjugation BFS."""
import collections


def m2_small_cycle_repair(n,d,k,grid,target,stamp,actions,minimum_gain=1):
    nn=n*n;dd=d*d;width=n-d+1;size=nn+dd
    def canonical(a,b,c):
        if a<b and a<c:return(a,b,c)
        if b<c:return(b,c,a)
        return(c,a,b)
    direct={}
    for x in range(width):
        for y in range(width):
            for dx,dy in ((d-1,d-1),(d-1,1-d)):
                if not(0<=x+dx<width and 0<=y+dy<width):continue
                for r in range(4):
                    a=(x*width+y)*4+r
                    b=((x+dx)*width+y+dy)*4+r
                    pa=(a,b)*3+((a//4)*4+(r+2)%4,(b//4)*4+(r+2)%4)*3
                    state=list(range(size))
                    for aid in pa:
                        for j,p in enumerate(actions[aid]):state[p],state[nn+j]=state[nn+j],state[p]
                    changed=[p for p,q in enumerate(state) if p!=q]
                    assert len(changed)==3
                    p=changed[0];q=state[p];r2=state[q]
                    triple=canonical(p,q,r2)
                    direct[triple]=pa
                    direct[canonical(p,r2,q)]=pa[::-1]
    renames=[]
    for pos in actions:
        mapping=list(range(size))
        for j,p in enumerate(pos):mapping[p]=nn+j;mapping[nn+j]=p
        renames.append(mapping)
    wanted=target if len(target)>nn else target+[6]*dd
    def score(state,triple):
        a,b,c=triple
        gain=0
        for p,q in ((a,b),(b,c),(c,a)):
            gain+=(state[q]==wanted[p])-(state[p]==wanted[p])
        return gain
    state=grid+stamp
    initial=sum(a==b for a,b in zip(state,wanted))
    parents={trip:None for trip in direct}
    front=list(direct)
    used=0
    for depth in range(12,min(k,24)+1,2):
        for triple in front:
            gain=score(state,triple)
            if gain>=minimum_gain:
                word=[];tr=triple
                while parents[tr] is not None:
                    tr,aid=parents[tr];word.append(aid)
                path=word+list(direct[tr])+word[::-1]
                return path,initial+gain,len(parents),depth
        if depth+2>k:break
        nextfront=[]
        for triple in front:
            a,b,c=triple
            for aid,rename in enumerate(renames):
                used+=1
                if used>1000000:return [],initial,len(parents),0
                child=canonical(rename[a],rename[b],rename[c])
                if child not in parents:
                    parents[child]=(triple,aid);nextfront.append(child)
                    gain=score(state,child)
                    if gain>=minimum_gain:
                        word=[];tr=child
                        while parents[tr] is not None:
                            tr,step=parents[tr];word.append(step)
                        path=word+list(direct[tr])+word[::-1]
                        return path,initial+gain,len(parents),depth+2
        front=nextfront
        if not front:break
    return [],initial,len(parents),0


_m2_cycle_parent=solve

def solve(n,d,c,k,grid,target,stamp):
    reference=_m2_cycle_parent(n,d,c,k,grid,target,stamp)
    if d!=3 or n<5 or k-len(reference)<12:return reference
    indices,_,ops,_,_=build(n,d,target)
    side=n-d+1
    state=grid+stamp
    for x,y,r in reference:_st(state,n*n,indices[(x*side+y)*4+r])
    score=sum(a==b for a,b in zip(state,target))
    bound=color_bound(grid+stamp,target)
    for _ in range(3):
        if score==bound or k-len(reference)<12:break
        path,value,_,_=m2_small_cycle_repair(n,d,k-len(reference),state[:n*n],target,state[n*n:],indices)
        if value<=score:break
        reference=reference+[ops[aid] for aid in path]
        for aid in path:_st(state,n*n,indices[aid])
        score=value
    return reference
