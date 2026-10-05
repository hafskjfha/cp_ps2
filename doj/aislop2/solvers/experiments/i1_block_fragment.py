def i1_packed_expand(n,d):
 """Packed complete-state transitions; IDs use ((x*width+y)*4+r)."""
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
 patches=[]
 for x in range(n-d+1):
  for y in range(n-d+1):
   shift=3*(n*x+y)
   patches.append((shift,board_mask^(patch_mask<<shift)))
 def apply(state,aid):
  p,r=divmod(aid,4)
  shift,mask=patches[p]
  board,stamp=state&board_mask,state>>stamp_shift
  patch=gather(board>>shift)
  return board&mask|scatter(rotate(stamp,r))<<shift|rotate(patch,-r&3)<<stamp_shift
 def expand(state):
  board,stamp=state&board_mask,state>>stamp_shift
  paints=[scatter(rotate(stamp,r))for r in range(4)]
  for p,(shift,mask) in enumerate(patches):
   patch=gather(board>>shift)
   retained=board&mask
   for r in range(4):
    yield 4*p+r,retained|paints[r]<<shift|rotate(patch,-r&3)<<stamp_shift
 expand.apply=apply
 return expand


def i1_search_block(n,d,initial,wanted,depth,width=8,node_budget=160000,seed=0,expand=None,reference=()):
 """Exact suffix objective, complete states, full legal expansions, fixed cap."""
 import heapq,random,itertools
 if expand is None:
  expand=i1_packed_expand(n,d)
 packed=sum(v<<3*i for i,v in enumerate(initial))
 goal=sum(v<<3*i for i,v in enumerate(wanted))
 mask=sum(1<<3*i for i,v in enumerate(wanted) if v!=6)
 scored=mask.bit_count()
 def score(state):
  diff=state^goal
  return scored-((diff|diff>>1|diff>>2)&mask).bit_count()
 best_score=score(packed)
 best=[]
 upper=sum(min(initial.count(v),wanted.count(v))for v in range(6))
 frontier=[(packed,())]
 visited={packed}
 rng=random.Random(seed)
 used=0
 reference=tuple(reference[:depth])
 refstate=packed
 for level in range(max(0,depth)):
  if used>=node_budget or best_score==upper:
   break
  candidates={}
  refnode=None
  if level<len(reference):
   aid=reference[level]
   if level and aid==reference[level-1]:
    reference=reference[:level]
   else:
    refstate=expand.apply(refstate,aid)
    used+=1
    refnode=(refstate,reference[:level+1])
    value=score(refstate)
    if value>best_score:
     best_score,best=value,list(refnode[1])
     if value==upper:
      return best,best_score,used
  for parent,(state,path) in enumerate(frontier):
   for aid,child in itertools.islice(expand(state),max(0,node_budget-used)):
    used+=1
    if (path and aid==path[-1]) or child in visited or child in candidates:
     continue
    value=score(child)
    candidates[child]=(value,rng.getrandbits(32),parent,aid)
    if value>best_score:
     best_score,best=value,list(path)+[aid]
     if value==upper:
      return best,best_score,used
   if used>=node_budget:
    break
  chosen=heapq.nlargest(max(1,width),candidates,key=candidates.get)
  next_frontier=[]
  for state in chosen:
   _,_,parent,aid=candidates[state]
   next_frontier.append((state,frontier[parent][1]+(aid,)))
  if refnode is not None and refnode[0] not in chosen:
   if len(next_frontier)>=max(1,width):
    next_frontier.pop()
   next_frontier.append(refnode)
  if not next_frontier:
   break
  frontier=next_frontier
  visited.update(state for state,_ in frontier)
 return best,best_score,used


def i1_block_repair(n,d,c,k,initial,target,actions,sequence,rounds=4,width=8,node_budget=160000):
 """Replace internal/suffix blocks only upon verified strict final-score gain."""
 import random
 nn,dd=n*n,d*d
 final_wanted=list(target)+[6]*dd
 def swap(state,aid):
  for j,p in enumerate(actions[aid][0]):
   state[p],state[nn+j]=state[nn+j],state[p]
 def snapshots(path):
  state=list(initial)
  forward=[state[:]]
  for aid in path:
   swap(state,aid)
   forward.append(state[:])
  wishes=final_wanted[:]
  reverse=[None]*(len(path)+1)
  reverse[-1]=wishes[:]
  for j in range(len(path)-1,-1,-1):
   swap(wishes,path[j])
   reverse[j]=wishes[:]
  return forward,reverse
 best=[]
 for aid in sequence:
  if aid>=0:
   if best and best[-1]==aid:
    best.pop()
   else:
    best.append(aid)
 forward,reverse=snapshots(best)
 best_score=sum(a==b for a,b in zip(forward[-1],final_wanted))
 upper=sum(min(initial.count(v),target.count(v))for v in range(c))
 q=len(actions)
 minimum=q*(1+max(1,width)*max(0,min(4,k)-1))+min(4,k)
 rounds=min(max(0,rounds),max(1,node_budget//max(1,minimum)))
 if not rounds or k<=0 or best_score==upper:
  return best
 seed=sum((i+43)*v for i,v in enumerate(initial))+k*8161+n*319+d
 rng=random.Random(seed)
 expand=i1_packed_expand(n,d)
 for trial in range(rounds):
  allowance=node_budget//(rounds-trial)
  affordable=max(0,1+(allowance-q-32)//(max(1,width)*q))
  requested=(4,8,16,32)[trial%4]
  length=max((v for v in (4,8,16,32) if v<=min(requested,affordable)),default=min(requested,affordable))
  length=min(k,length)
  if length<=0:
   break
  span=min(length,len(best))
  left=len(best)-span if trial%4 in (0,3) else rng.randrange(len(best)-span+1)
  right=left+span
  depth=min(length,k-len(best)+span)
  block,value,used=i1_search_block(n,d,forward[left],reverse[right],depth,width,allowance,seed+trial*104729,expand,best[left:right])
  node_budget-=used
  if value>best_score:
   candidate=best[:left]+block+best[right:]
   ahead,behind=snapshots(candidate)
   actual=sum(a==b for a,b in zip(ahead[-1],final_wanted))
   if len(candidate)<=k and actual>best_score:
    best,best_score=candidate,actual
    forward,reverse=ahead,behind
  if best_score==upper:
   break
 return best
