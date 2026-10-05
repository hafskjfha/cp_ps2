"""Exact six-operation three-cycles from almost-identical conjugated stamps."""
_M2_GAP_SIX_TEMPLATES=None
_M2_GAP_SIX_GEOMETRY=None

def m2_gap_six_templates():
 global _M2_GAP_SIX_TEMPLATES
 if _M2_GAP_SIX_TEMPLATES is not None:return _M2_GAP_SIX_TEMPLATES
 n=5;d=3;nn=25;size=34;indices=[];ops=[]
 for x in range(3):
  for y in range(3):
   for r in range(4):
    patch=[]
    for u in range(3):
     for v in range(3):
      p,q=((u,v),(v,2-u),(2-u,2-v),(2-v,u))[r];patch.append((x+p)*5+y+q)
    indices.append(patch);ops.append((x,y,r))
 groups={};found={}
 for a in range(len(indices)):
  for b in range(len(indices)):
   if a==b:continue
   st=list(range(size))
   for aid in(a,b,a):
    for j,p in enumerate(indices[aid]):st[p],st[nn+j]=st[nn+j],st[p]
   pairs=tuple((p,q)for p,q in enumerate(st)if p<q)
   for j,pair in enumerate(pairs):
    key=pairs[:j]+pairs[j+1:]
    for old,word in groups.get(key,[]):
     if len(set(old+pair))!=3:continue
     path=word+(a,b,a);state=list(range(size))
     for aid in path:
      for j,p in enumerate(indices[aid]):state[p],state[nn+j]=state[nn+j],state[p]
     changed=[p for p,q in enumerate(state)if p!=q];assert len(changed)==3
     grids=[p for p in changed if p<nn]
     if len(grids)!=1:continue
     p=grids[0];q=state[p];r=state[q];assert q>=nn and r>=nn and state[r]==p
     found[p,q-nn,r-nn]=tuple(ops[a]for a in path)
    groups.setdefault(key,[]).append((pair,(a,b,a)))
 _M2_GAP_SIX_TEMPLATES=[(p//5,p%5,q,r,path)for(p,q,r),path in found.items()]
 return _M2_GAP_SIX_TEMPLATES

def m2_gap_six_geometry(n):
 global _M2_GAP_SIX_GEOMETRY
 if _M2_GAP_SIX_GEOMETRY is not None and _M2_GAP_SIX_GEOMETRY[0]==n:return _M2_GAP_SIX_GEOMETRY[1]
 nn=n*n;found={}
 for u,v,q,r,word in m2_gap_six_templates():
  minx=min(p[0]for p in word);miny=min(p[1]for p in word);maxx=max(p[0]for p in word);maxy=max(p[1]for p in word)
  for x in range(-minx,n-2-maxx):
   for y in range(-miny,n-2-maxy):
    p=(x+u)*n+y+v;key=(p,nn+q,nn+r)
    if key not in found:found[key]=tuple((x+a,y+b,c)for a,b,c in word)
 _M2_GAP_SIX_GEOMETRY=n,found
 return found

def m2_gap_six_choose(n,state,wanted,minimum_gain=1):
 best=minimum_gain-1;word=None
 for(p,q,r),path in m2_gap_six_geometry(n).items():
  gain=(state[q]==wanted[p])+(state[r]==wanted[q])+(state[p]==wanted[r])-(state[p]==wanted[p])-(state[q]==wanted[q])-(state[r]==wanted[r])
  if gain>best:best=gain;word=path
 return word,best


"""Conjugates of a six-stamp double-transposition macro."""
_M2_GAP_PAIR_GEOMETRY=None

def m2_gap_paired_repair(n,d,k,grid,target,stamp,actions,budget=1000000,minimum_gain=1):
 nn=n*n;dd=d*d;width=n-d+1;size=nn+dd
 def canonical(a,b,c,e):
  if a>b:a,b=b,a
  if c>e:c,e=e,c
  return(a,b,c,e)if a<c else(c,e,a,b)
 global _M2_GAP_PAIR_GEOMETRY
 if _M2_GAP_PAIR_GEOMETRY is not None and _M2_GAP_PAIR_GEOMETRY[0]==(n,d):
  direct,renames=_M2_GAP_PAIR_GEOMETRY[1:]
 else:
  templates=[]
  offsets=[[(u,v),(v,2-u),(2-u,2-v),(2-v,u)]for u in range(3)for v in range(3)]
  for dx,dy in ((0,2),(1,-2),(1,2),(2,-1),(2,0),(2,1)):
   for r in range(4):
    a=[xy[r]for xy in offsets];b=[(dx+xy[(r+2)%4][0],dy+xy[(r+2)%4][1])for xy in offsets]
    state={p:p for p in set(a+b)};state.update({j:j for j in range(9)})
    for _ in range(3):
     for patch in(a,b):
      for j,p in enumerate(patch):state[p],state[j]=state[j],state[p]
    changed=[p for p,q in state.items()if p!=q];assert len(changed)==4
    a=changed[0];b=state[a];c=next(p for p in changed if p not in(a,b));e=state[c]
    assert state[b]==a and state[e]==c
    templates.append((dx,dy,r,(a,b,c,e)))
  direct={}
  for x in range(width):
   for y in range(width):
    for dx,dy,r,vertices in templates:
     if not(0<=x+dx<width and 0<=y+dy<width):continue
     a=(x*width+y)*4+r;b=((x+dx)*width+y+dy)*4+(r+2)%4
     points=[nn+p if isinstance(p,int)else(x+p[0])*n+y+p[1]for p in vertices]
     direct[canonical(*points)]=(a,b)*3
  renames=[]
  for pos in actions:
   mapping=list(range(size))
   for j,p in enumerate(pos):mapping[p]=nn+j;mapping[nn+j]=p
   renames.append(mapping)
  _M2_GAP_PAIR_GEOMETRY=(n,d),direct,renames
 wanted=target if len(target)>nn else target+[6]*dd;state=grid+stamp;initial=sum(a==b for a,b in zip(state,wanted))
 def score(a,b,c,e):
  return (state[b]==wanted[a])+(state[a]==wanted[b])+(state[e]==wanted[c])+(state[c]==wanted[e])-(state[a]==wanted[a])-(state[b]==wanted[b])-(state[c]==wanted[c])-(state[e]==wanted[e])
 def reconstruct(tr):
  word=[]
  while parents[tr] is not None:tr,aid=parents[tr];word.append(aid)
  return word+list(direct[tr])+word[::-1]
 parents={tr:None for tr in direct};front=list(direct);used=0
 for depth in range(6,min(k,16)+1,2):
  for tr in front:
   gain=score(*tr)
   if gain>=minimum_gain:return reconstruct(tr),initial+gain,used
  if depth+2>k:break
  nextfront=[]
  for tr in front:
   a,b,c,e=tr
   for aid,rename in enumerate(renames):
    used+=1
    if used>budget:return [],initial,used
    child=canonical(rename[a],rename[b],rename[c],rename[e])
    if child not in parents:
     parents[child]=(tr,aid);nextfront.append(child)
     gain=score(*child)
     if gain>=minimum_gain:return reconstruct(child),initial+gain,used
  front=nextfront
  if not front:break
 return [],initial,used



def m2_gap_optional(n,d,c,k,grid,target,stamp,reference):
    if d!=3 or n<5 or k<5:return reference
    nn=n*n;side=n-d+1
    indices,_,ops,_,_=build(n,d,target)
    wanted=target+[6]*(d*d)
    upper=color_bound(grid+stamp,target)
    def action(op):
        x,y,r=op;return(x*side+y)*4+r
    def snapshots(path):
        state=grid+stamp;rows=[state[:]]
        for op in path:_st(state,nn,indices[action(op)]);rows.append(state[:])
        return rows
    def score(path):
        state=grid+stamp
        for op in path:_st(state,nn,indices[action(op)])
        return sum(a==b for a,b in zip(state,target))
    best=score(reference)
    if best==upper:return reference
    if n<=12 and k<=16:
        candidate=seven_backward_construct(n,d,c,k,grid,target,stamp,width=512,branch=12,future_weight=3)
        value=score(candidate)
        if value>best:reference=candidate;best=value
    if best==upper or k<6:return reference
    # Rebuild late prefixes using exact six-operation one-grid-cell cycles.
    original=reference;forward=snapshots(original)
    for cut in range(min(len(original),k-6),-1,-1):
        state=forward[cut][:];value=sum(a==b for a,b in zip(state,target))
        if value+(k-cut)//6<=best:continue
        candidate=original[:cut]
        while k-len(candidate)>=6:
            word,gain=m2_gap_six_choose(n,state,wanted)
            if word is None:break
            candidate=candidate+list(word)
            for op in word:_st(state,nn,indices[action(op)])
            value=sum(a==b for a,b in zip(state,target))
            if value>best:reference=candidate;best=value
            if best==upper:break
        if best==upper:return reference
    # A bounded conjugation search also covers useful two-swap permutations.
    original=reference;forward=snapshots(original)
    cuts=[len(original)]
    if n<=10:cuts+=list(range(min(len(original),k-6),-1,-1))
    tried=0
    for cut in dict.fromkeys(cuts):
        if k-cut<6:continue
        state=forward[cut];value=sum(a==b for a,b in zip(state,target))
        if value+4<=best:continue
        if tried>=4:break
        tried+=1
        path,estimate,_=m2_gap_paired_repair(n,d,k-cut,state[:nn],target,state[nn:],indices,budget=350000,minimum_gain=best-value+1)
        if estimate>best:
            candidate=original[:cut]+[ops[a]for a in path];value=score(candidate)
            if value>best:reference=candidate;best=value
            if best==upper:return reference
    # Replace short weak interior windows, using exact propagated suffix wishes.
    original=reference;forward=snapshots(original);sequence=[action(op)for op in original]
    reverse=[None]*(len(sequence)+1);state=wanted[:];reverse[-1]=state[:]
    for j in range(len(sequence)-1,-1,-1):_st(state,nn,indices[sequence[j]]);reverse[j]=state[:]
    windows=[]
    for length in(6,8,10):
        for left in range(len(sequence)-length+1):
            right=left+length;baseline=sum(a==b for a,b in zip(forward[left],reverse[right]))
            if baseline+4>best:windows.append((baseline,-length,left,right))
    windows.sort(reverse=True)
    for baseline,_,left,right in windows[:6]:
        if baseline+4<=best:continue
        state=forward[left];depth=right-left+k-len(sequence)
        path,estimate,_=m2_gap_paired_repair(n,d,depth,state[:nn],reverse[right],state[nn:],indices,budget=350000,minimum_gain=best-baseline+1)
        if estimate>best:
            candidate=original[:left]+[ops[a]for a in path]+original[right:];value=score(candidate)
            if value>best:reference=candidate;best=value
            if best==upper:return reference
    return reference

_m2_gap_optional_parent=solve

def solve(n,d,c,k,grid,target,stamp):
    reference=_m2_gap_optional_parent(n,d,c,k,grid,target,stamp)
    return m2_gap_optional(n,d,c,k,grid,target,stamp,reference)
