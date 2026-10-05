"""Packed comparisons and deterministic diversified greedy plateau search."""
import random
import sys
RUNS=12
NEUTRAL=True
def color_bound(initial,target):
 available,needed=([0]*6,[0]*6)
 for value in initial:
  available[value]+=1
 for value in target:
  needed[value]+=1
 return sum((min(a,b)for a,b in zip(available,needed)))
def build(n,d,target):
 rotations=[]
 for r in range(4):
  rotations.append([p*n+q for u in range(d)for v in range(d)for p,q in[((u,v),(v,d-1-u),(d-1-u,d-1-v),(d-1-v,u))[r]]])
 indices,codes,operations=([],[],[])
 coverage=[[]for _ in range(n*n)]
 patches=[]
 for x in range(n-d+1):
  for y in range(n-d+1):
   patch=len(patches)
   positions=[x*n+y+v for v in rotations[0]]
   patches.append(positions)
   for pos in positions:
    coverage[pos].append(patch)
   for r in range(4):
    action=tuple((x*n+y+v for v in rotations[r]))
    indices.append(action)
    codes.append(sum((1<<6*j+target[pos]for j,pos in enumerate(action))))
    operations.append((x,y,r))
 return(indices,codes,operations,coverage,patches)
def transition(grid,stamp,indices):
 for j,pos in enumerate(indices):
  stamp[j],grid[pos]=(grid[pos],stamp[j])
def solve_plateau(n,d,c,k,initial,target,start_stamp):
 initial_score=sum((a==b for a,b in zip(initial,target)))
 limit=color_bound(initial+start_stamp,target)
 if initial_score==limit:
  return[]
 best_score,answer=(initial_score,[])
 seed=917351
 for value in initial+target+start_stamp:
  seed=(seed^value)*1000003&4294967295
 rng=random.Random(seed)
 order=list(range(4*(n-d+1)**2))
 for run in range(RUNS):
  if run:
   rng.shuffle(order)
  state=State(n,d,c,initial[:],target,start_stamp[:],order[:])
  score,path=(initial_score,[])
  seen=set()
  for step in range(k):
   seen.add(tuple(state.stamp))
   gain,candidates=state.best_candidates()
   if gain<0 or(gain==0 and(not NEUTRAL or run==0)):
    break
   chosen=-1
   while candidates:
    bit=candidates&-candidates
    action=state.order[bit.bit_length()-1]
    if gain>0 or tuple((state.grid[p]for p in state.actions[action][0]))not in seen:
     chosen=action
     break
    candidates^=bit
   if chosen<0:
    break
   if gain>0:
    seen.clear()
   state.apply(chosen)
   score+=gain
   path.append(state.actions[chosen][1])
   if score>best_score:
    best_score,answer=(score,path[:])
   if best_score==limit:
    return answer
 return answer
class State:
 _geometry_cache=None
 def __init__(self,n,d,c,grid,target,stamp,order=None):
  self.n,self.d,self.c=(n,d,c)
  self.grid,self.target,self.stamp=(grid,target,stamp)
  self.matches=sum((a==b for a,b in zip(grid,target)))
  self.limit=color_bound(grid+stamp,target)
  key=(n,d,c,tuple(target))
  cached=State._geometry_cache
  if cached is not None and cached[0]==key:
   self.regions,self.actions,self.masks,self.cover=cached[1:]
  else:
   self.regions=[]
   self.actions=[]
   self.masks=[]
   self.cover=[[]for _ in grid]
   rotations=[]
   for r in range(4):
    offsets=[]
    for u in range(d):
     for v in range(d):
      p,q=((u,v),(v,d-1-u),(d-1-u,d-1-v),(d-1-v,u))[r]
      offsets.append(p*n+q)
    rotations.append(offsets)
   for x in range(n-d+1):
    for y in range(n-d+1):
     base=x*n+y
     indices=tuple((base+o for o in rotations[0]))
     region=len(self.regions)
     self.regions.append(indices)
     for p in indices:
      self.cover[p].append(region)
     for r in range(4):
      indices=tuple((base+o for o in rotations[r]))
      self.actions.append((indices,(x,y,r)))
      self.masks.append(sum((1<<c*j+target[p]for j,p in enumerate(indices))))
   State._geometry_cache=(key,self.regions,self.actions,self.masks,self.cover)
  self.order=list(range(len(self.actions)))if order is None else order
  self.counts=[sum((grid[p]==target[p]for p in indices))for indices in self.regions]
  self.stampmask=sum((1<<c*j+value for j,value in enumerate(stamp)))
  self.size=d*d
  self.all_actions=(1<<len(self.actions))-1
  self.target_bits=[[0]*c for _ in stamp]
  self.region_bits=[0]*len(self.regions)
  for rank,action in enumerate(self.order):
   bit=1<<rank
   self.region_bits[action>>2]|=bit
   for j,p in enumerate(self.actions[action][0]):
    self.target_bits[j][target[p]]|=bit
  self.old_planes=[0]*4
  for region,count in enumerate(self.counts):
   value=self.size-count
   for plane in range(4):
    if value&1<<plane:
     self.old_planes[plane]|=self.region_bits[region]
 def gain(self,action):
  return(self.stampmask&self.masks[action]).bit_count()-self.counts[action>>2]
 def apply(self,action):
  indices,_=self.actions[action]
  grid,stamp,target=(self.grid,self.stamp,self.target)
  changed={}
  for j,p in enumerate(indices):
   old,new=(grid[p],stamp[j])
   stamp[j],grid[p]=(old,new)
   delta=(new==target[p])-(old==target[p])
   self.matches+=delta
   if delta:
    for region in self.cover[p]:
     changed[region]=changed.get(region,0)+delta
  counts,planes,region_bits=(self.counts,self.old_planes,self.region_bits)
  size=self.size
  for region,delta in changed.items():
   if not delta:
    continue
   old=counts[region]
   new=old+delta
   counts[region]=new
   changed_planes=size-old^size-new
   bits=region_bits[region]
   while changed_planes:
    bit=changed_planes&-changed_planes
    planes[bit.bit_length()-1]^=bits
    changed_planes^=bit
  c=self.c
  self.stampmask=sum((1<<c*j+value for j,value in enumerate(stamp)))
 def best_candidates(self):
  planes=[0]*5
  for j,color in enumerate(self.stamp):
   carry=self.target_bits[j][color]
   plane=0
   while carry:
    previous=planes[plane]
    planes[plane]=previous^carry
    carry&=previous
    plane+=1
  carry=0
  for plane in range(4):
   a,b=(planes[plane],self.old_planes[plane])
   different=a^b
   planes[plane]=different^carry
   carry=a&b|different&carry
  planes[4]=carry
  candidates,value=(self.all_actions,0)
  for plane in range(4,-1,-1):
   hits=candidates&planes[plane]
   if hits:
    candidates=hits
    value|=1<<plane
  return(value-self.size,candidates)
 def best(self):
  gain,candidates=self.best_candidates()
  rank=(candidates&-candidates).bit_length()-1
  return(gain,self.order[rank])
 def escape(self,rng,width=64):
  mask,counts=(self.stampmask,self.counts)
  candidates=[(mask&m).bit_count()-counts[i>>2]for i,m in enumerate(self.masks)]
  eligible=[i for i,g in enumerate(candidates)if g>=-2]
  rng.shuffle(eligible)
  top=sorted(eligible,key=lambda i:candidates[i],reverse=True)[:8]
  ordered=top+eligible
  seen,tried=(set(),set())
  best_total,pair=(0,None)
  examined=0
  saved_counts=self.counts[:]
  saved_planes=self.old_planes[:]
  saved_matches=self.matches
  for first in ordered:
   if first in tried:
    continue
   tried.add(first)
   indices,_=self.actions[first]
   outgoing=tuple((self.grid[p]for p in indices))
   signature=(outgoing,candidates[first])
   if signature in seen:
    continue
   seen.add(signature)
   first_gain=candidates[first]
   self.apply(first)
   second_gain,second=self.best()
   total=first_gain+second_gain
   grid,stamp=(self.grid,self.stamp)
   for j,p in enumerate(indices):
    stamp[j],grid[p]=(grid[p],stamp[j])
   self.counts[:]=saved_counts
   self.old_planes[:]=saved_planes
   self.matches=saved_matches
   self.stampmask=mask
   if total>best_total:
    best_total,pair=(total,(first,second))
   examined+=1
   if examined>=width:
    break
  return pair
def solve_lookahead(n,d,c,k,grid,target,stamp):
 seed=n*101+d*19+c*7+k
 for p in range(0,len(grid),11):
  seed=seed*131+grid[p]*7+target[p]&4294967295
 best_matches,best_operations=(-1,[])
 for restart in range(8):
  rng=random.Random(seed+restart*87917)
  order=list(range(4*(n-d+1)**2))
  if restart:
   rng.shuffle(order)
  state=State(n,d,c,grid.copy(),target,stamp.copy(),order)
  operations=[]
  while len(operations)<k and state.matches<state.limit:
   gain,action=state.best()
   if gain>0:
    state.apply(action)
    operations.append(state.actions[action][1])
   elif len(operations)+2<=k:
    pair=state.escape(rng)
    if pair is None:
     break
    for action in pair:
     state.apply(action)
     operations.append(state.actions[action][1])
   else:
    break
  matches=sum((a==t for a,t in zip(state.grid,target)))
  if matches>best_matches:
   best_matches,best_operations=(matches,operations)
  if best_matches==state.limit:
   break
 return best_operations
def construct(n,d,c,k,grid,target,stamp):
 limit=color_bound(grid+stamp,target)
 if sum((a==b for a,b in zip(grid,target)))==limit:
  return[]
 indices,codes,operations,coverage,patches=build(n,d,target)
 width=n-d+1
 best_matches=-1
 best_ops=[]
 for search in(solve_plateau,solve_lookahead,solve_productive):
  ops=search(n,d,c,k,grid[:],target,stamp[:])
  final,buffer=(grid[:],stamp[:])
  for x,y,r in ops:
   action=(x*width+y)*4+r
   transition(final,buffer,indices[action])
  matches=sum((a==b for a,b in zip(final,target)))
  if matches>best_matches:
   best_matches,best_ops=(matches,ops)
  if matches==limit:
   break
 return best_ops
'Packed greedy with exact positive-total two-move plateau escapes.'
import random
import sys
class ProductiveState(State):
 def escape(self,rng,width=64,min_gain=-2):
  mask,counts=(self.stampmask,self.counts)
  candidates=[(mask&m).bit_count()-counts[i>>2]for i,m in enumerate(self.masks)]
  eligible=[i for i,g in enumerate(candidates)if g>=min_gain]
  rng.shuffle(eligible)
  top=sorted(eligible,key=lambda i:candidates[i],reverse=True)[:8]
  ordered=top+eligible
  seen,tried=(set(),set())
  best_total,pair=(0,None)
  examined=0
  saved_counts=self.counts[:]
  saved_planes=self.old_planes[:]
  saved_matches=self.matches
  for first in ordered:
   if first in tried:
    continue
   tried.add(first)
   indices,_=self.actions[first]
   outgoing=tuple((self.grid[p]for p in indices))
   signature=(outgoing,candidates[first])
   if signature in seen:
    continue
   seen.add(signature)
   first_gain=candidates[first]
   self.apply(first)
   second_gain,second=self.best()
   total=first_gain+second_gain
   grid,stamp=(self.grid,self.stamp)
   for j,p in enumerate(indices):
    stamp[j],grid[p]=(grid[p],stamp[j])
   self.counts[:]=saved_counts
   self.old_planes[:]=saved_planes
   self.matches=saved_matches
   self.stampmask=mask
   if total>best_total:
    best_total,pair=(total,(first,second))
   examined+=1
   if examined>=width:
    break
  return pair
def solve_productive(n,d,c,k,grid,target,stamp):
 state=ProductiveState(n,d,c,grid,target,stamp)
 seed=n*101+d*19+c*7+k
 for p in range(0,len(grid),11):
  seed=seed*131+grid[p]*7+target[p]&4294967295
 rng=random.Random(seed)
 operations=[]
 while len(operations)<k and state.matches<state.limit:
  gain,action=state.best()
  if gain>0:
   if len(operations)+2<=k:
    pair=state.escape(rng,width=8,min_gain=max(1,gain-1))
    if pair is not None:
     action=pair[0]
   state.apply(action)
   operations.append(state.actions[action][1])
  elif len(operations)+2<=k:
   pair=state.escape(rng)
   if pair is None:
    break
   for action in pair:
    state.apply(action)
    operations.append(state.actions[action][1])
  else:
   break
 return operations
def seq_transition(state,nn,indices):
 for j,pos in enumerate(indices):
  state[nn+j],state[pos]=(state[pos],state[nn+j])
def best_action(state,wishes,actions,nn,dd,current=-1,allow_zero=False):
 grid,wanted=(state[:nn],wishes[:nn])
 losses=[value==goal for value,goal in zip(grid,wanted)]
 rows=[]
 for j in range(dd):
  carried,goal=(state[nn+j],wishes[nn+j])
  fixed_loss=carried==goal
  rows.append([(carried==desire)+(value==goal)-loss-fixed_loss for value,desire,loss in zip(grid,wanted,losses)])
 best_id,best_gain=(-1,0)
 if current>=0:
  old=sum((rows[j][pos]for j,pos in enumerate(actions[current][0])))
  if old>=0:
   best_id,best_gain=(current,old)
 if dd==4:
  g0,g1,g2,g3=rows
  for aid,(p,_)in enumerate(actions):
   gain=g0[p[0]]+g1[p[1]]+g2[p[2]]+g3[p[3]]
   if gain>best_gain or(allow_zero and best_id<0 and(gain==best_gain)):
    best_id,best_gain=(aid,gain)
 else:
  g0,g1,g2,g3,g4,g5,g6,g7,g8=rows
  for aid,(p,_)in enumerate(actions):
   gain=g0[p[0]]+g1[p[1]]+g2[p[2]]+g3[p[3]]+g4[p[4]]+g5[p[5]]+g6[p[6]]+g7[p[7]]+g8[p[8]]
   if gain>best_gain or(allow_zero and best_id<0 and(gain==best_gain)):
    best_id,best_gain=(aid,gain)
 return(best_id,best_gain)
def greedy(n,d,k,grid,target,stamp,actions):
 nn,dd=(n*n,d*d)
 state,wishes=(grid+stamp,target+[-1]*dd)
 sequence=[]
 for _ in range(k):
  aid,gain=best_action(state,wishes,actions,nn,dd)
  if gain<=0:
   break
  seq_transition(state,nn,actions[aid][0])
  sequence.append(aid)
 return sequence
_REFINE_GEOMETRY={}
_REFINE_COVER_BITS={}
class RefineState:
 def __init__(self,n,d,initial,target,actions,order):
  nn,dd=(n*n,d*d)
  self.nn,self.dd=(nn,dd)
  self.grid,self.stamp=(initial[:nn],initial[nn:])
  self.wishes,self.wstamp=(target[:],[6]*dd)
  self.actions,self.order=(actions,order)
  size=len(actions)
  self.all_bits=(1<<size)-1
  key=(n,d)
  geometry=_REFINE_GEOMETRY.get(key)
  if geometry is None:
   positions=[[0]*nn for _ in range(dd)]
   region_bits=[15<<4*r for r in range(size//4)]
   regions=[actions[i][0]for i in range(0,size,4)]
   cover=[[]for _ in range(nn)]
   for r,patch in enumerate(regions):
    for p in patch:
     cover[p].append(r)
   for aid,(patch,_)in enumerate(actions):
    bit=1<<aid
    for j,p in enumerate(patch):
     positions[j][p]|=bit
   geometry=(positions,region_bits,regions,cover)
   _REFINE_GEOMETRY[key]=geometry
  self.positions,self.region_bits,self.regions,self.cover=geometry
  cover_bits=_REFINE_COVER_BITS.get(key)
  if cover_bits is None:
   cover_bits=[sum((self.region_bits[r]for r in ids))for ids in self.cover]
   _REFINE_COVER_BITS[key]=cover_bits
  self.cover_bits=cover_bits
  self.values=[[0]*7 for _ in range(dd)]
  self.goals=[[0]*7 for _ in range(dd)]
  for j in range(dd):
   values,goals=(self.values[j],self.goals[j])
   for p,mask in enumerate(self.positions[j]):
    values[self.grid[p]]|=mask
    goals[self.wishes[p]]|=mask
  self.tie_masks=[0]*size.bit_length()
  for rank,aid in enumerate(order):
   bit=1<<aid
   while rank:
    low=rank&-rank
    self.tie_masks[low.bit_length()-1]|=bit
    rank^=low
  self.counts=[sum((self.grid[p]==self.wishes[p]for p in patch))for patch in self.regions]
  self.old_planes=[0]*5
  for r,count in enumerate(self.counts):
   value=dd-count
   for plane in range(4):
    if value&1<<plane:
     self.old_planes[plane]|=self.region_bits[r]
  self.counts=None
 def apply(self,action,wishes=False):
  if wishes:
   grid,stamp,bits,opposite=(self.wishes,self.wstamp,self.goals,self.grid)
  else:
   grid,stamp,bits,opposite=(self.grid,self.stamp,self.values,self.wishes)
  positions=self.positions
  planes,cover_bits=(self.old_planes,self.cover_bits)
  for j,p in enumerate(self.actions[action][0]):
   old,new=(grid[p],stamp[j])
   if old!=new:
    for ref in range(self.dd):
     mask=positions[ref][p]
     bits[ref][old]^=mask
     bits[ref][new]^=mask
    delta=(new==opposite[p])-(old==opposite[p])
    if delta:
     carry=cover_bits[p]
     plane=0
     if delta>0:
      while carry:
       previous=planes[plane]
       planes[plane]=previous^carry
       carry&=~previous
       plane+=1
     else:
      while carry:
       previous=planes[plane]
       planes[plane]=previous^carry
       carry&=previous
       plane+=1
    stamp[j],grid[p]=(old,new)
 def best(self):
  planes=[0]*5
  for j in range(self.dd):
   for carry in(self.values[j][self.wstamp[j]],self.goals[j][self.stamp[j]]):
    plane=0
    while carry:
     old=planes[plane]
     planes[plane]=old^carry
     carry&=old
     plane+=1
  carry=0
  for plane in range(5):
   a,b=(planes[plane],self.old_planes[plane])
   different=a^b
   planes[plane]=different^carry
   carry=a&b|different&carry
  candidates,value=(self.all_bits,0)
  for plane in range(4,-1,-1):
   hits=candidates&planes[plane]
   if hits:
    candidates=hits
    value|=1<<plane
  gain=value-self.dd-sum((a==b for a,b in zip(self.stamp,self.wstamp)))
  if gain<0:
   return(-1,0)
  for mask in reversed(self.tie_masks):
   if not candidates&candidates-1:
    break
   preferred=candidates&~mask
   if preferred:
    candidates=preferred
  return((candidates&-candidates).bit_length()-1,gain)
def refine(n,d,k,initial,target,actions,sequence,passes=8,offset=0,seed_offset=0):
 nn,dd=(n*n,d*d)
 limit=color_bound(initial,target)
 seed=sum(((i+1)*v for i,v in enumerate(initial)))+k*131+seed_offset
 rng=random.Random(seed)
 for _ in range(offset):
  rng.shuffle(list(range(len(actions))))
 for iteration in range(passes):
  sequence=sequence+[-1]*min(8,k-len(sequence))
  final=initial[:]
  for action in sequence:
   if action>=0:
    seq_transition(final,nn,actions[action][0])
  if sum((a==b for a,b in zip(final,target)))==limit:
   return[action for action in sequence if action>=0]
  order=list(range(len(actions)))
  rng.shuffle(order)
  state=RefineState(n,d,final,target,actions,order)
  for i in range(len(sequence)-1,-1,-1):
   old=sequence[i]
   if old>=0:
    state.apply(old)
   chosen,_=state.best()
   sequence[i]=chosen
   if chosen>=0:
    state.apply(chosen,wishes=True)
  sequence=[action for action in sequence if action>=0]
 return sequence
class SequenceState:
 def __init__(self,initial,target,actions,sequence,nn):
  self.nn=nn
  self.actions=actions
  self.sequence=sequence[:]
  self.prefix=[initial[:]]
  for aid in sequence:
   state=self.prefix[-1][:]
   if aid>=0:
    seq_transition(state,nn,actions[aid][0])
   self.prefix.append(state)
  self.wishes=[None]*(len(sequence)+1)
  self.wishes[-1]=target+[-1]*(len(initial)-nn)
  for i in range(len(sequence)-1,-1,-1):
   wanted=self.wishes[i+1][:]
   if sequence[i]>=0:
    seq_transition(wanted,nn,actions[sequence[i]][0])
   self.wishes[i]=wanted
  self.score=sum((x==y for x,y in zip(self.prefix[-1],target)))
 def delta(self,i,replacements):
  nn,actions=(self.nn,self.actions)
  outgoing=self.prefix[i][:]
  affected=set(range(nn,len(outgoing)))
  for old,new in zip(self.sequence[i:i+len(replacements)],replacements):
   if old>=0:
    affected.update(actions[old][0])
   if new>=0:
    indices=actions[new][0]
    affected.update(indices)
    seq_transition(outgoing,nn,indices)
  previous=self.prefix[i+len(replacements)]
  wishes=self.wishes[i+len(replacements)]
  return sum(((outgoing[p]==wishes[p])-(previous[p]==wishes[p])for p in affected))
 def accept(self,i,replacements,delta):
  nn,actions=(self.nn,self.actions)
  self.sequence[i:i+len(replacements)]=replacements
  for j in range(i,len(self.sequence)):
   state=self.prefix[j][:]
   aid=self.sequence[j]
   if aid>=0:
    seq_transition(state,nn,actions[aid][0])
   self.prefix[j+1]=state
  for j in range(i+len(replacements)-1,-1,-1):
   wanted=self.wishes[j+1][:]
   aid=self.sequence[j]
   if aid>=0:
    seq_transition(wanted,nn,actions[aid][0])
   self.wishes[j]=wanted
  self.score+=delta
def pair_repair(n,d,k,initial,target,actions,sequence,proposals=None):
 if k<2:
  return sequence
 nn,dd=(n*n,d*d)
 state=SequenceState(initial,target,actions,sequence+[-1]*(k-len(sequence)),nn)
 if state.score==color_bound(initial,target):
  return sequence
 rng=random.Random(sum(((i+7)*v for i,v in enumerate(initial)))+k*977+9167)
 width=n-d+1
 if proposals is None:
  proposals=min(2400,max(160,450000//nn))
 for step in range(proposals):
  i=rng.randrange(k-1)
  fixed_slot=step%2
  old=state.sequence[i+fixed_slot]
  mode=rng.randrange(5)
  if mode<2 and old>=0:
   x,y,r=actions[old][1]
   x=min(width-1,max(0,x+rng.choice((-2,-1,0,0,1,2))))
   y=min(width-1,max(0,y+rng.choice((-2,-1,0,0,1,2))))
   action=(x*width+y)*4+rng.randrange(4)
  elif mode==4:
   action=-1
  else:
   action=rng.randrange(len(actions))
  if fixed_slot==0:
   before=state.prefix[i][:]
   if action>=0:
    seq_transition(before,nn,actions[action][0])
   second,_=best_action(before,state.wishes[i+2],actions,nn,dd,current=state.sequence[i+1],allow_zero=True)
   replacements=[action,second]
  else:
   wished=state.wishes[i+2][:]
   if action>=0:
    seq_transition(wished,nn,actions[action][0])
   first,_=best_action(state.prefix[i],wished,actions,nn,dd,current=state.sequence[i],allow_zero=True)
   replacements=[first,action]
  if state.sequence[i:i+2]==replacements:
   continue
  delta=state.delta(i,replacements)
  if delta>0 or(delta==0 and rng.randrange(8)==0):
   state.accept(i,replacements,delta)
   if state.score==color_bound(initial,target):
    break
 return[aid for aid in state.sequence if aid>=0]
def operation_gain(state,action):
 if action<0:
  return 0
 gain=0
 for j,p in enumerate(state.actions[action][0]):
  v,w=(state.stamp[j],state.grid[p])
  a,b=(state.wishes[p],state.wstamp[j])
  gain+=(v==a)+(w==b)-(w==a)-(v==b)
 return gain
def refine_trial(state,action,wishes=False):
 if action<0:
  return None
 if wishes:
  grid,stamp,bits=(state.wishes,state.wstamp,state.goals)
 else:
  grid,stamp,bits=(state.grid,state.stamp,state.values)
 patch=state.actions[action][0]
 undo=(wishes,patch,[grid[p]for p in patch],stamp[:],[row[:]for row in bits],state.counts[:]if state.counts is not None else None,state.old_planes[:])
 state.apply(action,wishes=wishes)
 return undo
def refine_restore(state,undo):
 if undo is None:
  return
 wishes,patch,colors,stamp,bits,counts,planes=undo
 grid=state.wishes if wishes else state.grid
 for p,color in zip(patch,colors):
  grid[p]=color
 if wishes:
  state.wstamp,state.goals=(stamp,bits)
 else:
  state.stamp,state.values=(stamp,bits)
 state.counts,state.old_planes=(counts,planes)
def optimize_pair(state,first,second,candidates):
 best=operation_gain(state,first)
 undo=refine_trial(state,first)
 best+=operation_gain(state,second)
 refine_restore(state,undo)
 answer=(first,second)
 if best<0:
  best,answer=(0,(-1,-1))
 for fixed,side in candidates:
  gain=operation_gain(state,fixed)
  undo=refine_trial(state,fixed,wishes=bool(side))
  chosen,other=state.best()
  refine_restore(state,undo)
  total=gain+other
  if total>=best:
   best=total
   answer=(chosen,fixed)if side else(fixed,chosen)
 return answer
def pair_sweep(n,d,k,initial,target,actions,sequence,passes=4,width=32):
 nn=n*n
 side_len=n-d+1
 rng=random.Random(sum(((i+13)*v for i,v in enumerate(initial)))+k*691+7147)
 for iteration in range(passes):
  sequence=sequence+[-1]*min(8,k-len(sequence))
  final=initial[:]
  for action in sequence:
   if action>=0:
    seq_transition(final,nn,actions[action][0])
  if sum((a==b for a,b in zip(final,target)))==color_bound(initial,target):
   return[action for action in sequence if action>=0]
  order=list(range(len(actions)))
  rng.shuffle(order)
  state=RefineState(n,d,final,target,actions,order)
  i=len(sequence)-1
  if iteration%2 and i>=0:
   old=sequence[i]
   if old>=0:
    state.apply(old)
   chosen,_=state.best()
   sequence[i]=chosen
   if chosen>=0:
    state.apply(chosen,wishes=True)
   i-=1
  while i>=1:
   first,second=(sequence[i-1],sequence[i])
   if second>=0:
    state.apply(second)
   if first>=0:
    state.apply(first)
   candidates=[(first,0),(second,1),(-1,0),(-1,1)]
   for _ in range(width):
    side=rng.randrange(2)
    old=second if side else first
    mode=rng.randrange(4)
    if mode==0 and old>=0:
     x,y,r=actions[old][1]
     x=min(side_len-1,max(0,x+rng.choice((-1,0,1))))
     y=min(side_len-1,max(0,y+rng.choice((-1,0,1))))
     candidate=(x*side_len+y)*4+rng.randrange(4)
    elif mode==1:
     candidate=rng.choice(sequence)
    else:
     candidate=rng.randrange(len(actions))
    candidates.append((candidate,side))
   first,second=optimize_pair(state,first,second,candidates)
   sequence[i-1],sequence[i]=(first,second)
   if second>=0:
    state.apply(second,wishes=True)
   if first>=0:
    state.apply(first,wishes=True)
   i-=2
  if i==0:
   old=sequence[0]
   if old>=0:
    state.apply(old)
   sequence[0],_=state.best()
  sequence=[action for action in sequence if action>=0]
 return sequence
def iterated_refine(n,d,k,initial,target,actions,sequence):
 if n>16:
  return sequence
 nn=n*n
 def evaluate(path):
  final=initial[:]
  for action in path:
   if action>=0:
    seq_transition(final,nn,actions[action][0])
  return sum((a==b for a,b in zip(final,target)))
 best_score=evaluate(sequence)
 limit=color_bound(initial,target)
 if best_score==limit:
  return sequence
 rng=random.Random(sum(((i+29)*v for i,v in enumerate(initial)))+k*2281)
 best=sequence[:]
 width=n-d+1
 restarts=max(2,min(8,9000//(nn+6*k)))
 for restart in range(restarts):
  candidate=best+[-1]*min(8,k-len(best))
  positions=rng.sample(range(len(candidate)),min(len(candidate),2+restart%6))
  for position in positions:
   old=candidate[position]
   mode=rng.randrange(4)
   if old>=0 and mode<2:
    x,y,r=actions[old][1]
    x=max(0,min(width-1,x+rng.choice((-2,-1,0,1,2))))
    y=max(0,min(width-1,y+rng.choice((-2,-1,0,1,2))))
    candidate[position]=(x*width+y)*4+rng.randrange(4)
   elif mode==2:
    candidate[position]=-1
   else:
    candidate[position]=rng.randrange(len(actions))
  candidate=refine(n,d,k,initial,target,actions,candidate,passes=4,seed_offset=37307*(restart+1))
  score=evaluate(candidate)
  if score>=best_score:
   best,best_score=(candidate,score)
   if score==limit:
    break
 return best
class WeightedState(State):
 def __init__(self,n,d,c,grid,target,stamp,order=None):
  super().__init__(n,d,c,grid,target,stamp,order)
  self.weights=[2 if min(p//n,p%n,n-1-p//n,n-1-p%n)<d-1 else 1 for p in range(n*n)]
  self.size=2*d*d
  self.heavy_bits=[[0]*c for _ in stamp]
  for rank,action in enumerate(self.order):
   bit=1<<rank
   for j,p in enumerate(self.actions[action][0]):
    if self.weights[p]==2:
     self.heavy_bits[j][target[p]]|=bit
  self.counts=[sum((self.weights[p]for p in positions if grid[p]==target[p]))for positions in self.regions]
  self.old_planes=[0]*6
  for region,count in enumerate(self.counts):
   value=self.size-count
   for plane in range(6):
    if value&1<<plane:
     self.old_planes[plane]|=self.region_bits[region]
 def gain(self,action):
  return sum((self.weights[p]for j,p in enumerate(self.actions[action][0])if self.stamp[j]==self.target[p]))-self.counts[action>>2]
 def apply(self,action):
  indices,_=self.actions[action]
  grid,stamp,target=(self.grid,self.stamp,self.target)
  changed={}
  for j,p in enumerate(indices):
   old,new=(grid[p],stamp[j])
   stamp[j],grid[p]=(old,new)
   delta=(new==target[p])-(old==target[p])
   self.matches+=delta
   if delta:
    delta*=self.weights[p]
    for region in self.cover[p]:
     changed[region]=changed.get(region,0)+delta
  counts,planes,region_bits=(self.counts,self.old_planes,self.region_bits)
  size=self.size
  for region,delta in changed.items():
   if not delta:
    continue
   old=counts[region]
   new=old+delta
   counts[region]=new
   changed_planes=size-old^size-new
   bits=region_bits[region]
   while changed_planes:
    bit=changed_planes&-changed_planes
    planes[bit.bit_length()-1]^=bits
    changed_planes^=bit
  c=self.c
  self.stampmask=sum((1<<c*j+value for j,value in enumerate(stamp)))
 def best_candidates(self):
  planes=[0]*6
  for j,color in enumerate(self.stamp):
   heavy=self.heavy_bits[j][color]
   for plane,carry in((0,self.target_bits[j][color]^heavy),(1,heavy)):
    while carry:
     previous=planes[plane]
     planes[plane]=previous^carry
     carry&=previous
     plane+=1
  carry=0
  for plane in range(6):
   a,b=(planes[plane],self.old_planes[plane])
   different=a^b
   planes[plane]=different^carry
   carry=a&b|different&carry
  candidates,value=(self.all_actions,0)
  for plane in range(5,-1,-1):
   hits=candidates&planes[plane]
   if hits:
    candidates=hits
    value|=1<<plane
  return(value-self.size,candidates)
def solve_weighted(n,d,c,k,initial,target,start_stamp):
 seed=7418729
 for value in initial+target+start_stamp:
  seed=(seed^value)*1000003&4294967295
 rng=random.Random(seed)
 order=list(range(4*(n-d+1)**2))
 initial_score=sum((a==b for a,b in zip(initial,target)))
 best_score,answer=(initial_score,[])
 limit=color_bound(initial+start_stamp,target)
 if best_score==limit:
  return answer
 for restart in range(4):
  if restart:
   rng.shuffle(order)
  state=WeightedState(n,d,c,initial[:],target,start_stamp[:],order[:])
  path,seen,score=([],set(),initial_score)
  for _ in range(k):
   seen.add(tuple(state.stamp))
   gain,candidates=state.best_candidates()
   if gain<0:
    break
   chosen=-1
   while candidates:
    bit=candidates&-candidates
    action=state.order[bit.bit_length()-1]
    if gain>0 or tuple((state.grid[p]for p in state.actions[action][0]))not in seen:
     chosen=action
     break
    candidates^=bit
   if chosen<0:
    break
   if gain>0:
    seen.clear()
   score+=sum(((state.stamp[j]==target[p])-(state.grid[p]==target[p])for j,p in enumerate(state.actions[chosen][0])))
   state.apply(chosen)
   path.append(state.actions[chosen][1])
   if score>best_score:
    best_score,answer=(score,path[:])
   if best_score==limit:
    return answer
 return answer
def construct_pool(n,d,c,k,grid,target,stamp):
 limit=color_bound(grid+stamp,target)
 initial_score=sum((a==b for a,b in zip(grid,target)))
 if initial_score==limit:
  return[(limit,[])]
 indices,codes,operations,coverage,patches=build(n,d,target)
 width=n-d+1
 candidates=[]
 for search in(solve_plateau,solve_lookahead,solve_productive,solve_weighted):
  ops=search(n,d,c,k,grid[:],target,stamp[:])
  final,buffer=(grid[:],stamp[:])
  for x,y,r in ops:
   action=(x*width+y)*4+r
   transition(final,buffer,indices[action])
  matches=sum((a==b for a,b in zip(final,target)))
  candidates.append((matches,ops))
  if matches==limit:
   break
 candidates.sort(key=lambda row:row[0],reverse=True)
 return candidates
def solve_parent(n,d,c,k,grid,target,stamp):
 pool=construct_pool(n,d,c,k,grid[:],target,stamp[:])
 if pool[0][0]==color_bound(grid+stamp,target):
  return pool[0][1]
 indices,_,ops,_,_=build(n,d,target)
 actions=list(zip(indices,ops))
 width=n-d+1
 initial=grid+stamp
 best_score,best_sequence=(-1,[])
 for _,operations in pool[:4]:
  sequence=[(x*width+y)*4+r for x,y,r in operations]
  sequence=refine(n,d,k,initial,target,actions,sequence,passes=2)
  state=initial[:]
  for aid in sequence:
   seq_transition(state,n*n,actions[aid][0])
  score=sum((a==b for a,b in zip(state,target)))
  if score>best_score:
   best_score,best_sequence=(score,sequence)
 sequence=refine(n,d,k,initial,target,actions,best_sequence,passes=6,offset=2)
 sequence=pair_sweep(n,d,k,initial,target,actions,sequence)
 sequence=pair_repair(n,d,k,initial,target,actions,sequence)
 sequence=refine(n,d,k,initial,target,actions,sequence,passes=2)
 sequence=iterated_refine(n,d,k,initial,target,actions,sequence)
 return[actions[aid][1]for aid in sequence]
def clone_state(state):
 child=object.__new__(State)
 child.__dict__=state.__dict__.copy()
 child.grid=state.grid[:]
 child.stamp=state.stamp[:]
 child.counts=state.counts[:]
 child.old_planes=state.old_planes[:]
 return child
def beam_actions(state,rng):
 mask,counts=(state.stampmask,state.counts)
 gains=[(mask&m).bit_count()-counts[i>>2]for i,m in enumerate(state.masks)]
 best=max(gains)
 groups=[[],[],[]]
 for action,gain in enumerate(gains):
  distance=best-gain
  if distance<3:
   groups[distance].append(action)
 selected=[]
 for group,limit in zip(groups,(4,3,1)):
  rng.shuffle(group)
  seen={}
  for action in group:
   outgoing=tuple((state.grid[p]for p in state.actions[action][0]))
   if seen.get(outgoing,0)>=2:
    continue
   seen[outgoing]=seen.get(outgoing,0)+1
   selected.append((action,gains[action]))
   limit-=1
   if limit==0:
    break
 return selected
def finite_beam(n,d,c,k,grid,target,stamp,width=24):
 initial=State(n,d,c,grid[:],target,stamp[:])
 base_score=sum((a==b for a,b in zip(grid,target)))
 supply=[0]*c
 wanted=[0]*c
 for color in grid+stamp:
  supply[color]+=1
 for color in target:
  wanted[color]+=1
 upper_gain=sum((min(a,b)for a,b in zip(supply,wanted)))-base_score
 if upper_gain<=0:
  return[]
 seed=47893+k*1009+n*79+d*13+c
 for value in grid+stamp:
  seed=seed*131+value&4294967295
 rng=random.Random(seed)
 beam=[(initial,0,[])]
 best_gain,best_path=(0,[])
 for depth in range(k):
  children=[]
  seen_states=set()
  for state,gain,path in beam:
   for action,delta in beam_actions(state,rng):
    if path and action==path[-1]:
     continue
    child=clone_state(state)
    child.apply(action)
    signature=bytes(child.grid)+bytes(child.stamp)
    if signature in seen_states:
     continue
    seen_states.add(signature)
    total=gain+delta
    new_path=path+[action]
    if total>best_gain:
     best_gain,best_path=(total,new_path)
     if best_gain==upper_gain:
      return[initial.actions[aid][1]for aid in best_path]
    future=max(0,child.best()[0])if depth+1<k else 0
    priority=total*2+future
    children.append((priority,total,child,new_path))
  if not children:
   break
  children.sort(key=lambda item:(item[0],item[1]),reverse=True)
  beam=[]
  carried_counts={}
  deferred=[]
  for priority,gain,state,path in children:
   key=tuple(state.stamp)
   if carried_counts.get(key,0)>=3:
    deferred.append((state,gain,path))
    continue
   carried_counts[key]=carried_counts.get(key,0)+1
   beam.append((state,gain,path))
   if len(beam)==width:
    break
  if len(beam)<width:
   beam.extend(deferred[:width-len(beam)])
 return[initial.actions[aid][1]for aid in best_path]
def exact_two(n,d,c,k,grid,target,stamp):
 state=State(n,d,c,grid[:],target,stamp[:])
 gain,action=state.best()
 best_gain,best_path=(max(0,gain),[action]if gain>0 else[])
 if k==1:
  return[state.actions[aid][1]for aid in best_path]
 ranked=[(state.gain(aid),aid)for aid in range(len(state.actions))]
 ranked.sort(reverse=True)
 for first_gain,first in ranked:
  if first_gain+d*d<=best_gain:
   break
  state.apply(first)
  second_gain,second=state.best()
  total=first_gain+second_gain
  state.apply(first)
  if total>best_gain:
   best_gain,best_path=(total,[first,second])
 return[state.actions[aid][1]for aid in best_path]
def construct_all(n,d,c,k,grid,target,stamp):
 if k<=2:
  return exact_two(n,d,c,k,grid,target,stamp)
 reference=solve_parent(n,d,c,k,grid[:],target,stamp[:])
 if k>24:
  return reference
 candidate=finite_beam(n,d,c,k,grid,target,stamp,width=24 if k<=12 else 12)
 indices,_,ops,_,_=build(n,d,target)
 actions=list(zip(indices,ops))
 width=n-d+1
 sequence=[(x*width+y)*4+r for x,y,r in candidate]
 sequence=refine(n,d,k,grid+stamp,target,actions,sequence)
 candidate=[actions[aid][1]for aid in sequence]
 best_score,best_ops=(-1,[])
 for operations in(reference,candidate):
  final,buffer=(grid[:],stamp[:])
  for x,y,r in operations:
   transition(final,buffer,indices[(x*width+y)*4+r])
  score=sum((a==b for a,b in zip(final,target)))
  if score>best_score:
   best_score,best_ops=(score,operations)
 return best_ops
def optimize_triple(state,first,middle,last,left,right):
 best=operation_gain(state,first)
 outer=refine_trial(state,first)
 best+=operation_gain(state,middle)
 inner=refine_trial(state,middle)
 best+=operation_gain(state,last)
 refine_restore(state,inner)
 refine_restore(state,outer)
 answer=(first,middle,last)
 for first in left:
  base=operation_gain(state,first)
  outer=refine_trial(state,first)
  for last in right:
   extra=operation_gain(state,last)
   inner=refine_trial(state,last,wishes=True)
   middle,gain=state.best()
   refine_restore(state,inner)
   total=base+extra+gain
   if total>=best:
    best=total
    answer=(first,middle,last)
  refine_restore(state,outer)
 return answer
def triple_refine(n,d,k,initial,target,actions,sequence,passes=2):
 if k<3:
  return sequence
 nn=n*n
 limit=color_bound(initial,target)
 size=n-d+1
 rng=random.Random(sum(((i+17)*v for i,v in enumerate(initial)))+k*1777+71983)
 for iteration in range(passes):
  sequence=sequence+[-1]*min(6,k-len(sequence))
  final=initial[:]
  for aid in sequence:
   if aid>=0:
    seq_transition(final,nn,actions[aid][0])
  if sum((a==b for a,b in zip(final,target)))==limit:
   return[aid for aid in sequence if aid>=0]
  order=list(range(len(actions)))
  rng.shuffle(order)
  state=RefineState(n,d,final,target,actions,order)
  i=len(sequence)-1
  for _ in range(iteration%3):
   if i<0:
    break
   old=sequence[i]
   if old>=0:
    state.apply(old)
   chosen,_=state.best()
   sequence[i]=chosen
   if chosen>=0:
    state.apply(chosen,wishes=True)
   i-=1
  while i>=2:
   first,middle,last=sequence[i-2:i+1]
   for aid in(last,middle,first):
    if aid>=0:
     state.apply(aid)
   preferred,_=state.best()
   pools=[]
   for old in(first,last):
    mode=rng.randrange(3)
    if mode==0 and old>=0:
     x,y,r=actions[old][1]
     x=min(size-1,max(0,x+rng.choice((-1,0,1))))
     y=min(size-1,max(0,y+rng.choice((-1,0,1))))
     trial=(x*size+y)*4+rng.randrange(4)
    elif mode==1:
     p=rng.randrange(nn)
     for _ in range(10):
      p=rng.randrange(nn)
      if state.wishes[p]<6 and state.grid[p]!=state.wishes[p]:
       break
     x=min(size-1,max(0,p//n-rng.randrange(d)))
     y=min(size-1,max(0,p%n-rng.randrange(d)))
     trial=(x*size+y)*4+rng.randrange(4)
    else:
     trial=rng.randrange(len(actions))
    pools.append(list(dict.fromkeys((old,-1,preferred,trial))))
   for ending in pools[1]:
    undo=refine_trial(state,ending,wishes=True)
    starting,_=state.best()
    refine_restore(state,undo)
    if starting not in pools[0]:
     pools[0].append(starting)
   first,middle,last=optimize_triple(state,first,middle,last,*pools)
   sequence[i-2:i+1]=(first,middle,last)
   for aid in(last,middle,first):
    if aid>=0:
     state.apply(aid,wishes=True)
   i-=3
  while i>=0:
   old=sequence[i]
   if old>=0:
    state.apply(old)
   chosen,_=state.best()
   sequence[i]=chosen
   if chosen>=0:
    state.apply(chosen,wishes=True)
   i-=1
  sequence=[aid for aid in sequence if aid>=0]
 return sequence
def solve_original_iterated(n,d,c,k,grid,target,stamp):
 operations=construct_all(n,d,c,k,grid[:],target,stamp[:])
 if k<=2:
  return operations
 indices,_,ops,_,_=build(n,d,target)
 actions=list(zip(indices,ops))
 side=n-d+1
 sequence=[(x*side+y)*4+r for x,y,r in operations]
 sequence=triple_refine(n,d,k,grid+stamp,target,actions,sequence)
 sequence=refine(n,d,k,grid+stamp,target,actions,sequence,passes=2)
 return[actions[aid][1]for aid in sequence]
def solve_retained_iterated(n,d,c,k,grid,target,stamp):
 if n>16 or k<=2:
  return solve_original_iterated(n,d,c,k,grid,target,stamp)
 initial=grid+stamp
 indices,_,ops,_,_=build(n,d,target)
 actions=list(zip(indices,ops))
 width=n-d+1
 def evaluate(sequence):
  final=initial[:]
  for aid in sequence:
   seq_transition(final,n*n,indices[aid])
  return sum((a==b for a,b in zip(final,target)))
 operations=construct(n,d,c,k,grid[:],target,stamp[:])
 base=[(x*width+y)*4+r for x,y,r in operations]
 base=refine(n,d,k,initial,target,actions,base)
 base=pair_sweep(n,d,k,initial,target,actions,base)
 base=pair_repair(n,d,k,initial,target,actions,base)
 base=refine(n,d,k,initial,target,actions,base,passes=2)
 perturbed=iterated_refine(n,d,k,initial,target,actions,base)
 if k<=24:
  beam=finite_beam(n,d,c,k,grid,target,stamp,width=24 if k<=12 else 12)
  beam=[(x*width+y)*4+r for x,y,r in beam]
  beam=refine(n,d,k,initial,target,actions,beam)
  beam_score=evaluate(beam)
  if beam_score>evaluate(base):
   base=beam
  if beam_score>evaluate(perturbed):
   perturbed=beam
 choices=[base]
 if perturbed!=base:
  choices.append(perturbed)
 best_score,best=(-1,None)
 for candidate in choices:
  candidate=triple_refine(n,d,k,initial,target,actions,candidate)
  candidate=refine(n,d,k,initial,target,actions,candidate,passes=2)
  candidate=anneal_walk(n,d,k,initial,target,actions,candidate)
  candidate=refine(n,d,k,initial,target,actions,candidate,passes=2)
  score=evaluate(candidate)
  if score>best_score:
   best_score,best=(score,candidate)
 return[ops[aid]for aid in best]
def solve_before_pair_annealing(n,d,c,k,grid,target,stamp):
 reference=solve_retained_iterated(n,d,c,k,grid,target,stamp)
 if n>6 or k<=24:
  return reference
 indices,_,ops,_,_=build(n,d,target)
 actions=list(zip(indices,ops))
 width=n-d+1
 def evaluate(operations):
  final,buffer=(grid[:],stamp[:])
  for x,y,r in operations:
   transition(final,buffer,indices[(x*width+y)*4+r])
  return sum((a==b for a,b in zip(final,target)))
 reference_score=evaluate(reference)
 if reference_score==color_bound(grid+stamp,target):
  return reference
 candidate=finite_beam(n,d,c,min(k,60),grid,target,stamp,width=96)
 sequence=[(x*width+y)*4+r for x,y,r in candidate]
 sequence=refine(n,d,k,grid+stamp,target,actions,sequence)
 sequence=anneal_walk(n,d,k,grid+stamp,target,actions,sequence)
 sequence=refine(n,d,k,grid+stamp,target,actions,sequence,passes=2)
 candidate=[actions[aid][1]for aid in sequence]
 return candidate if evaluate(candidate)>reference_score else reference
class PairWalker:
 def __init__(self,n,d,initial,target,actions,sequence,order):
  self.sequence=sequence[:]
  self.actions=actions
  self.position=0
  self.state=RefineState(n,d,initial,target,actions,order)
  final=initial[:]
  for aid in sequence:
   if aid>=0:
    seq_transition(final,n*n,actions[aid][0])
  self.score=sum((a==b for a,b in zip(final,target)))
  for aid in reversed(sequence[2:]):
   if aid>=0:
    self.state.apply(aid,wishes=True)
  self.boundary_score=sum((x==y for x,y in zip(self.state.grid+self.state.stamp,self.state.wishes+self.state.wstamp)))
 def move(self,position):
  if position>self.position:
   steps=range(self.position,position)
  else:
   steps=range(self.position-1,position-1,-1)
  for i in steps:
   a,b=(self.sequence[i],self.sequence[i+2])
   if a>=0:
    self.boundary_score+=operation_gain(self.state,a)
    self.state.apply(a)
   if b>=0:
    self.boundary_score+=operation_gain(self.state,b)
    self.state.apply(b,wishes=True)
  self.position=position
 def propose(self,fixed,side):
  state=self.state
  old=self.score-self.boundary_score
  gain=operation_gain(state,fixed)
  undo=refine_trial(state,fixed,wishes=bool(side))
  other,extra=state.best()
  refine_restore(state,undo)
  pair=(other,fixed)if side else(fixed,other)
  return(pair,gain+extra-old)
 def accept(self,pair,delta):
  self.sequence[self.position:self.position+2]=pair
  self.score+=delta
def anneal_walk(n,d,k,initial,target,actions,sequence,proposals=None):
 import math
 if k<3:
  return sequence
 limit=color_bound(initial,target)
 final=initial[:]
 for aid in sequence:
  if aid>=0:
   seq_transition(final,n*n,actions[aid][0])
 if sum((a==b for a,b in zip(final,target)))==limit:
  return[aid for aid in sequence if aid>=0]
 rng=random.Random(sum(((i+23)*v for i,v in enumerate(initial)))+k*1357+7751)
 order=list(range(len(actions)))
 rng.shuffle(order)
 sequence=sequence+[-1]*(k-len(sequence))
 walker=PairWalker(n,d,initial,target,actions,sequence,order)
 if walker.score==limit:
  return[aid for aid in sequence if aid>=0]
 if proposals is None:
  proposals=min(4000,max(300,900000//(n*n)))
 best_score,best=(walker.score,walker.sequence[:])
 period=max(1,proposals//4)
 position=rng.randrange(k-1)
 walker.move(position)
 direction=1
 size=n-d+1
 for step in range(proposals):
  if step and step%period==0:
   rng.shuffle(order)
   walker=PairWalker(n,d,initial,target,actions,best,order)
   position=rng.randrange(k-1)
   walker.move(position)
  side=step%2
  old=walker.sequence[position+side]
  mode=rng.randrange(5)
  if mode==0 and old>=0:
   x,y,r=actions[old][1]
   x=min(size-1,max(0,x+rng.choice((-2,-1,0,0,1,2))))
   y=min(size-1,max(0,y+rng.choice((-2,-1,0,0,1,2))))
   fixed=(x*size+y)*4+rng.randrange(4)
  elif mode==1:
   fixed=walker.state.best()[0]
  elif mode==4:
   fixed=-1
  else:
   fixed=rng.randrange(len(actions))
  pair,delta=walker.propose(fixed,side)
  temperature=0.4*(1-step%period/period)**2+0.04
  if delta>=0 or rng.random()<math.exp(delta/temperature):
   walker.accept(pair,delta)
   if walker.score>=best_score:
    best_score,best=(walker.score,walker.sequence[:])
    if best_score==limit:
     break
  if rng.randrange(16)==0:
   direction=-direction
  if not 0<=position+direction<k-1:
   direction=-direction
  position+=direction
  walker.move(position)
 return[aid for aid in best if aid>=0]
def solve_without_binary(n,d,c,k,grid,target,stamp):
 operations=solve_before_pair_annealing(n,d,c,k,grid[:],target,stamp[:])
 if k<=2 or n<=16:
  return operations
 indices,_,ops,_,_=build(n,d,target)
 actions=list(zip(indices,ops))
 size=n-d+1
 sequence=[(x*size+y)*4+r for x,y,r in operations]
 sequence=anneal_walk(n,d,k,grid+stamp,target,actions,sequence)
 sequence=refine(n,d,k,grid+stamp,target,actions,sequence,passes=2)
 return[actions[aid][1]for aid in sequence]
def binary_transitions():
 rotations=[]
 for r in range(4):
  table=[]
  for value in range(512):
   result=0
   for u in range(3):
    for v in range(3):
     x,y=((u,v),(v,2-u),(2-u,2-v),(2-v,u))[r]
     result|=(value>>u*3+v&1)<<x*3+y
   table.append(result)
  rotations.append(table)
 patches=[]
 for x in range(2):
  for y in range(2):
   base=4*x+y
   scatter=[(v&7)<<base|(v&56)<<base+1|(v&448)<<base+2 for v in range(512)]
   paint=[[scatter[v]for v in rotations[r]]for r in range(4)]
   patches.append((base,65535^scatter[511],paint))
 def expand(state):
  board,stamp=(state&65535,state>>16)
  for position,(base,mask,paint)in enumerate(patches):
   patch=board>>base&7|board>>base+1&56|board>>base+2&448
   retained=board&mask
   for rotation in range(4):
    child=retained|paint[rotation][stamp]|rotations[-rotation&3][patch]<<16
    yield(position*4+rotation,child)
 return expand
def binary_bfs(grid,target,stamp,k):
 initial=sum((v<<i for i,v in enumerate(grid+stamp)))
 wanted=sum((v<<i for i,v in enumerate(target)))
 if initial&65535==wanted:
  return[]
 required=initial.bit_count()-wanted.bit_count()
 if not 0<=required<=9:
  return None
 expand=binary_transitions()
 forward={initial:(None,None)}
 frontier=[initial]
 first_depth=min(3,k)
 def prefix(state):
  path=[]
  while forward[state][0]is not None:
   state,action=forward[state]
   path.append(action)
  return path[::-1]
 for _ in range(first_depth):
  next_layer=[]
  for state in frontier:
   for action,child in expand(state):
    if child in forward:
     continue
    forward[child]=(state,action)
    if child&65535==wanted:
     return prefix(child)
    next_layer.append(child)
  frontier=next_layer
 goals=[wanted|v<<16 for v in range(512)if v.bit_count()==required]
 backward={state:(None,None)for state in goals}
 frontier=goals
 for _ in range(min(2,k-first_depth)):
  next_layer=[]
  for state in frontier:
   for action,child in expand(state):
    if child in backward:
     continue
    backward[child]=(state,action)
    if child in forward:
     answer=prefix(child)
     while backward[child][0]is not None:
      child,action=backward[child]
      answer.append(action)
     return answer
    next_layer.append(child)
  frontier=next_layer
 return None
def solve_weighted_parent(n,d,c,k,grid,target,stamp):
 if n==4 and d==3 and(c==2):
  path=binary_bfs(grid,target,stamp,k)
  if path is not None:
   return[(aid//8,aid//4%2,aid%4)for aid in path]
 return solve_without_binary(n,d,c,k,grid,target,stamp)
class WeightedRefineState:
 def __init__(self,n,d,initial,target,weights,actions,order):
  nn,dd=(n*n,d*d)
  self.nn,self.dd=(nn,dd)
  self.grid,self.stamp=(initial[:nn],initial[nn:])
  self.wishes,self.wstamp=(target[:],[6]*dd)
  self.weights,self.wstamp_weights=(weights[:],[0]*dd)
  self.actions,self.order=(actions,order)
  self.all_bits=(1<<len(actions))-1
  key=(n,d)
  geometry=_REFINE_GEOMETRY.get(key)
  if geometry is None:
   positions=[[0]*nn for _ in range(dd)]
   region_bits=[15<<4*r for r in range(len(actions)//4)]
   regions=[actions[i][0]for i in range(0,len(actions),4)]
   cover=[[]for _ in range(nn)]
   for region,patch in enumerate(regions):
    for p in patch:
     cover[p].append(region)
   for aid,(patch,_)in enumerate(actions):
    bit=1<<aid
    for j,p in enumerate(patch):
     positions[j][p]|=bit
   geometry=(positions,region_bits,regions,cover)
   _REFINE_GEOMETRY[key]=geometry
  self.positions,self.region_bits,self.regions,self.cover=geometry
  self.values=[[0]*7 for _ in range(dd)]
  self.goals=[[0]*7 for _ in range(dd)]
  self.weight_bits=[[0]*3 for _ in range(dd)]
  for j in range(dd):
   values,goals,importance=(self.values[j],self.goals[j],self.weight_bits[j])
   for p,mask in enumerate(self.positions[j]):
    values[self.grid[p]]|=mask
    goals[self.wishes[p]]|=mask
    importance[self.weights[p]]|=mask
  self.tie_masks=[0]*len(actions).bit_length()
  for rank,aid in enumerate(order):
   bit=1<<aid
   while rank:
    low=rank&-rank
    self.tie_masks[low.bit_length()-1]|=bit
    rank^=low
  self.counts=[sum((self.weights[p]*(self.grid[p]==self.wishes[p])for p in positions))for positions in self.regions]
  self.old_planes=[0]*6
  for region,count in enumerate(self.counts):
   value=2*dd-count
   for plane in range(5):
    if value&1<<plane:
     self.old_planes[plane]|=self.region_bits[region]
 def apply(self,action,wishes=False):
  changed={}
  positions,cover,counts=(self.positions,self.cover,self.counts)
  if wishes:
   grid,stamp=(self.wishes,self.wstamp)
   weights,stamp_weights=(self.weights,self.wstamp_weights)
   for j,p in enumerate(self.actions[action][0]):
    old,new=(grid[p],stamp[j])
    old_weight,new_weight=(weights[p],stamp_weights[j])
    if old!=new:
     for ref in range(self.dd):
      mask=positions[ref][p]
      self.goals[ref][old]^=mask
      self.goals[ref][new]^=mask
    if old_weight!=new_weight:
     for ref in range(self.dd):
      mask=positions[ref][p]
      self.weight_bits[ref][old_weight]^=mask
      self.weight_bits[ref][new_weight]^=mask
    actual=self.grid[p]
    delta=new_weight*(actual==new)-old_weight*(actual==old)
    if delta:
     for region in cover[p]:
      changed[region]=changed.get(region,0)+delta
    stamp[j],grid[p]=(old,new)
    stamp_weights[j],weights[p]=(old_weight,new_weight)
  else:
   grid,stamp=(self.grid,self.stamp)
   for j,p in enumerate(self.actions[action][0]):
    old,new=(grid[p],stamp[j])
    if old==new:
     continue
    for ref in range(self.dd):
     mask=positions[ref][p]
     self.values[ref][old]^=mask
     self.values[ref][new]^=mask
    delta=self.weights[p]*((new==self.wishes[p])-(old==self.wishes[p]))
    if delta:
     for region in cover[p]:
      changed[region]=changed.get(region,0)+delta
    stamp[j],grid[p]=(old,new)
  for region,delta in changed.items():
   if not delta:
    continue
   previous=counts[region]
   counts[region]+=delta
   change=2*self.dd-previous^2*self.dd-counts[region]
   while change:
    bit=change&-change
    self.old_planes[bit.bit_length()-1]^=self.region_bits[region]
    change^=bit
 def best(self):
  planes=[0]*6
  for j in range(self.dd):
   match=self.goals[j][self.stamp[j]]
   parts=[(match&self.weight_bits[j][1],0),(match&self.weight_bits[j][2],1)]
   weight=self.wstamp_weights[j]
   if weight:
    parts.append((self.values[j][self.wstamp[j]],weight-1))
   for carry,plane in parts:
    while carry:
     old=planes[plane]
     planes[plane]=old^carry
     carry&=old
     plane+=1
  carry=0
  for plane in range(6):
   a,b=(planes[plane],self.old_planes[plane])
   different=a^b
   planes[plane]=different^carry
   carry=a&b|different&carry
  candidates,value=(self.all_bits,0)
  for plane in range(5,-1,-1):
   hits=candidates&planes[plane]
   if hits:
    candidates=hits
    value|=1<<plane
  stamp_loss=sum((w*(a==b)for w,a,b in zip(self.wstamp_weights,self.stamp,self.wstamp)))
  gain=value-2*self.dd-stamp_loss
  if gain<0:
   return(-1,0)
  for mask in reversed(self.tie_masks):
   if not candidates&candidates-1:
    break
   preferred=candidates&~mask
   if preferred:
    candidates=preferred
  return((candidates&-candidates).bit_length()-1,gain)
def weighted_refine(n,d,k,initial,target,weights,actions,sequence,passes=1):
 nn,dd=(n*n,d*d)
 seed=sum(((i+1)*v for i,v in enumerate(initial)))+k*131
 seed+=sum(((i+7)*weight for i,weight in enumerate(weights)))*17
 rng=random.Random(seed)
 for iteration in range(passes):
  sequence=sequence+[-1]*min(8,k-len(sequence))
  final=initial[:]
  for action in sequence:
   if action>=0:
    seq_transition(final,nn,actions[action][0])
  if all((a==b for a,b in zip(final,target))):
   return[action for action in sequence if action>=0]
  order=list(range(len(actions)))
  rng.shuffle(order)
  state=WeightedRefineState(n,d,final,target,weights,actions,order)
  for i in range(len(sequence)-1,-1,-1):
   old=sequence[i]
   if old>=0:
    state.apply(old)
   chosen,_=state.best()
   sequence[i]=chosen
   if chosen>=0:
    state.apply(chosen,wishes=True)
  sequence=[action for action in sequence if action>=0]
 return sequence
def solve_before_triple_walking(n,d,c,k,grid,target,stamp):
 reference=solve_weighted_parent(n,d,c,k,grid[:],target,stamp[:])
 if k<=2:
  return reference
 nn,dd=(n*n,d*d)
 indices,_,ops,_,_=build(n,d,target)
 actions=list(zip(indices,ops))
 side=n-d+1
 sequence=[(x*side+y)*4+r for x,y,r in reference]
 initial,final=(grid+stamp,grid+stamp)
 for aid in sequence:
  seq_transition(final,nn,indices[aid])
 best_score=sum((a==b for a,b in zip(final,target)))
 best_sequence=sequence
 supply,wanted=([0]*c,[0]*c)
 for color in initial:
  supply[color]+=1
 for color in target:
  wanted[color]+=1
 upper=sum((min(a,b)for a,b in zip(supply,wanted)))
 if best_score==upper:
  return reference
 coverage=[min(p,n-d)-max(0,p-d+1)+1 for p in range(n)]
 maximum=max(coverage)**2
 boundary=[1+(coverage[row]*coverage[col]<maximum)for row in range(n)for col in range(n)]
 unresolved=[1+(a!=b)for a,b in zip(final,target)]
 seen_weights=set()
 for weights in(unresolved,boundary):
  signature=tuple(weights)
  if min(weights)==max(weights)or signature in seen_weights:
   continue
  seen_weights.add(signature)
  candidate=weighted_refine(n,d,k,initial,target,weights,actions,sequence)
  candidate=refine(n,d,k,initial,target,actions,candidate,passes=2)
  final=initial[:]
  for aid in candidate:
   seq_transition(final,nn,indices[aid])
  score=sum((a==b for a,b in zip(final,target)))
  if score>best_score:
   best_score,best_sequence=(score,candidate)
   if score==upper:
    break
 return[ops[aid]for aid in best_sequence]
class TripleWalker:
 def __init__(self,n,d,initial,target,actions,sequence,order):
  self.sequence=sequence[:]
  self.actions=actions
  self.position=0
  self.state=RefineState(n,d,initial,target,actions,order)
  final=initial[:]
  for aid in sequence:
   if aid>=0:
    seq_transition(final,n*n,actions[aid][0])
  self.score=sum((a==b for a,b in zip(final,target)))
  for aid in reversed(sequence[3:]):
   if aid>=0:
    self.state.apply(aid,wishes=True)
  self.boundary_score=sum((x==y for x,y in zip(self.state.grid+self.state.stamp,self.state.wishes+self.state.wstamp)))
 def move(self,position):
  if position>self.position:
   steps=range(self.position,position)
  else:
   steps=range(self.position-1,position-1,-1)
  for i in steps:
   a,b=(self.sequence[i],self.sequence[i+3])
   if a>=0:
    self.boundary_score+=operation_gain(self.state,a)
    self.state.apply(a)
   if b>=0:
    self.boundary_score+=operation_gain(self.state,b)
    self.state.apply(b,wishes=True)
  self.position=position
 def informed(self,side):
  state=self.state
  opposite=self.sequence[self.position if side else self.position+2]
  wishes=not bool(side)
  undo=refine_trial(state,opposite,wishes=wishes)
  fixed,_=state.best()
  refine_restore(state,undo)
  return fixed
 def propose(self,first,last):
  state=self.state
  old=self.score-self.boundary_score
  gain=operation_gain(state,first)
  outer=refine_trial(state,first)
  gain+=operation_gain(state,last)
  inner=refine_trial(state,last,wishes=True)
  middle,extra=state.best()
  refine_restore(state,inner)
  refine_restore(state,outer)
  return((first,middle,last),gain+extra-old)
 def accept(self,triple,delta):
  self.sequence[self.position:self.position+3]=triple
  self.score+=delta
def anneal_triples(n,d,k,initial,target,actions,sequence,proposals=None):
 import math
 if k<3:
  return sequence
 limit=color_bound(initial,target)
 final=initial[:]
 for aid in sequence:
  if aid>=0:
   seq_transition(final,n*n,actions[aid][0])
 if sum((a==b for a,b in zip(final,target)))==limit:
  return[aid for aid in sequence if aid>=0]
 rng=random.Random(sum(((i+31)*v for i,v in enumerate(initial)))+k*1123+19271)
 order=list(range(len(actions)))
 rng.shuffle(order)
 sequence=sequence+[-1]*(k-len(sequence))
 walker=TripleWalker(n,d,initial,target,actions,sequence,order)
 if proposals is None:
  proposals=min(6000,max(600,1350000//(n*n)))
 best_score,best=(walker.score,walker.sequence[:])
 period=max(1,proposals//3)
 position=rng.randrange(k-2)
 walker.move(position)
 direction=1
 size=n-d+1
 for step in range(proposals):
  if step and step%period==0:
   rng.shuffle(order)
   walker=TripleWalker(n,d,initial,target,actions,best,order)
   position=rng.randrange(k-2)
   walker.move(position)
  first,last=(walker.sequence[position],walker.sequence[position+2])
  side=step%2
  old=last if side else first
  mode=rng.randrange(5)
  if mode==0 and old>=0:
   x,y,r=actions[old][1]
   x=min(size-1,max(0,x+rng.choice((-2,-1,0,0,1,2))))
   y=min(size-1,max(0,y+rng.choice((-2,-1,0,0,1,2))))
   fixed=(x*size+y)*4+rng.randrange(4)
  elif mode==1:
   fixed=walker.informed(side)
  elif mode==4:
   fixed=-1
  else:
   fixed=rng.randrange(len(actions))
  if side:
   last=fixed
  else:
   first=fixed
  triple,delta=walker.propose(first,last)
  temperature=0.4*(1-step%period/period)**2+0.04
  if delta>=0 or rng.random()<math.exp(delta/temperature):
   walker.accept(triple,delta)
   if walker.score>=best_score:
    best_score,best=(walker.score,walker.sequence[:])
    if best_score==limit:
     break
  if k>3:
   if rng.randrange(16)==0:
    direction=-direction
   if not 0<=position+direction<k-2:
    direction=-direction
   position+=direction
   walker.move(position)
 return[aid for aid in best if aid>=0]
def solve_without_wildcard(n,d,c,k,grid,target,stamp):
 operations=solve_before_triple_walking(n,d,c,k,grid[:],target,stamp[:])
 if k<=2:
  return operations
 indices,_,ops,_,_=build(n,d,target)
 actions=list(zip(indices,ops))
 size=n-d+1
 sequence=[(x*size+y)*4+r for x,y,r in operations]
 sequence=anneal_triples(n,d,k,grid+stamp,target,actions,sequence)
 sequence=refine(n,d,k,grid+stamp,target,actions,sequence,passes=2)
 return[actions[aid][1]for aid in sequence]
def packed_transitions():
 rotations=[]
 for r in range(4):
  rows=[]
  for u in range(3):
   table=[]
   for value in range(512):
    result=0
    for v in range(3):
     x,y=((u,v),(v,2-u),(2-u,2-v),(2-v,u))[r]
     result|=(value>>3*v&7)<<3*(x*3+y)
    table.append(result)
   rows.append(table)
  rotations.append(rows)
 board_mask=(1<<48)-1
 patches=[]
 for x in range(2):
  for y in range(2):
   shift=3*(4*x+y)
   mask=board_mask^(511|511<<12|511<<24)<<shift
   patches.append((shift,mask))
 def rotate(value,r):
  tables=rotations[r]
  return tables[0][value&511]|tables[1][value>>9&511]|tables[2][value>>18]
 def expand(state):
  board,stamp=(state&board_mask,state>>48)
  rotated=[rotate(stamp,r)for r in range(4)]
  scatter=[v&511|(v&261632)<<3|(v&133955584)<<6 for v in rotated]
  for p,(shift,mask)in enumerate(patches):
   shifted=board>>shift
   patch=shifted&511|shifted>>3&261632|shifted>>6&133955584
   retained=board&mask
   for r in range(4):
    child=retained|scatter[r]<<shift|rotate(patch,-r&3)<<48
    yield(p*4+r,child)
 return expand
_PACKED_EXPAND=None
_WILDCARD_BACKWARD=None
def wildcard_backward_records(expand,wanted):
 goal=wanted|(1<<27)-1<<48
 backward={goal:b''}
 frontier=[goal]
 for depth in range(1,5):
  next_layer=[]
  for state in frontier:
   path=backward[state]
   for aid,child in expand(state):
    if child in backward:
     continue
    new_path=path+bytes((aid,))
    backward[child]=new_path
    next_layer.append(child)
    wishes=child
    constraints=bytearray()
    for position in range(25):
     color=wishes&7
     wishes>>=3
     if color!=7:
      constraints.append(position*6+color)
    yield(depth,new_path,bytes(constraints))
  frontier=next_layer
def wildcard_finish(grid,target,stamp,k,depth=8):
 global _PACKED_EXPAND,_WILDCARD_BACKWARD
 if grid==target:
  return[]
 if color_bound(grid+stamp,target)<16:
  return None
 if _PACKED_EXPAND is None:
  _PACKED_EXPAND=packed_transitions()
 expand=_PACKED_EXPAND
 initial=sum((v<<3*i for i,v in enumerate(grid+stamp)))
 wanted=sum((v<<3*i for i,v in enumerate(target)))
 board_mask=(1<<48)-1
 forward={initial:b''}
 frontier=[initial]
 forward_depth=min(4,k,depth)
 for _ in range(forward_depth):
  next_layer=[]
  for state in frontier:
   path=forward[state]
   for aid,child in expand(state):
    if child in forward:
     continue
    new_path=path+bytes((aid,))
    forward[child]=new_path
    if child&board_mask==wanted:
     return list(new_path)
    next_layer.append(child)
  frontier=next_layer
 backward_depth=min(4,k-forward_depth,depth-forward_depth)
 if backward_depth<=0:
  return None
 states=list(forward)
 byte_count=(len(states)+7)//8
 buffers=[[bytearray(byte_count)for _ in range(6)]for _ in range(25)]
 for index,state in enumerate(states):
  offset,bit=(index>>3,1<<(index&7))
  for row in buffers:
   row[state&7][offset]|=bit
   state>>=3
 indexes=[int.from_bytes(buf,'little')for row in buffers for buf in row]
 counts=[bits.bit_count()for bits in indexes]
 counts_get=counts.__getitem__
 all_bits=(1<<len(states))-1
 if _WILDCARD_BACKWARD is None or _WILDCARD_BACKWARD[0]!=wanted:
  _WILDCARD_BACKWARD=[wanted,[],wildcard_backward_records(expand,wanted)]
 cache=_WILDCARD_BACKWARD
 records=cache[1]
 cursor=0
 while True:
  if cursor==len(records):
   if cache[2]is None:
    break
   record=next(cache[2],None)
   if record is None:
    cache[2]=None
    break
   records.append(record)
  level,new_path,encoded=records[cursor]
  if level>backward_depth:
   break
  cursor+=1
  hits=all_bits
  for identifier in sorted(encoded,key=counts_get):
   hits&=indexes[identifier]
   if not hits:
    break
  if hits:
   match=states[(hits&-hits).bit_length()-1]
   return list(forward[match]+new_path[::-1])
 return None
def solve_without_suffix_finish(n,d,c,k,grid,target,stamp):
 reference=solve_without_wildcard(n,d,c,k,grid,target,stamp)
 if n!=4 or d!=3 or len(reference)>=k:
  return reference
 indices,_,ops,_,_=build(n,d,target)
 board,buffer=(grid[:],stamp[:])
 for x,y,r in reference:
  transition(board,buffer,indices[(x*2+y)*4+r])
 tail=wildcard_finish(board,target,buffer,k-len(reference))
 return reference+[ops[aid]for aid in tail]if tail is not None else reference
def solve_forward_parent(n,d,c,k,grid,target,stamp):
 reference=solve_without_suffix_finish(n,d,c,k,grid,target,stamp)
 if n!=4 or d!=3 or k<6 or(color_bound(grid+stamp,target)<16):
  return reference
 indices,_,ops,_,_=build(n,d,target)
 board,buffer=(grid[:],stamp[:])
 for x,y,r in reference:
  transition(board,buffer,indices[(x*2+y)*4+r])
 if board==target:
  return reference
 tried=set()
 for remove in(2,4,8,12):
  length=max(0,len(reference)-remove)
  if length in tried:
   continue
  tried.add(length)
  board,buffer=(grid[:],stamp[:])
  for x,y,r in reference[:length]:
   transition(board,buffer,indices[(x*2+y)*4+r])
  tail=wildcard_finish(board,target,buffer,k-length)
  if tail is not None:
   return reference[:length]+[ops[aid]for aid in tail]
 return reference
def forward_sweep(n,d,initial,target,actions,sequence,order):
 nn=n*n
 wishes=target+[6]*(d*d)
 for old in reversed(sequence):
  if old>=0:
   seq_transition(wishes,nn,actions[old][0])
 state=RefineState(n,d,initial,wishes[:nn],actions,order)
 state.wstamp=wishes[nn:]
 result=sequence[:]
 for i,old in enumerate(sequence):
  if old>=0:
   state.apply(old,wishes=True)
  chosen,_=state.best()
  result[i]=chosen
  if chosen>=0:
   state.apply(chosen)
 return result
def forward_refine(n,d,k,initial,target,actions,sequence,passes=1,seed_offset=0):
 nn=n*n
 limit=color_bound(initial,target)
 seed=sum(((i+1)*v for i,v in enumerate(initial)))+k*131+1000003+seed_offset
 rng=random.Random(seed)
 sequence=[aid for aid in sequence if aid>=0]
 for iteration in range(passes):
  final=initial[:]
  for aid in sequence:
   seq_transition(final,nn,actions[aid][0])
  if sum((a==b for a,b in zip(final,target)))==limit:
   return sequence
  padded=sequence+[-1]*min(8,k-len(sequence))
  order=list(range(len(actions)))
  rng.shuffle(order)
  sequence=forward_sweep(n,d,initial,target,actions,padded,order)
  sequence=[aid for aid in sequence if aid>=0]
 return sequence
def solve_without_late_beam(n,d,c,k,grid,target,stamp):
 reference=solve_forward_parent(n,d,c,k,grid[:],target,stamp[:])
 if k<=2:
  return reference
 nn=n*n
 initial=grid+stamp
 indices,_,ops,_,_=build(n,d,target)
 actions=list(zip(indices,ops))
 side=n-d+1
 candidate=[(x*side+y)*4+r for x,y,r in reference]
 final=initial[:]
 for aid in candidate:
  seq_transition(final,nn,indices[aid])
 best_score=sum((a==b for a,b in zip(final,target)))
 limit=color_bound(initial,target)
 if best_score==limit:
  return reference
 best_sequence=candidate
 for iteration in range(2):
  candidate=forward_refine(n,d,k,initial,target,actions,candidate,seed_offset=iteration*104729)
  candidate=refine(n,d,k,initial,target,actions,candidate,passes=1,seed_offset=3301+iteration*7919)
  final=initial[:]
  for aid in candidate:
   seq_transition(final,nn,indices[aid])
  score=sum((a==b for a,b in zip(final,target)))
  if score>best_score:
   best_score,best_sequence=(score,candidate)
   if score==limit:
    break
 return[ops[aid]for aid in best_sequence]
def packed3_transitions(n):
 rotations=[]
 for r in range(4):
  tables=[]
  for u in range(3):
   row=[]
   for value in range(512):
    output=0
    for v in range(3):
     x,y=((u,v),(v,2-u),(2-u,2-v),(2-v,u))[r]
     output|=(value>>3*v&7)<<3*(3*x+y)
    row.append(output)
   tables.append(row)
  rotations.append(tables)
 shift_stamp=3*n*n
 board_mask=(1<<shift_stamp)-1
 stride=3*n
 patches=[]
 for x in range(n-2):
  for y in range(n-2):
   shift=3*(n*x+y)
   mask=board_mask^(511|511<<stride|511<<2*stride)<<shift
   patches.append((shift,mask))
 def rotate(value,r):
  tables=rotations[r]
  return tables[0][value&511]|tables[1][value>>9&511]|tables[2][value>>18]
 def expand(state):
  board,stamp=(state&board_mask,state>>shift_stamp)
  rotated=[rotate(stamp,r)for r in range(4)]
  scatter=[v&511|(v>>9&511)<<stride|v>>18<<2*stride for v in rotated]
  for p,(shift,mask)in enumerate(patches):
   shifted=board>>shift
   patch=shifted&511|(shifted>>stride&511)<<9|(shifted>>2*stride&511)<<18
   retained=board&mask
   for r in range(4):
    yield(4*p+r,retained|scatter[r]<<shift|rotate(patch,-r&3)<<shift_stamp)
 return expand
def late_beam_finish(n,grid,target,stamp,k):
 if k<=0:
  return None
 nn=n*n
 initial_score=sum((a==b for a,b in zip(grid,target)))
 if initial_score==color_bound(grid+stamp,target):
  return None
 expand=packed3_transitions(n)
 initial=sum((v<<3*i for i,v in enumerate(grid+stamp)))
 wanted=sum((v<<3*i for i,v in enumerate(target)))
 comparison_mask=sum((1<<3*i for i in range(nn)))
 rng=random.Random(initial+k*997)
 import heapq
 frontier=[(initial,b'')]
 visited={initial}
 for depth in range(min(6,k)):
  candidates={}
  for state,path in frontier:
   for aid,child in expand(state):
    if child in visited or child in candidates:
     continue
    new_path=path+bytes((aid,))
    diff=child^wanted
    score=nn-((diff|diff>>1|diff>>2)&comparison_mask).bit_count()
    if score>initial_score:
     return list(new_path)
    candidates[child]=(score,rng.getrandbits(32),new_path)
  if not candidates:
   break
  selected=heapq.nlargest(256,candidates,key=candidates.get)
  frontier=[(state,candidates[state][2])for state in selected]
  visited.update(selected)
 return None
def solve_without_hot_restart(n,d,c,k,grid,target,stamp):
 reference=solve_without_late_beam(n,d,c,k,grid,target,stamp)
 if not 5<=n<=9 or d!=3 or len(reference)>=k:
  return reference
 indices,_,ops,_,_=build(n,d,target)
 board,buffer=(grid[:],stamp[:])
 width=n-d+1
 for x,y,r in reference:
  transition(board,buffer,indices[(x*width+y)*4+r])
 missing=sum((a!=b for a,b in zip(board,target)))
 if not 1<=missing<=8:
  return reference
 candidate=reference[:]
 for _ in range(4):
  tail=late_beam_finish(n,board,target,buffer,k-len(candidate))
  if tail is None:
   break
  for aid in tail:
   transition(board,buffer,indices[aid])
   candidate.append(ops[aid])
 return candidate
def anneal_hot_triples(n,d,k,initial,target,actions,sequence,proposals=None):
 import math
 if k<3:
  return sequence
 limit=color_bound(initial,target)
 final=initial[:]
 for aid in sequence:
  if aid>=0:
   seq_transition(final,n*n,actions[aid][0])
 if sum((a==b for a,b in zip(final,target)))==limit:
  return[aid for aid in sequence if aid>=0]
 rng=random.Random(sum(((i+67)*v for i,v in enumerate(initial)))+k*1559+925713)
 order=list(range(len(actions)))
 rng.shuffle(order)
 sequence=sequence+[-1]*(k-len(sequence))
 walker=TripleWalker(n,d,initial,target,actions,sequence,order)
 if proposals is None:
  proposals=min(3000,max(300,675000//(n*n)))
 best_score,best=(walker.score,walker.sequence[:])
 period=max(1,proposals//3)
 position=rng.randrange(k-2)
 walker.move(position)
 direction=1
 size=n-d+1
 for step in range(proposals):
  if step and step%period==0:
   rng.shuffle(order)
   walker=TripleWalker(n,d,initial,target,actions,best,order)
   position=rng.randrange(k-2)
   walker.move(position)
  first,last=(walker.sequence[position],walker.sequence[position+2])
  side=step%2
  old=last if side else first
  mode=rng.randrange(5)
  if mode==0 and old>=0:
   x,y,r=actions[old][1]
   x=min(size-1,max(0,x+rng.choice((-2,-1,0,0,1,2))))
   y=min(size-1,max(0,y+rng.choice((-2,-1,0,0,1,2))))
   fixed=(x*size+y)*4+rng.randrange(4)
  elif mode==1:
   fixed=walker.informed(side)
  elif mode==4:
   fixed=-1
  else:
   fixed=rng.randrange(len(actions))
  if side:
   last=fixed
  else:
   first=fixed
  triple,delta=walker.propose(first,last)
  temperature=0.86*(1-step%period/period)**2+0.04
  if delta>=0 or rng.random()<math.exp(delta/temperature):
   walker.accept(triple,delta)
   if walker.score>=best_score:
    best_score,best=(walker.score,walker.sequence[:])
    if best_score==limit:
     break
  if k>3:
   if rng.randrange(16)==0:
    direction=-direction
   if not 0<=position+direction<k-2:
    direction=-direction
   position+=direction
   walker.move(position)
 return[aid for aid in best if aid>=0]
def hot_triple_repair(n,d,k,initial,target,actions,sequence,proposals=None):
 if k<3:
  return sequence
 final=initial[:]
 for aid in sequence:
  if aid>=0:
   seq_transition(final,n*n,actions[aid][0])
 parent_score=sum((a==b for a,b in zip(final,target)))
 if parent_score==color_bound(initial,target):
  return sequence
 candidate=anneal_hot_triples(n,d,k,initial,target,actions,sequence,proposals)
 candidate=refine(n,d,k,initial,target,actions,candidate,passes=2)
 final=initial[:]
 for aid in candidate:
  if aid>=0:
   seq_transition(final,n*n,actions[aid][0])
 if sum((a==b for a,b in zip(final,target)))>parent_score:
  return candidate
 return sequence
def solve_without_commutator(n,d,c,k,grid,target,stamp):
 reference=solve_without_hot_restart(n,d,c,k,grid[:],target,stamp[:])
 if k<3:
  return reference
 indices,_,ops,_,_=build(n,d,target)
 actions=list(zip(indices,ops))
 width=n-d+1
 sequence=[(x*width+y)*4+r for x,y,r in reference]
 found=hot_triple_repair(n,d,k,grid+stamp,target,actions,sequence)
 if found==sequence:
  return reference
 return[ops[aid]for aid in found if aid>=0]
def commutator_word_gain(grid,target,stamp,indices,word,touched):
 before=sum((grid[p]==target[p]for p in touched))
 for aid in word:
  transition(grid,stamp,indices[aid])
 after=sum((grid[p]==target[p]for p in touched))
 for aid in reversed(word):
  transition(grid,stamp,indices[aid])
 return after-before
def commutator_tail(n,d,grid,target,stamp,indices,seed,pair_limit=20000):
 if pair_limit<=0:
  return None
 width=n-d+1
 missing=[p for p in range(n*n)if grid[p]!=target[p]]
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
  seconds=[(x*width+y)*4+r for x in range(max(0,row-d+1),min(width,row+d))for y in range(max(0,col-d+1),min(width,col+d))for r in range(4)]
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
   for left,right in((first,second),(second,first)):
    word=(left,right,left,right)
    gain=commutator_word_gain(grid,target,stamp,indices,word,touched)
    if gain>best_gain:
     best_gain,best_word=(gain,word)
     if best_gain==possible:
      return best_word
 return best_word
def solve_four_parent(n,d,c,k,grid,target,stamp):
 reference=solve_without_commutator(n,d,c,k,grid,target,stamp)
 if n>16 or k-len(reference)<4:
  return reference
 indices,_,operations,_,_=build(n,d,target)
 width=n-d+1
 board,buffer=(grid[:],stamp[:])
 for x,y,r in reference:
  transition(board,buffer,indices[(x*width+y)*4+r])
 matches=sum((a==b for a,b in zip(board,target)))
 if not 1<=n*n-matches<=12 or matches>=color_bound(grid+stamp,target):
  return reference
 seed=sum(((i+41)*v for i,v in enumerate(grid+target+stamp)))+n*1009+d*9176+k*131
 word=commutator_tail(n,d,board,target,buffer,indices,seed)
 if word is None:
  return reference
 return reference+[operations[aid]for aid in word]
class FourWindowWalker:
 def __init__(self,n,d,initial,target,actions,sequence,order):
  self.sequence=sequence[:]
  self.actions=actions
  self.position=0
  nn=n*n
  final=initial[:]
  for aid in sequence:
   if aid>=0:
    seq_transition(final,nn,actions[aid][0])
  self.score=sum((a==b for a,b in zip(final,target)))
  wishes=target+[6]*(d*d)
  for aid in reversed(sequence[4:]):
   if aid>=0:
    seq_transition(wishes,nn,actions[aid][0])
  self.state=RefineState(n,d,initial,wishes[:nn],actions,order)
  self.state.wstamp=wishes[nn:]
  self.boundary_score=sum((a==b for a,b in zip(initial,wishes)))
 def move(self,position):
  if position>self.position:
   steps=range(self.position,position)
  else:
   steps=range(self.position-1,position-1,-1)
  for i in steps:
   a,b=(self.sequence[i],self.sequence[i+4])
   if a>=0:
    self.boundary_score+=operation_gain(self.state,a)
    self.state.apply(a)
   if b>=0:
    self.boundary_score+=operation_gain(self.state,b)
    self.state.apply(b,wishes=True)
  self.position=position
 def propose(self,first,last,candidates):
  state=self.state
  old=self.score-self.boundary_score
  gain=operation_gain(state,first)
  outer=refine_trial(state,first)
  gain+=operation_gain(state,last)
  inner=refine_trial(state,last,wishes=True)
  second,third=optimize_pair(state,self.sequence[self.position+1],self.sequence[self.position+2],candidates)
  gain+=operation_gain(state,second)
  middle=refine_trial(state,second)
  gain+=operation_gain(state,third)
  refine_restore(state,middle)
  refine_restore(state,inner)
  refine_restore(state,outer)
  return((first,second,third,last),gain-old)
 def accept(self,window,delta):
  self.sequence[self.position:self.position+4]=window
  self.score+=delta
def repair_four_windows(n,d,k,initial,target,actions,sequence,proposals=None):
 import math
 if k<4:
  return sequence
 padded=sequence+[-1]*min(8,k-len(sequence))
 rng=random.Random(sum(((i+43)*v for i,v in enumerate(initial)))+k*1733+74821)
 order=list(range(len(actions)))
 rng.shuffle(order)
 walker=FourWindowWalker(n,d,initial,target,actions,padded,order)
 limit=color_bound(initial,target)
 if walker.score==limit:
  return sequence
 if proposals is None:
  proposals=min(1800,max(120,180000//(n*n)))
 best_score,best=(walker.score,walker.sequence[:])
 size=n-d+1
 length=len(padded)
 position=rng.randrange(length-3)
 walker.move(position)
 direction=1
 for step in range(proposals):
  first,last=(walker.sequence[position],walker.sequence[position+3])
  side=step%2
  old=last if side else first
  mode=rng.randrange(5)
  if mode==0 and old>=0:
   x,y,r=actions[old][1]
   x=min(size-1,max(0,x+rng.choice((-1,0,1))))
   y=min(size-1,max(0,y+rng.choice((-1,0,1))))
   fixed=(x*size+y)*4+rng.randrange(4)
  elif mode==1:
   state=walker.state
   p=rng.randrange(n*n)
   for _ in range(10):
    p=rng.randrange(n*n)
    if state.wishes[p]<6 and state.grid[p]!=state.wishes[p]:
     break
   x=min(size-1,max(0,p//n-rng.randrange(d)))
   y=min(size-1,max(0,p%n-rng.randrange(d)))
   fixed=(x*size+y)*4+rng.randrange(4)
  elif mode==4:
   fixed=-1
  else:
   fixed=rng.randrange(len(actions))
  if side:
   last=fixed
  else:
   first=fixed
  if step%11==10:
   if side:
    first=rng.randrange(len(actions))
   else:
    last=rng.randrange(len(actions))
  candidates=[(walker.sequence[position+1],0),(walker.sequence[position+2],1),(-1,0),(-1,1),(rng.randrange(len(actions)),rng.randrange(2))]
  window,delta=walker.propose(first,last,candidates)
  temperature=0.04+0.76*(1-step/max(1,proposals-1))**2
  if delta>=0 or rng.random()<math.exp(delta/temperature):
   walker.accept(window,delta)
   if walker.score>=best_score:
    best_score,best=(walker.score,walker.sequence[:])
    if best_score==limit:
     break
  if length>4:
   if rng.randrange(16)==0:
    direction=-direction
   if not 0<=position+direction<length-3:
    direction=-direction
   position+=direction
   walker.move(position)
 return[aid for aid in best if aid>=0]
def solve_without_deeper_beam(n,d,c,k,grid,target,stamp):
 reference=solve_four_parent(n,d,c,k,grid[:],target,stamp[:])
 if k<4:
  return reference
 nn=n*n
 initial=grid+stamp
 indices,_,ops,_,_=build(n,d,target)
 actions=list(zip(indices,ops))
 width=n-d+1
 sequence=[(x*width+y)*4+r for x,y,r in reference]
 final=initial[:]
 for aid in sequence:
  seq_transition(final,nn,indices[aid])
 baseline=sum((a==b for a,b in zip(final,target)))
 if baseline==color_bound(initial,target):
  return reference
 candidate=repair_four_windows(n,d,k,initial,target,actions,sequence)
 if candidate==sequence:
  return reference
 candidate=refine(n,d,k,initial,target,actions,candidate,passes=1,seed_offset=2947)
 final=initial[:]
 for aid in candidate:
  seq_transition(final,nn,indices[aid])
 if sum((a==b for a,b in zip(final,target)))<=baseline:
  return reference
 return[ops[aid]for aid in candidate]
def deeper_beam_finish(n,grid,target,stamp,k):
 if k<=0:
  return None
 nn=n*n
 initial_score=sum((a==b for a,b in zip(grid,target)))
 if initial_score==color_bound(grid+stamp,target):
  return None
 expand=packed3_transitions(n)
 initial=sum((v<<3*i for i,v in enumerate(grid+stamp)))
 wanted=sum((v<<3*i for i,v in enumerate(target)))
 comparison_mask=sum((1<<3*i for i in range(nn)))
 rng=random.Random(initial+k*997)
 import heapq
 frontier=[(initial,b'')]
 visited={initial}
 for depth in range(min(8,k)):
  candidates={}
  for state,path in frontier:
   for aid,child in expand(state):
    if child in visited or child in candidates:
     continue
    new_path=path+bytes((aid,))
    diff=child^wanted
    score=nn-((diff|diff>>1|diff>>2)&comparison_mask).bit_count()
    if score>initial_score:
     return list(new_path)
    candidates[child]=(score,rng.getrandbits(32),new_path)
  if not candidates:
   break
  selected=heapq.nlargest(512,candidates,key=candidates.get)
  frontier=[(state,candidates[state][2])for state in selected]
  visited.update(selected)
 return None
def solve_route_parent(n,d,c,k,grid,target,stamp):
 reference=solve_without_deeper_beam(n,d,c,k,grid,target,stamp)
 if not 5<=n<=9 or d!=3 or k-len(reference)<3:
  return reference
 indices,_,ops,_,_=build(n,d,target)
 board,buffer=(grid[:],stamp[:])
 width=n-d+1
 for x,y,r in reference:
  transition(board,buffer,indices[(x*width+y)*4+r])
 missing=sum((a!=b for a,b in zip(board,target)))
 if not 1<=missing<=8:
  return reference
 tail=deeper_beam_finish(n,board,target,buffer,k-len(reference))
 if tail is None:
  return reference
 for aid in tail:
  transition(board,buffer,indices[aid])
 if sum((a==b for a,b in zip(board,target)))<=n*n-missing:
  return reference
 return reference+[ops[aid]for aid in tail]
def route_patterns(n,d,repeats=(3,)):
 patterns=[]
 offsets=[[(u,v),(v,d-1-u),(d-1-u,d-1-v),(d-1-v,u)]for u in range(d)for v in range(d)]
 for dx in range(d):
  for dy in range(1 if dx==0 else 1-d,d):
   for r in range(4):
    left=[xy[r]for xy in offsets]
    for s in range(4):
     right=[(dx+xy[s][0],dy+xy[s][1])for xy in offsets]
     cells=set(left+right)
     initial={p:p for p in cells}
     initial.update({j:j for j in range(d*d)})
     for backward in range(2):
      a,b=(right,left)if backward else(left,right)
      state=initial.copy()
      for count in range(1,max(repeats)+1):
       for patch in(a,b):
        for j,p in enumerate(patch):
         state[j],state[p]=(state[p],state[j])
       if count not in repeats:
        continue
       mapping=[]
       for p in sorted(cells):
        q=state[p]
        if q==p:
         continue
        src=n*n+q if isinstance(q,int)else q[0]*n+q[1]
        mapping.append((p[0]*n+p[1],src,isinstance(q,int)))
       if mapping:
        patterns.append((dx,dy,r,s,backward,count,mapping))
 return patterns
'Exact parallel scoring of sparse routing permutations at every legal anchor.'
def route_tail(n,d,grid,target,stamp,k,repeats=(3,),rounds=3):
 active=tuple((x for x in repeats if 2*x<=k))
 if not active:
  return[]
 patterns=route_patterns(n,d,active)
 width=n-d+1
 state=grid+stamp
 wanted=[0]*6
 for p,color in enumerate(target):
  wanted[color]|=1<<p
 def shift(bits,offset):
  return bits>>offset if offset>=0 else bits<<-offset
 offsets={p for*_,mapping in patterns for p,_,_ in mapping}
 sources={q for*_,mapping in patterns for _,q,buffer in mapping if not buffer}
 wishes={p:tuple((shift(bits,p)for bits in wanted))for p in offsets}
 legal={}
 for dx,dy,*_ in patterns:
  key=(dx,dy)
  if key in legal:
   continue
  left,right=(max(0,-dy),min(width,width-dy))
  if left>=right or dx>=width:
   legal[key]=0
  else:
   row=(1<<right-left)-1<<left
   legal[key]=sum((row<<x*n for x in range(width-dx)))
 rotations=[[p*n+q for u in range(d)for v in range(d)for p,q in[((u,v),(v,d-1-u),(d-1-u,d-1-v),(d-1-v,u))[r]]]for r in range(4)]
 answer=[]
 for _ in range(rounds):
  have=[0]*6
  agreement=0
  for p,color in enumerate(state[:n*n]):
   have[color]|=1<<p
   if color==target[p]:
    agreement|=1<<p
  if agreement==(1<<n*n)-1:
   break
  values={q:tuple((shift(bits,q)for bits in have))for q in sources}
  old={p:shift(agreement,p)for p in offsets}
  matches={}
  best_gain=0
  best=None
  for dx,dy,r,s,backward,count,mapping in patterns:
   if len(answer)+2*count>k:
    continue
   anchors=legal[dx,dy]
   if not anchors:
    continue
   planes=[0]*(2*len(mapping)+1).bit_length()
   for p,q,buffer in mapping:
    if buffer:
     new=wishes[p][state[q]]
    else:
     key=(p,q)
     new=matches.get(key)
     if new is None:
      new=0
      for want,value in zip(wishes[p],values[q]):
       new|=want&value
      matches[key]=new
    for carry in(new&anchors,anchors&~old[p]):
     level=0
     while carry:
      before=planes[level]
      planes[level]=before^carry
      carry&=before
      level+=1
   candidates,value=(anchors,0)
   for level in range(len(planes)-1,-1,-1):
    hits=candidates&planes[level]
    if hits:
     candidates=hits
     value|=1<<level
   gain=value-len(mapping)
   if gain>best_gain:
    best_gain=gain
    base=(candidates&-candidates).bit_length()-1
    x,y=divmod(base,n)
    left,right=((x,y,r),(x+dx,y+dy,s))
    best=([right,left]if backward else[left,right])*count
  if best is None:
   break
  answer.extend(best)
  for x,y,r in best:
   base=x*n+y
   for j,offset in enumerate(rotations[r]):
    p=base+offset
    state[n*n+j],state[p]=(state[p],state[n*n+j])
 return answer
def cancel_inverse_pairs(sequence):
 compact=[]
 for aid in sequence:
  if compact and compact[-1]==aid:
   compact.pop()
  else:
   compact.append(aid)
 return compact
def best_insertion(n,d,initial,target,actions,sequence,seed=0):
 final=initial[:]
 for aid in sequence:
  seq_transition(final,n*n,actions[aid][0])
 order=list(range(len(actions)))
 random.Random(seed).shuffle(order)
 state=RefineState(n,d,final,target,actions,order)
 best=(0,-1,-1)
 for pos in range(len(sequence),-1,-1):
  aid,gain=state.best()
  if gain>best[0]:
   best=(gain,pos,aid)
  if pos:
   old=sequence[pos-1]
   state.apply(old)
   state.apply(old,wishes=True)
 return best
def deletion_deltas(n,d,initial,target,actions,sequence):
 final=initial[:]
 for aid in sequence:
  seq_transition(final,n*n,actions[aid][0])
 state=RefineState(n,d,final,target,actions,list(range(len(actions))))
 deltas=[0]*len(sequence)
 for pos in range(len(sequence)-1,-1,-1):
  old=sequence[pos]
  state.apply(old)
  deltas[pos]=-operation_gain(state,old)
  state.apply(old,wishes=True)
 return deltas
def temporal_repair(n,d,k,initial,target,actions,sequence,rounds=1,removals=0):
 nn=n*n
 sequence=sequence[:]
 final=initial[:]
 for aid in sequence:
  seq_transition(final,nn,actions[aid][0])
 score=sum((a==b for a,b in zip(final,target)))
 upper=color_bound(initial,target)
 for iteration in range(rounds):
  if score==upper:
   break
  seed=sum(((p+11)*v for p,v in enumerate(initial)))+iteration*10891
  best_gain,best_sequence=(0,sequence)
  if len(sequence)<k:
   gain,pos,aid=best_insertion(n,d,initial,target,actions,sequence,seed)
   if gain:
    best_gain,best_sequence=(gain,sequence[:pos]+[aid]+sequence[pos:])
  if removals and sequence:
   deltas=deletion_deltas(n,d,initial,target,actions,sequence)
   order=sorted(range(len(sequence)),key=lambda p:(deltas[p],-p),reverse=True)
   for remove in order[:removals]:
    child=sequence[:remove]+sequence[remove+1:]
    gain,pos,aid=best_insertion(n,d,initial,target,actions,child,seed+remove)
    gain+=deltas[remove]
    if gain>best_gain:
     best_gain,best_sequence=(gain,child[:pos]+[aid]+child[pos:]if aid>=0 else child)
  if best_gain<=0:
   break
  sequence=best_sequence
  score+=best_gain
 return sequence
def solve(n,d,c,k,grid,target,stamp):
 reference=solve_route_parent(n,d,c,k,grid[:],target,stamp[:])
 if k<=2:
  return reference
 indices,_,ops,_,_=build(n,d,target)
 side=n-d+1
 sequence=cancel_inverse_pairs([(x*side+y)*4+r for x,y,r in reference])
 initial=grid+stamp
 sequence=temporal_repair(n,d,k,initial,target,list(zip(indices,ops)),sequence,5,5)
 final=initial[:]
 for aid in sequence:
  seq_transition(final,n*n,indices[aid])
 candidate=[ops[aid]for aid in sequence]
 if sum((a==b for a,b in zip(final,target)))>=color_bound(initial,target):
  return candidate
 rounds=min(12,max(3,3000//(n*n)))
 return candidate+route_tail(n,d,final[:n*n],target,final[n*n:],k-len(candidate),(3,),rounds)
def main():
 data=list(map(int,sys.stdin.buffer.read().split()))
 n,d,c,k=data[:4]
 nn=n*n
 operations=solve(n,d,c,k,data[4:4+nn],data[4+nn:4+2*nn],data[4+2*nn:])
 print(len(operations))
 for operation in operations:
  print(*operation)
if __name__=='__main__':
 main()
