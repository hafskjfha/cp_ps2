import random
import heapq
import sys
RUNS=12
NEUTRAL=True
def color_bound(mq1,mq2):
 available,needed=([0]*6,[0]*6)
 for value in mq1:
  available[value]+=1
 for value in mq2:
  needed[value]+=1
 return sum((min(a,b)for a,b in zip(available,needed)))
def build(n,d,mq2):
 mq12=[]
 for r in range(4):
  mq12.append([p*n+q for u in range(d)for v in range(d)for p,q in[((u,v),(v,d-1-u),(d-1-u,d-1-v),(d-1-v,u))[r]]])
 mq10,codes,mq8=([],[],[])
 coverage=[[]for _ in range(n*n)]
 patches=[]
 for x in range(n-d+1):
  for y in range(n-d+1):
   patch=len(patches)
   mq16=[x*n+y+v for v in mq12[0]]
   patches.append(mq16)
   for pos in mq16:
    coverage[pos].append(patch)
   for r in range(4):
    action=tuple((x*n+y+v for v in mq12[r]))
    mq10.append(action)
    codes.append(sum((1<<6*j+mq2[pos]for j,pos in enumerate(action))))
    mq8.append((x,y,r))
 return(mq10,codes,mq8,coverage,patches)
def transition(mq18,mq17,mq10):
 for j,pos in enumerate(mq10):
  mq17[j],mq18[pos]=(mq18[pos],mq17[j])
def solve_plateau(n,d,c,k,mq1,mq2,start_stamp):
 _is=sum((a==b for a,b in zip(mq1,mq2)))
 limit=color_bound(mq1+start_stamp,mq2)
 if _is==limit:
  return[]
 mq6,answer=(_is,[])
 seed=917351
 for value in mq1+mq2+start_stamp:
  seed=(seed^value)*1000003&4294967295
 rng=random.Random(seed)
 order=list(range(4*(n-d+1)**2))
 for run in range(RUNS):
  if run:
   rng.shuffle(order)
  my=State(n,d,c,mq1[:],mq2,start_stamp[:],order[:])
  score,path=(_is,[])
  seen=set()
  for step in range(k):
   seen.add(tuple(my.mq17))
   gain,mq5=my.best_candidates()
   if gain<0 or(gain==0 and(not NEUTRAL or run==0)):
    break
   chosen=-1
   while mq5:
    bit=mq5&-mq5
    action=my.order[bit.bit_length()-1]
    if gain>0 or tuple((my.mq18[p]for p in my.mq19[action][0]))not in seen:
     chosen=action
     break
    mq5^=bit
   if chosen<0:
    break
   if gain>0:
    seen.clear()
   my.apply(chosen)
   score+=gain
   path.append(my.mq19[chosen][1])
   if score>mq6:
    mq6,answer=(score,path[:])
   if mq6==limit:
    return answer
 return answer
class State:
 _geometry_cache=None
 def __init__(mz,n,d,c,mq18,mq2,mq17,order=None):
  mz.n,mz.d,mz.c=(n,d,c)
  mz.mq18,mz.mq2,mz.mq17=(mq18,mq2,mq17)
  mz.matches=sum((a==b for a,b in zip(mq18,mq2)))
  mz.limit=color_bound(mq18+mq17,mq2)
  key=(n,d,c,tuple(mq2))
  cached=State._geometry_cache
  if cached is not None and cached[0]==key:
   mz.regions,mz.mq19,mz.masks,mz.cover=cached[1:]
  else:
   mz.regions=[]
   mz.mq19=[]
   mz.masks=[]
   mz.cover=[[]for _ in mq18]
   mq12=[]
   for r in range(4):
    offsets=[]
    for u in range(d):
     for v in range(d):
      p,q=((u,v),(v,d-1-u),(d-1-u,d-1-v),(d-1-v,u))[r]
      offsets.append(p*n+q)
    mq12.append(offsets)
   for x in range(n-d+1):
    for y in range(n-d+1):
     base=x*n+y
     mq10=tuple((base+o for o in mq12[0]))
     region=len(mz.regions)
     mz.regions.append(mq10)
     for p in mq10:
      mz.cover[p].append(region)
     for r in range(4):
      mq10=tuple((base+o for o in mq12[r]))
      mz.mq19.append((mq10,(x,y,r)))
      mz.masks.append(sum((1<<c*j+mq2[p]for j,p in enumerate(mq10))))
   State._geometry_cache=(key,mz.regions,mz.mq19,mz.masks,mz.cover)
  mz.order=list(range(len(mz.mq19)))if order is None else order
  mz.mv=[sum((mq18[p]==mq2[p]for p in mq10))for mq10 in mz.regions]
  mz.stampmask=sum((1<<c*j+value for j,value in enumerate(mq17)))
  mz.size=d*d
  mz.all_actions=(1<<len(mz.mq19))-1
  mz.target_bits=[[0]*c for _ in mq17]
  mz.region_bits=[0]*len(mz.regions)
  for rank,action in enumerate(mz.order):
   bit=1<<rank
   mz.region_bits[action>>2]|=bit
   for j,p in enumerate(mz.mq19[action][0]):
    mz.target_bits[j][mq2[p]]|=bit
  mz.old_planes=[0]*4
  for region,count in enumerate(mz.mv):
   value=mz.size-count
   for plane in range(4):
    if value&1<<plane:
     mz.old_planes[plane]|=mz.region_bits[region]
 def gain(mz,action):
  return(mz.stampmask&mz.masks[action]).bit_count()-mz.mv[action>>2]
 def apply(mz,action):
  mq10,_=mz.mq19[action]
  mq18,mq17,mq2=(mz.mq18,mz.mq17,mz.mq2)
  mv,planes=(mz.mv,mz.old_planes)
  cover=mz.cover
  cover_bits=getattr(mz,'_runtime_cover_bits',None)
  if cover_bits is None:
   region_bits=mz.region_bits
   cover_bits=[sum((region_bits[r]for r in ids))for ids in cover]
   mz._runtime_cover_bits=cover_bits
  for j,p in enumerate(mq10):
   old,new=(mq18[p],mq17[j])
   mq17[j],mq18[p]=(old,new)
   delta=(new==mq2[p])-(old==mq2[p])
   mz.matches+=delta
   if delta:
    for region in cover[p]:
     mv[region]+=delta
    carry=cover_bits[p]
    plane=0
    if delta>0:
     while carry:
      mq15=planes[plane]
      planes[plane]=mq15^carry
      carry&=~mq15
      plane+=1
    else:
     while carry:
      mq15=planes[plane]
      planes[plane]=mq15^carry
      carry&=mq15
      plane+=1
  c=mz.c
  mz.stampmask=sum((1<<c*j+value for j,value in enumerate(mq17)))
 def best_candidates(mz):
  planes=[0]*5
  for j,color in enumerate(mz.mq17):
   carry=mz.target_bits[j][color]
   plane=0
   while carry:
    mq15=planes[plane]
    planes[plane]=mq15^carry
    carry&=mq15
    plane+=1
  carry=0
  for plane in range(4):
   a,b=(planes[plane],mz.old_planes[plane])
   different=a^b
   planes[plane]=different^carry
   carry=a&b|different&carry
  planes[4]=carry
  mq5,value=(mz.all_actions,0)
  for plane in range(4,-1,-1):
   hits=mq5&planes[plane]
   if hits:
    mq5=hits
    value|=1<<plane
  return(value-mz.size,mq5)
 def best(mz):
  gain,mq5=mz.best_candidates()
  rank=(mq5&-mq5).bit_length()-1
  return(gain,mz.order[rank])
 def escape(mz,rng,width=64):
  mask,mv=(mz.stampmask,mz.mv)
  mq5=[(mask&m).bit_count()-mv[i>>2]for i,m in enumerate(mz.masks)]
  eligible=[i for i,g in enumerate(mq5)if g>=-2]
  rng.shuffle(eligible)
  top=heapq.nlargest(8,eligible,key=lambda i:mq5[i])
  ordered=top+eligible
  seen,tried=(set(),set())
  best_total,pair=(0,None)
  examined=0
  saved_counts=mz.mv[:]
  saved_planes=mz.old_planes[:]
  saved_matches=mz.matches
  for first in ordered:
   if first in tried:
    continue
   tried.add(first)
   mq10,_=mz.mq19[first]
   mq9=tuple((mz.mq18[p]for p in mq10))
   signature=(mq9,mq5[first])
   if signature in seen:
    continue
   seen.add(signature)
   first_gain=mq5[first]
   mz.apply(first)
   second_gain,second=mz.best()
   total=first_gain+second_gain
   mq18,mq17=(mz.mq18,mz.mq17)
   for j,p in enumerate(mq10):
    mq17[j],mq18[p]=(mq18[p],mq17[j])
   mz.mv[:]=saved_counts
   mz.old_planes[:]=saved_planes
   mz.matches=saved_matches
   mz.stampmask=mask
   if total>best_total:
    best_total,pair=(total,(first,second))
   examined+=1
   if examined>=width:
    break
  return pair
def solve_lookahead(n,d,c,k,mq18,mq2,mq17):
 seed=n*101+d*19+c*7+k
 for p in range(0,len(mq18),11):
  seed=seed*131+mq18[p]*7+mq2[p]&4294967295
 mq7,best_operations=(-1,[])
 for restart in range(8):
  rng=random.Random(seed+restart*87917)
  order=list(range(4*(n-d+1)**2))
  if restart:
   rng.shuffle(order)
  my=State(n,d,c,mq18.copy(),mq2,mq17.copy(),order)
  mq8=[]
  while len(mq8)<k and my.matches<my.limit:
   gain,action=my.best()
   if gain>0:
    my.apply(action)
    mq8.append(my.mq19[action][1])
   elif len(mq8)+2<=k:
    pair=my.escape(rng)
    if pair is None:
     break
    for action in pair:
     my.apply(action)
     mq8.append(my.mq19[action][1])
   else:
    break
  matches=sum((a==t for a,t in zip(my.mq18,mq2)))
  if matches>mq7:
   mq7,best_operations=(matches,mq8)
  if mq7==my.limit:
   break
 return best_operations
def construct(n,d,c,k,mq18,mq2,mq17):
 limit=color_bound(mq18+mq17,mq2)
 if sum((a==b for a,b in zip(mq18,mq2)))==limit:
  return[]
 mq10,codes,mq8,coverage,patches=build(n,d,mq2)
 width=n-d+1
 mq7=-1
 best_ops=[]
 for search in(solve_plateau,solve_lookahead,solve_productive):
  ops=search(n,d,c,k,mq18[:],mq2,mq17[:])
  final,buffer=(mq18[:],mq17[:])
  for x,y,r in ops:
   action=(x*width+y)*4+r
   transition(final,buffer,mq10[action])
  matches=sum((a==b for a,b in zip(final,mq2)))
  if matches>mq7:
   mq7,best_ops=(matches,ops)
  if matches==limit:
   break
 return best_ops
import random
import sys
class ProductiveState(State):
 def escape(mz,rng,width=64,min_gain=-2):
  mask,mv=(mz.stampmask,mz.mv)
  mq5=[(mask&m).bit_count()-mv[i>>2]for i,m in enumerate(mz.masks)]
  eligible=[i for i,g in enumerate(mq5)if g>=min_gain]
  rng.shuffle(eligible)
  top=heapq.nlargest(8,eligible,key=lambda i:mq5[i])
  ordered=top+eligible
  seen,tried=(set(),set())
  best_total,pair=(0,None)
  examined=0
  saved_counts=mz.mv[:]
  saved_planes=mz.old_planes[:]
  saved_matches=mz.matches
  for first in ordered:
   if first in tried:
    continue
   tried.add(first)
   mq10,_=mz.mq19[first]
   mq9=tuple((mz.mq18[p]for p in mq10))
   signature=(mq9,mq5[first])
   if signature in seen:
    continue
   seen.add(signature)
   first_gain=mq5[first]
   mz.apply(first)
   second_gain,second=mz.best()
   total=first_gain+second_gain
   mq18,mq17=(mz.mq18,mz.mq17)
   for j,p in enumerate(mq10):
    mq17[j],mq18[p]=(mq18[p],mq17[j])
   mz.mv[:]=saved_counts
   mz.old_planes[:]=saved_planes
   mz.matches=saved_matches
   mz.stampmask=mask
   if total>best_total:
    best_total,pair=(total,(first,second))
   examined+=1
   if examined>=width:
    break
  return pair
def solve_productive(n,d,c,k,mq18,mq2,mq17):
 my=ProductiveState(n,d,c,mq18,mq2,mq17)
 seed=n*101+d*19+c*7+k
 for p in range(0,len(mq18),11):
  seed=seed*131+mq18[p]*7+mq2[p]&4294967295
 rng=random.Random(seed)
 mq8=[]
 while len(mq8)<k and my.matches<my.limit:
  gain,action=my.best()
  if gain>0:
   if len(mq8)+2<=k:
    pair=my.escape(rng,width=8,min_gain=max(1,gain-1))
    if pair is not None:
     action=pair[0]
   my.apply(action)
   mq8.append(my.mq19[action][1])
  elif len(mq8)+2<=k:
   pair=my.escape(rng)
   if pair is None:
    break
   for action in pair:
    my.apply(action)
    mq8.append(my.mq19[action][1])
  else:
   break
 return mq8
def _st(my,nn,mq10):
 for j,pos in enumerate(mq10):
  my[nn+j],my[pos]=(my[pos],my[nn+j])
def best_action(my,mu,mq19,nn,dd,mx=-1,allow_zero=False):
 mq18,wanted=(my[:nn],mu[:nn])
 losses=[value==goal for value,goal in zip(mq18,wanted)]
 rows=[]
 for j in range(dd):
  carried,goal=(my[nn+j],mu[nn+j])
  fixed_loss=carried==goal
  rows.append([(carried==desire)+(value==goal)-loss-fixed_loss for value,desire,loss in zip(mq18,wanted,losses)])
 best_id,mw=(-1,0)
 if mx>=0:
  old=sum((rows[j][pos]for j,pos in enumerate(mq19[mx][0])))
  if old>=0:
   best_id,mw=(mx,old)
 if dd==4:
  g0,g1,g2,g3=rows
  for aid,(p,_)in enumerate(mq19):
   gain=g0[p[0]]+g1[p[1]]+g2[p[2]]+g3[p[3]]
   if gain>mw or(allow_zero and best_id<0 and(gain==mw)):
    best_id,mw=(aid,gain)
 else:
  g0,g1,g2,g3,g4,g5,g6,g7,g8=rows
  for aid,(p,_)in enumerate(mq19):
   gain=g0[p[0]]+g1[p[1]]+g2[p[2]]+g3[p[3]]+g4[p[4]]+g5[p[5]]+g6[p[6]]+g7[p[7]]+g8[p[8]]
   if gain>mw or(allow_zero and best_id<0 and(gain==mw)):
    best_id,mw=(aid,gain)
 return(best_id,mw)
def greedy(n,d,k,mq18,mq2,mq17,mq19):
 nn,dd=(n*n,d*d)
 my,mu=(mq18+mq17,mq2+[-1]*dd)
 mq0=[]
 for _ in range(k):
  aid,gain=best_action(my,mu,mq19,nn,dd)
  if gain<=0:
   break
  _st(my,nn,mq19[aid][0])
  mq0.append(aid)
 return mq0
_REFINE_GEOMETRY={}
_REFINE_COVER_BITS={}
_REFINE_GOALS={}
class RefineState:
 def __init__(mz,n,d,mq1,mq2,mq19,order):
  nn,dd=(n*n,d*d)
  mz.nn,mz.dd=(nn,dd)
  mz.mq18,mz.mq17=(mq1[:nn],mq1[nn:])
  mz.mu,mz.wstamp=(mq2[:],[6]*dd)
  mz.mq19,mz.order=(mq19,order)
  size=len(mq19)
  mz.all_bits=(1<<size)-1
  key=(n,d)
  geometry=_REFINE_GEOMETRY.get(key)
  if geometry is None:
   mq16=[[0]*nn for _ in range(dd)]
   region_bits=[15<<4*r for r in range(size//4)]
   regions=[mq19[i][0]for i in range(0,size,4)]
   cover=[[]for _ in range(nn)]
   for r,patch in enumerate(regions):
    for p in patch:
     cover[p].append(r)
   for aid,(patch,_)in enumerate(mq19):
    bit=1<<aid
    for j,p in enumerate(patch):
     mq16[j][p]|=bit
   geometry=(mq16,region_bits,regions,cover)
   _REFINE_GEOMETRY[key]=geometry
  mz.mq16,mz.region_bits,mz.regions,mz.cover=geometry
  cover_bits=_REFINE_COVER_BITS.get(key)
  if cover_bits is None:
   cover_bits=[sum((mz.region_bits[r]for r in ids))for ids in mz.cover]
   _REFINE_COVER_BITS[key]=cover_bits
  mz.cover_bits=cover_bits
  mz.values=[[0]*7 for _ in range(dd)]
  goal_key=(n,d,tuple(mq2))
  cached_goals=_REFINE_GOALS.get(goal_key)
  if cached_goals is None:
   cached_goals=[[0]*7 for _ in range(dd)]
   for j in range(dd):
    goals=cached_goals[j]
    for p,mask in enumerate(mz.mq16[j]):
     goals[mq2[p]]|=mask
   _REFINE_GOALS[goal_key]=cached_goals
  mz.goals=[row[:]for row in cached_goals]
  for j in range(dd):
   values=mz.values[j]
   for p,mask in enumerate(mz.mq16[j]):
    values[mz.mq18[p]]|=mask
  mz.tie_masks=[0]*size.bit_length()
  for rank,aid in enumerate(order):
   bit=1<<aid
   while rank:
    low=rank&-rank
    mz.tie_masks[low.bit_length()-1]|=bit
    rank^=low
  mz.old_planes=[0]*5
  planes=mz.old_planes
  for p in range(nn):
   if mz.mq18[p]!=mz.mu[p]:
    carry=cover_bits[p]
    level=0
    while carry:
     before=planes[level]
     planes[level]=before^carry
     carry&=before
     level+=1
  mz.mv=None
 def apply(mz,action,mu=False):
  if mu:
   mq18,mq17,bits,opposite=(mz.mu,mz.wstamp,mz.goals,mz.mq18)
  else:
   mq18,mq17,bits,opposite=(mz.mq18,mz.mq17,mz.values,mz.mu)
  mq16=mz.mq16
  planes,cover_bits=(mz.old_planes,mz.cover_bits)
  for j,p in enumerate(mz.mq19[action][0]):
   old,new=(mq18[p],mq17[j])
   if old!=new:
    for ref in range(mz.dd):
     mask=mq16[ref][p]
     bits[ref][old]^=mask
     bits[ref][new]^=mask
    delta=(new==opposite[p])-(old==opposite[p])
    if delta:
     carry=cover_bits[p]
     plane=0
     if delta>0:
      while carry:
       mq15=planes[plane]
       planes[plane]=mq15^carry
       carry&=~mq15
       plane+=1
     else:
      while carry:
       mq15=planes[plane]
       planes[plane]=mq15^carry
       carry&=mq15
       plane+=1
    mq17[j],mq18[p]=(old,new)
 def best(mz):
  planes=[0]*5
  for j in range(mz.dd):
   for carry in(mz.values[j][mz.wstamp[j]],mz.goals[j][mz.mq17[j]]):
    plane=0
    while carry:
     old=planes[plane]
     planes[plane]=old^carry
     carry&=old
     plane+=1
  carry=0
  for plane in range(5):
   a,b=(planes[plane],mz.old_planes[plane])
   different=a^b
   planes[plane]=different^carry
   carry=a&b|different&carry
  mq5,value=(mz.all_bits,0)
  for plane in range(4,-1,-1):
   hits=mq5&planes[plane]
   if hits:
    mq5=hits
    value|=1<<plane
  gain=value-mz.dd-sum((a==b for a,b in zip(mz.mq17,mz.wstamp)))
  if gain<0:
   return(-1,0)
  for mask in reversed(mz.tie_masks):
   if not mq5&mq5-1:
    break
   preferred=mq5&~mask
   if preferred:
    mq5=preferred
  return((mq5&-mq5).bit_length()-1,gain)
def refine(n,d,k,mq1,mq2,mq19,mq0,passes=8,offset=0,seed_offset=0):
 nn,dd=(n*n,d*d)
 limit=color_bound(mq1,mq2)
 seed=sum(((i+1)*v for i,v in enumerate(mq1)))+k*131+seed_offset
 rng=random.Random(seed)
 for _ in range(offset):
  rng.shuffle(list(range(len(mq19))))
 for iteration in range(passes):
  mq0=mq0+[-1]*min(8,k-len(mq0))
  final=mq1[:]
  for action in mq0:
   if action>=0:
    _st(final,nn,mq19[action][0])
  if sum((a==b for a,b in zip(final,mq2)))==limit:
   return[action for action in mq0 if action>=0]
  order=list(range(len(mq19)))
  rng.shuffle(order)
  my=RefineState(n,d,final,mq2,mq19,order)
  for i in range(len(mq0)-1,-1,-1):
   old=mq0[i]
   if old>=0:
    my.apply(old)
   chosen,_=my.best()
   mq0[i]=chosen
   if chosen>=0:
    my.apply(chosen,mu=True)
  mq0=[action for action in mq0 if action>=0]
 return mq0
class SequenceState:
 def __init__(mz,mq1,mq2,mq19,mq0,nn):
  mz.nn=nn
  mz.mq19=mq19
  mz.mq0=mq0[:]
  mz.prefix=[mq1[:]]
  for aid in mq0:
   my=mz.prefix[-1][:]
   if aid>=0:
    _st(my,nn,mq19[aid][0])
   mz.prefix.append(my)
  mz.mu=[None]*(len(mq0)+1)
  mz.mu[-1]=mq2+[-1]*(len(mq1)-nn)
  for i in range(len(mq0)-1,-1,-1):
   wanted=mz.mu[i+1][:]
   if mq0[i]>=0:
    _st(wanted,nn,mq19[mq0[i]][0])
   mz.mu[i]=wanted
  mz.score=sum((x==y for x,y in zip(mz.prefix[-1],mq2)))
 def delta(mz,i,replacements):
  nn,mq19=(mz.nn,mz.mq19)
  mq9=mz.prefix[i][:]
  affected=set(range(nn,len(mq9)))
  for old,new in zip(mz.mq0[i:i+len(replacements)],replacements):
   if old>=0:
    affected.update(mq19[old][0])
   if new>=0:
    mq10=mq19[new][0]
    affected.update(mq10)
    _st(mq9,nn,mq10)
  mq15=mz.prefix[i+len(replacements)]
  mu=mz.mu[i+len(replacements)]
  return sum(((mq9[p]==mu[p])-(mq15[p]==mu[p])for p in affected))
 def accept(mz,i,replacements,delta):
  nn,mq19=(mz.nn,mz.mq19)
  mz.mq0[i:i+len(replacements)]=replacements
  for j in range(i,len(mz.mq0)):
   my=mz.prefix[j][:]
   aid=mz.mq0[j]
   if aid>=0:
    _st(my,nn,mq19[aid][0])
   mz.prefix[j+1]=my
  for j in range(i+len(replacements)-1,-1,-1):
   wanted=mz.mu[j+1][:]
   aid=mz.mq0[j]
   if aid>=0:
    _st(wanted,nn,mq19[aid][0])
   mz.mu[j]=wanted
  mz.score+=delta
def pair_repair(n,d,k,mq1,mq2,mq19,mq0,proposals=None):
 if k<2:
  return mq0
 nn,dd=(n*n,d*d)
 my=SequenceState(mq1,mq2,mq19,mq0+[-1]*(k-len(mq0)),nn)
 if my.score==color_bound(mq1,mq2):
  return mq0
 rng=random.Random(sum(((i+7)*v for i,v in enumerate(mq1)))+k*977+9167)
 width=n-d+1
 if proposals is None:
  proposals=min(2400,max(160,450000//nn))
 for step in range(proposals):
  i=rng.randrange(k-1)
  fixed_slot=step%2
  old=my.mq0[i+fixed_slot]
  mode=rng.randrange(5)
  if mode<2 and old>=0:
   x,y,r=mq19[old][1]
   x=min(width-1,max(0,x+rng.choice((-2,-1,0,0,1,2))))
   y=min(width-1,max(0,y+rng.choice((-2,-1,0,0,1,2))))
   action=(x*width+y)*4+rng.randrange(4)
  elif mode==4:
   action=-1
  else:
   action=rng.randrange(len(mq19))
  if fixed_slot==0:
   before=my.prefix[i][:]
   if action>=0:
    _st(before,nn,mq19[action][0])
   second,_=best_action(before,my.mu[i+2],mq19,nn,dd,mx=my.mq0[i+1],allow_zero=True)
   replacements=[action,second]
  else:
   wished=my.mu[i+2][:]
   if action>=0:
    _st(wished,nn,mq19[action][0])
   first,_=best_action(my.prefix[i],wished,mq19,nn,dd,mx=my.mq0[i],allow_zero=True)
   replacements=[first,action]
  if my.mq0[i:i+2]==replacements:
   continue
  delta=my.delta(i,replacements)
  if delta>0 or(delta==0 and rng.randrange(8)==0):
   my.accept(i,replacements,delta)
   if my.score==color_bound(mq1,mq2):
    break
 return[aid for aid in my.mq0 if aid>=0]
def _og(my,action):
 if action<0:
  return 0
 gain=0
 for j,p in enumerate(my.mq19[action][0]):
  v,w=(my.mq17[j],my.mq18[p])
  a,b=(my.mu[p],my.wstamp[j])
  gain+=(v==a)+(w==b)-(w==a)-(v==b)
 return gain
def refine_trial(my,action,mu=False):
 if action<0:
  return None
 if mu:
  mq18,mq17,bits=(my.mu,my.wstamp,my.goals)
 else:
  mq18,mq17,bits=(my.mq18,my.mq17,my.values)
 patch=my.mq19[action][0]
 undo=(mu,patch,[mq18[p]for p in patch],mq17[:],[row[:]for row in bits],my.mv[:]if my.mv is not None else None,my.old_planes[:])
 my.apply(action,mu=mu)
 return undo
def refine_restore(my,undo):
 if undo is None:
  return
 mu,patch,colors,mq17,bits,mv,planes=undo
 mq18=my.mu if mu else my.mq18
 for p,color in zip(patch,colors):
  mq18[p]=color
 if mu:
  my.wstamp,my.goals=(mq17,bits)
 else:
  my.mq17,my.values=(mq17,bits)
 my.mv,my.old_planes=(mv,planes)
def optimize_pair(my,first,second,mq5):
 best=_og(my,first)
 undo=refine_trial(my,first)
 best+=_og(my,second)
 refine_restore(my,undo)
 answer=(first,second)
 if best<0:
  best,answer=(0,(-1,-1))
 for fixed,side in mq5:
  gain=_og(my,fixed)
  undo=refine_trial(my,fixed,mu=bool(side))
  chosen,other=my.best()
  refine_restore(my,undo)
  total=gain+other
  if total>=best:
   best=total
   answer=(chosen,fixed)if side else(fixed,chosen)
 return answer
def pair_sweep(n,d,k,mq1,mq2,mq19,mq0,passes=4,width=32):
 nn=n*n
 side_len=n-d+1
 rng=random.Random(sum(((i+13)*v for i,v in enumerate(mq1)))+k*691+7147)
 for iteration in range(passes):
  mq0=mq0+[-1]*min(8,k-len(mq0))
  final=mq1[:]
  for action in mq0:
   if action>=0:
    _st(final,nn,mq19[action][0])
  if sum((a==b for a,b in zip(final,mq2)))==color_bound(mq1,mq2):
   return[action for action in mq0 if action>=0]
  order=list(range(len(mq19)))
  rng.shuffle(order)
  my=RefineState(n,d,final,mq2,mq19,order)
  i=len(mq0)-1
  if iteration%2 and i>=0:
   old=mq0[i]
   if old>=0:
    my.apply(old)
   chosen,_=my.best()
   mq0[i]=chosen
   if chosen>=0:
    my.apply(chosen,mu=True)
   i-=1
  while i>=1:
   first,second=(mq0[i-1],mq0[i])
   if second>=0:
    my.apply(second)
   if first>=0:
    my.apply(first)
   mq5=[(first,0),(second,1),(-1,0),(-1,1)]
   for _ in range(width):
    side=rng.randrange(2)
    old=second if side else first
    mode=rng.randrange(4)
    if mode==0 and old>=0:
     x,y,r=mq19[old][1]
     x=min(side_len-1,max(0,x+rng.choice((-1,0,1))))
     y=min(side_len-1,max(0,y+rng.choice((-1,0,1))))
     mq4=(x*side_len+y)*4+rng.randrange(4)
    elif mode==1:
     mq4=rng.choice(mq0)
    else:
     mq4=rng.randrange(len(mq19))
    mq5.append((mq4,side))
   first,second=optimize_pair(my,first,second,mq5)
   mq0[i-1],mq0[i]=(first,second)
   if second>=0:
    my.apply(second,mu=True)
   if first>=0:
    my.apply(first,mu=True)
   i-=2
  if i==0:
   old=mq0[0]
   if old>=0:
    my.apply(old)
   mq0[0],_=my.best()
  mq0=[action for action in mq0 if action>=0]
 return mq0
def iterated_refine(n,d,k,mq1,mq2,mq19,mq0):
 if n>16:
  return mq0
 nn=n*n
 def evaluate(path):
  final=mq1[:]
  for action in path:
   if action>=0:
    _st(final,nn,mq19[action][0])
  return sum((a==b for a,b in zip(final,mq2)))
 mq6=evaluate(mq0)
 limit=color_bound(mq1,mq2)
 if mq6==limit:
  return mq0
 rng=random.Random(sum(((i+29)*v for i,v in enumerate(mq1)))+k*2281)
 best=mq0[:]
 width=n-d+1
 restarts=max(2,min(8,9000//(nn+6*k)))
 for restart in range(restarts):
  mq4=best+[-1]*min(8,k-len(best))
  mq16=rng.sample(range(len(mq4)),min(len(mq4),2+restart%6))
  for position in mq16:
   old=mq4[position]
   mode=rng.randrange(4)
   if old>=0 and mode<2:
    x,y,r=mq19[old][1]
    x=max(0,min(width-1,x+rng.choice((-2,-1,0,1,2))))
    y=max(0,min(width-1,y+rng.choice((-2,-1,0,1,2))))
    mq4[position]=(x*width+y)*4+rng.randrange(4)
   elif mode==2:
    mq4[position]=-1
   else:
    mq4[position]=rng.randrange(len(mq19))
  mq4=refine(n,d,k,mq1,mq2,mq19,mq4,passes=4,seed_offset=37307*(restart+1))
  score=evaluate(mq4)
  if score>=mq6:
   best,mq6=(mq4,score)
   if score==limit:
    break
 return best
class WeightedState(State):
 def __init__(mz,n,d,c,mq18,mq2,mq17,order=None):
  super().__init__(n,d,c,mq18,mq2,mq17,order)
  mz.weights=[2 if min(p//n,p%n,n-1-p//n,n-1-p%n)<d-1 else 1 for p in range(n*n)]
  mz.size=2*d*d
  mz.heavy_bits=[[0]*c for _ in mq17]
  for rank,action in enumerate(mz.order):
   bit=1<<rank
   for j,p in enumerate(mz.mq19[action][0]):
    if mz.weights[p]==2:
     mz.heavy_bits[j][mq2[p]]|=bit
  mz.mv=[sum((mz.weights[p]for p in mq16 if mq18[p]==mq2[p]))for mq16 in mz.regions]
  mz.old_planes=[0]*6
  for region,count in enumerate(mz.mv):
   value=mz.size-count
   for plane in range(6):
    if value&1<<plane:
     mz.old_planes[plane]|=mz.region_bits[region]
 def gain(mz,action):
  return sum((mz.weights[p]for j,p in enumerate(mz.mq19[action][0])if mz.mq17[j]==mz.mq2[p]))-mz.mv[action>>2]
 def apply(mz,action):
  mq10,_=mz.mq19[action]
  mq18,mq17,mq2=(mz.mq18,mz.mq17,mz.mq2)
  changed={}
  for j,p in enumerate(mq10):
   old,new=(mq18[p],mq17[j])
   mq17[j],mq18[p]=(old,new)
   delta=(new==mq2[p])-(old==mq2[p])
   mz.matches+=delta
   if delta:
    delta*=mz.weights[p]
    for region in mz.cover[p]:
     changed[region]=changed.get(region,0)+delta
  mv,planes,region_bits=(mz.mv,mz.old_planes,mz.region_bits)
  size=mz.size
  for region,delta in changed.items():
   if not delta:
    continue
   old=mv[region]
   new=old+delta
   mv[region]=new
   changed_planes=size-old^size-new
   bits=region_bits[region]
   while changed_planes:
    bit=changed_planes&-changed_planes
    planes[bit.bit_length()-1]^=bits
    changed_planes^=bit
  c=mz.c
  mz.stampmask=sum((1<<c*j+value for j,value in enumerate(mq17)))
 def best_candidates(mz):
  planes=[0]*6
  for j,color in enumerate(mz.mq17):
   heavy=mz.heavy_bits[j][color]
   for plane,carry in((0,mz.target_bits[j][color]^heavy),(1,heavy)):
    while carry:
     mq15=planes[plane]
     planes[plane]=mq15^carry
     carry&=mq15
     plane+=1
  carry=0
  for plane in range(6):
   a,b=(planes[plane],mz.old_planes[plane])
   different=a^b
   planes[plane]=different^carry
   carry=a&b|different&carry
  mq5,value=(mz.all_actions,0)
  for plane in range(5,-1,-1):
   hits=mq5&planes[plane]
   if hits:
    mq5=hits
    value|=1<<plane
  return(value-mz.size,mq5)
def solve_weighted(n,d,c,k,mq1,mq2,start_stamp):
 seed=7418729
 for value in mq1+mq2+start_stamp:
  seed=(seed^value)*1000003&4294967295
 rng=random.Random(seed)
 order=list(range(4*(n-d+1)**2))
 _is=sum((a==b for a,b in zip(mq1,mq2)))
 mq6,answer=(_is,[])
 limit=color_bound(mq1+start_stamp,mq2)
 if mq6==limit:
  return answer
 for restart in range(4):
  if restart:
   rng.shuffle(order)
  my=WeightedState(n,d,c,mq1[:],mq2,start_stamp[:],order[:])
  path,seen,score=([],set(),_is)
  for _ in range(k):
   seen.add(tuple(my.mq17))
   gain,mq5=my.best_candidates()
   if gain<0:
    break
   chosen=-1
   while mq5:
    bit=mq5&-mq5
    action=my.order[bit.bit_length()-1]
    if gain>0 or tuple((my.mq18[p]for p in my.mq19[action][0]))not in seen:
     chosen=action
     break
    mq5^=bit
   if chosen<0:
    break
   if gain>0:
    seen.clear()
   score+=sum(((my.mq17[j]==mq2[p])-(my.mq18[p]==mq2[p])for j,p in enumerate(my.mq19[chosen][0])))
   my.apply(chosen)
   path.append(my.mq19[chosen][1])
   if score>mq6:
    mq6,answer=(score,path[:])
   if mq6==limit:
    return answer
 return answer
def construct_pool(n,d,c,k,mq18,mq2,mq17):
 limit=color_bound(mq18+mq17,mq2)
 _is=sum((a==b for a,b in zip(mq18,mq2)))
 if _is==limit:
  return[(limit,[])]
 mq10,codes,mq8,coverage,patches=build(n,d,mq2)
 width=n-d+1
 mq5=[]
 for search in(solve_plateau,solve_lookahead,solve_productive,solve_weighted):
  ops=search(n,d,c,k,mq18[:],mq2,mq17[:])
  final,buffer=(mq18[:],mq17[:])
  for x,y,r in ops:
   action=(x*width+y)*4+r
   transition(final,buffer,mq10[action])
  matches=sum((a==b for a,b in zip(final,mq2)))
  mq5.append((matches,ops))
  if matches==limit:
   break
 mq5.sort(key=lambda row:row[0],reverse=True)
 return mq5
def solve_parent(n,d,c,k,mq18,mq2,mq17):
 pool=construct_pool(n,d,c,k,mq18[:],mq2,mq17[:])
 if pool[0][0]==color_bound(mq18+mq17,mq2):
  return pool[0][1]
 mq10,_,ops,_,_=build(n,d,mq2)
 mq19=list(zip(mq10,ops))
 width=n-d+1
 mq1=mq18+mq17
 mq6,_bs=(-1,[])
 for _,mq8 in pool[:4]:
  mq0=[(x*width+y)*4+r for x,y,r in mq8]
  mq0=refine(n,d,k,mq1,mq2,mq19,mq0,passes=2)
  my=mq1[:]
  for aid in mq0:
   _st(my,n*n,mq19[aid][0])
  score=sum((a==b for a,b in zip(my,mq2)))
  if score>mq6:
   mq6,_bs=(score,mq0)
 mq0=refine(n,d,k,mq1,mq2,mq19,_bs,passes=6,offset=2)
 mq0=pair_sweep(n,d,k,mq1,mq2,mq19,mq0)
 mq0=pair_repair(n,d,k,mq1,mq2,mq19,mq0)
 mq0=refine(n,d,k,mq1,mq2,mq19,mq0,passes=2)
 mq0=iterated_refine(n,d,k,mq1,mq2,mq19,mq0)
 return[mq19[aid][1]for aid in mq0]
def clone_state(my):
 child=object.__new__(State)
 child.__dict__=my.__dict__.copy()
 child.mq18=my.mq18[:]
 child.mq17=my.mq17[:]
 child.mv=my.mv[:]
 child.old_planes=my.old_planes[:]
 return child
def beam_actions(my,rng):
 mask,mv=(my.stampmask,my.mv)
 gains=[(mask&m).bit_count()-mv[i>>2]for i,m in enumerate(my.masks)]
 best=max(gains)
 groups=[[],[],[]]
 for action,gain in enumerate(gains):
  distance=best-gain
  if distance<3:
   groups[distance].append(action)
 mq13=[]
 for group,limit in zip(groups,(4,3,1)):
  rng.shuffle(group)
  seen={}
  for action in group:
   mq9=tuple((my.mq18[p]for p in my.mq19[action][0]))
   if seen.get(mq9,0)>=2:
    continue
   seen[mq9]=seen.get(mq9,0)+1
   mq13.append((action,gains[action]))
   limit-=1
   if limit==0:
    break
 return mq13
def finite_beam(n,d,c,k,mq18,mq2,mq17,width=24):
 mq1=State(n,d,c,mq18[:],mq2,mq17[:])
 base_score=sum((a==b for a,b in zip(mq18,mq2)))
 supply=[0]*c
 wanted=[0]*c
 for color in mq18+mq17:
  supply[color]+=1
 for color in mq2:
  wanted[color]+=1
 upper_gain=sum((min(a,b)for a,b in zip(supply,wanted)))-base_score
 if upper_gain<=0:
  return[]
 seed=47893+k*1009+n*79+d*13+c
 for value in mq18+mq17:
  seed=seed*131+value&4294967295
 rng=random.Random(seed)
 beam=[(mq1,0,[])]
 mw,best_path=(0,[])
 for depth in range(k):
  children=[]
  seen_states=set()
  for my,gain,path in beam:
   for action,delta in beam_actions(my,rng):
    if path and action==path[-1]:
     continue
    child=clone_state(my)
    child.apply(action)
    signature=bytes(child.mq18)+bytes(child.mq17)
    if signature in seen_states:
     continue
    seen_states.add(signature)
    total=gain+delta
    new_path=path+[action]
    if total>mw:
     mw,best_path=(total,new_path)
     if mw==upper_gain:
      return[mq1.mq19[aid][1]for aid in best_path]
    future=max(0,child.best()[0])if depth+1<k else 0
    priority=total*2+future
    children.append((priority,total,child,new_path))
  if not children:
   break
  children.sort(key=lambda item:(item[0],item[1]),reverse=True)
  beam=[]
  carried_counts={}
  deferred=[]
  for priority,gain,my,path in children:
   key=tuple(my.mq17)
   if carried_counts.get(key,0)>=3:
    deferred.append((my,gain,path))
    continue
   carried_counts[key]=carried_counts.get(key,0)+1
   beam.append((my,gain,path))
   if len(beam)==width:
    break
  if len(beam)<width:
   beam.extend(deferred[:width-len(beam)])
 return[mq1.mq19[aid][1]for aid in best_path]
def exact_two(n,d,c,k,mq18,mq2,mq17):
 my=State(n,d,c,mq18[:],mq2,mq17[:])
 gain,action=my.best()
 mw,best_path=(max(0,gain),[action]if gain>0 else[])
 if k==1:
  return[my.mq19[aid][1]for aid in best_path]
 ranked=[(my.gain(aid),aid)for aid in range(len(my.mq19))]
 ranked.sort(reverse=True)
 for first_gain,first in ranked:
  if first_gain+d*d<=mw:
   break
  my.apply(first)
  second_gain,second=my.best()
  total=first_gain+second_gain
  my.apply(first)
  if total>mw:
   mw,best_path=(total,[first,second])
 return[my.mq19[aid][1]for aid in best_path]
def construct_all(n,d,c,k,mq18,mq2,mq17):
 if k<=2:
  return exact_two(n,d,c,k,mq18,mq2,mq17)
 mq3=solve_parent(n,d,c,k,mq18[:],mq2,mq17[:])
 if k>24:
  return mq3
 mq4=finite_beam(n,d,c,k,mq18,mq2,mq17,width=24 if k<=12 else 12)
 mq10,_,ops,_,_=build(n,d,mq2)
 mq19=list(zip(mq10,ops))
 width=n-d+1
 mq0=[(x*width+y)*4+r for x,y,r in mq4]
 mq0=refine(n,d,k,mq18+mq17,mq2,mq19,mq0)
 mq4=[mq19[aid][1]for aid in mq0]
 mq6,best_ops=(-1,[])
 for mq8 in(mq3,mq4):
  final,buffer=(mq18[:],mq17[:])
  for x,y,r in mq8:
   transition(final,buffer,mq10[(x*width+y)*4+r])
  score=sum((a==b for a,b in zip(final,mq2)))
  if score>mq6:
   mq6,best_ops=(score,mq8)
 return best_ops
def optimize_triple(my,first,middle,last,left,right):
 best=_og(my,first)
 outer=refine_trial(my,first)
 best+=_og(my,middle)
 inner=refine_trial(my,middle)
 best+=_og(my,last)
 refine_restore(my,inner)
 refine_restore(my,outer)
 answer=(first,middle,last)
 for first in left:
  base=_og(my,first)
  outer=refine_trial(my,first)
  for last in right:
   extra=_og(my,last)
   inner=refine_trial(my,last,mu=True)
   middle,gain=my.best()
   refine_restore(my,inner)
   total=base+extra+gain
   if total>=best:
    best=total
    answer=(first,middle,last)
  refine_restore(my,outer)
 return answer
def triple_refine(n,d,k,mq1,mq2,mq19,mq0,passes=2):
 if k<3:
  return mq0
 nn=n*n
 limit=color_bound(mq1,mq2)
 size=n-d+1
 rng=random.Random(sum(((i+17)*v for i,v in enumerate(mq1)))+k*1777+71983)
 for iteration in range(passes):
  mq0=mq0+[-1]*min(6,k-len(mq0))
  final=mq1[:]
  for aid in mq0:
   if aid>=0:
    _st(final,nn,mq19[aid][0])
  if sum((a==b for a,b in zip(final,mq2)))==limit:
   return[aid for aid in mq0 if aid>=0]
  order=list(range(len(mq19)))
  rng.shuffle(order)
  my=RefineState(n,d,final,mq2,mq19,order)
  i=len(mq0)-1
  for _ in range(iteration%3):
   if i<0:
    break
   old=mq0[i]
   if old>=0:
    my.apply(old)
   chosen,_=my.best()
   mq0[i]=chosen
   if chosen>=0:
    my.apply(chosen,mu=True)
   i-=1
  while i>=2:
   first,middle,last=mq0[i-2:i+1]
   for aid in(last,middle,first):
    if aid>=0:
     my.apply(aid)
   preferred,_=my.best()
   pools=[]
   for old in(first,last):
    mode=rng.randrange(3)
    if mode==0 and old>=0:
     x,y,r=mq19[old][1]
     x=min(size-1,max(0,x+rng.choice((-1,0,1))))
     y=min(size-1,max(0,y+rng.choice((-1,0,1))))
     trial=(x*size+y)*4+rng.randrange(4)
    elif mode==1:
     p=rng.randrange(nn)
     for _ in range(10):
      p=rng.randrange(nn)
      if my.mu[p]<6 and my.mq18[p]!=my.mu[p]:
       break
     x=min(size-1,max(0,p//n-rng.randrange(d)))
     y=min(size-1,max(0,p%n-rng.randrange(d)))
     trial=(x*size+y)*4+rng.randrange(4)
    else:
     trial=rng.randrange(len(mq19))
    pools.append(list(dict.fromkeys((old,-1,preferred,trial))))
   for ending in pools[1]:
    undo=refine_trial(my,ending,mu=True)
    starting,_=my.best()
    refine_restore(my,undo)
    if starting not in pools[0]:
     pools[0].append(starting)
   first,middle,last=optimize_triple(my,first,middle,last,*pools)
   mq0[i-2:i+1]=(first,middle,last)
   for aid in(last,middle,first):
    if aid>=0:
     my.apply(aid,mu=True)
   i-=3
  while i>=0:
   old=mq0[i]
   if old>=0:
    my.apply(old)
   chosen,_=my.best()
   mq0[i]=chosen
   if chosen>=0:
    my.apply(chosen,mu=True)
   i-=1
  mq0=[aid for aid in mq0 if aid>=0]
 return mq0
def solve_original_iterated(n,d,c,k,mq18,mq2,mq17):
 mq8=construct_all(n,d,c,k,mq18[:],mq2,mq17[:])
 if k<=2:
  return mq8
 mq10,_,ops,_,_=build(n,d,mq2)
 mq19=list(zip(mq10,ops))
 side=n-d+1
 mq0=[(x*side+y)*4+r for x,y,r in mq8]
 mq0=triple_refine(n,d,k,mq18+mq17,mq2,mq19,mq0)
 mq0=refine(n,d,k,mq18+mq17,mq2,mq19,mq0,passes=2)
 return[mq19[aid][1]for aid in mq0]
def solve_retained_iterated(n,d,c,k,mq18,mq2,mq17):
 if n>16 or k<=2:
  return solve_original_iterated(n,d,c,k,mq18,mq2,mq17)
 mq1=mq18+mq17
 mq10,_,ops,_,_=build(n,d,mq2)
 mq19=list(zip(mq10,ops))
 width=n-d+1
 def evaluate(mq0):
  final=mq1[:]
  for aid in mq0:
   _st(final,n*n,mq10[aid])
  return sum((a==b for a,b in zip(final,mq2)))
 mq8=construct(n,d,c,k,mq18[:],mq2,mq17[:])
 base=[(x*width+y)*4+r for x,y,r in mq8]
 base=refine(n,d,k,mq1,mq2,mq19,base)
 base=pair_sweep(n,d,k,mq1,mq2,mq19,base)
 base=pair_repair(n,d,k,mq1,mq2,mq19,base)
 base=refine(n,d,k,mq1,mq2,mq19,base,passes=2)
 perturbed=iterated_refine(n,d,k,mq1,mq2,mq19,base)
 if k<=24:
  beam=finite_beam(n,d,c,k,mq18,mq2,mq17,width=24 if k<=12 else 12)
  beam=[(x*width+y)*4+r for x,y,r in beam]
  beam=refine(n,d,k,mq1,mq2,mq19,beam)
  beam_score=evaluate(beam)
  if beam_score>evaluate(base):
   base=beam
  if beam_score>evaluate(perturbed):
   perturbed=beam
 choices=[base]
 if perturbed!=base:
  choices.append(perturbed)
 mq6,best=(-1,None)
 for mq4 in choices:
  mq4=triple_refine(n,d,k,mq1,mq2,mq19,mq4)
  mq4=refine(n,d,k,mq1,mq2,mq19,mq4,passes=2)
  mq4=anneal_walk(n,d,k,mq1,mq2,mq19,mq4)
  mq4=refine(n,d,k,mq1,mq2,mq19,mq4,passes=2)
  score=evaluate(mq4)
  if score>mq6:
   mq6,best=(score,mq4)
 return[ops[aid]for aid in best]
def solve_before_pair_annealing(n,d,c,k,mq18,mq2,mq17):
 mq3=solve_retained_iterated(n,d,c,k,mq18,mq2,mq17)
 if n>6 or k<=24:
  return mq3
 mq10,_,ops,_,_=build(n,d,mq2)
 mq19=list(zip(mq10,ops))
 width=n-d+1
 def evaluate(mq8):
  final,buffer=(mq18[:],mq17[:])
  for x,y,r in mq8:
   transition(final,buffer,mq10[(x*width+y)*4+r])
  return sum((a==b for a,b in zip(final,mq2)))
 reference_score=evaluate(mq3)
 if reference_score==color_bound(mq18+mq17,mq2):
  return mq3
 mq4=finite_beam(n,d,c,min(k,60),mq18,mq2,mq17,width=96)
 mq0=[(x*width+y)*4+r for x,y,r in mq4]
 mq0=refine(n,d,k,mq18+mq17,mq2,mq19,mq0)
 mq0=anneal_walk(n,d,k,mq18+mq17,mq2,mq19,mq0)
 mq0=refine(n,d,k,mq18+mq17,mq2,mq19,mq0,passes=2)
 mq4=[mq19[aid][1]for aid in mq0]
 return mq4 if evaluate(mq4)>reference_score else mq3
class PairWalker:
 def __init__(mz,n,d,mq1,mq2,mq19,mq0,order):
  mz.mq0=mq0[:]
  mz.mq19=mq19
  mz.position=0
  mz.my=RefineState(n,d,mq1,mq2,mq19,order)
  final=mq1[:]
  for aid in mq0:
   if aid>=0:
    _st(final,n*n,mq19[aid][0])
  mz.score=sum((a==b for a,b in zip(final,mq2)))
  for aid in reversed(mq0[2:]):
   if aid>=0:
    mz.my.apply(aid,mu=True)
  mz.boundary_score=sum((x==y for x,y in zip(mz.my.mq18+mz.my.mq17,mz.my.mu+mz.my.wstamp)))
 def move(mz,position):
  if position>mz.position:
   steps=range(mz.position,position)
  else:
   steps=range(mz.position-1,position-1,-1)
  for i in steps:
   a,b=(mz.mq0[i],mz.mq0[i+2])
   if a>=0:
    mz.boundary_score+=_og(mz.my,a)
    mz.my.apply(a)
   if b>=0:
    mz.boundary_score+=_og(mz.my,b)
    mz.my.apply(b,mu=True)
  mz.position=position
 def propose(mz,fixed,side):
  my=mz.my
  old=mz.score-mz.boundary_score
  gain=_og(my,fixed)
  undo=refine_trial(my,fixed,mu=bool(side))
  other,extra=my.best()
  refine_restore(my,undo)
  pair=(other,fixed)if side else(fixed,other)
  return(pair,gain+extra-old)
 def accept(mz,pair,delta):
  mz.mq0[mz.position:mz.position+2]=pair
  mz.score+=delta
def anneal_walk(n,d,k,mq1,mq2,mq19,mq0,proposals=None):
 import math
 if k<3:
  return mq0
 limit=color_bound(mq1,mq2)
 final=mq1[:]
 for aid in mq0:
  if aid>=0:
   _st(final,n*n,mq19[aid][0])
 if sum((a==b for a,b in zip(final,mq2)))==limit:
  return[aid for aid in mq0 if aid>=0]
 rng=random.Random(sum(((i+23)*v for i,v in enumerate(mq1)))+k*1357+7751)
 order=list(range(len(mq19)))
 rng.shuffle(order)
 mq0=mq0+[-1]*(k-len(mq0))
 walker=PairWalker(n,d,mq1,mq2,mq19,mq0,order)
 if walker.score==limit:
  return[aid for aid in mq0 if aid>=0]
 if proposals is None:
  proposals=min(4000,max(300,900000//(n*n)))
 mq6,best=(walker.score,walker.mq0[:])
 period=max(1,proposals//4)
 position=rng.randrange(k-1)
 walker.move(position)
 direction=1
 size=n-d+1
 for step in range(proposals):
  if step and step%period==0:
   rng.shuffle(order)
   walker=PairWalker(n,d,mq1,mq2,mq19,best,order)
   position=rng.randrange(k-1)
   walker.move(position)
  side=step%2
  old=walker.mq0[position+side]
  mode=rng.randrange(5)
  if mode==0 and old>=0:
   x,y,r=mq19[old][1]
   x=min(size-1,max(0,x+rng.choice((-2,-1,0,0,1,2))))
   y=min(size-1,max(0,y+rng.choice((-2,-1,0,0,1,2))))
   fixed=(x*size+y)*4+rng.randrange(4)
  elif mode==1:
   fixed=walker.my.best()[0]
  elif mode==4:
   fixed=-1
  else:
   fixed=rng.randrange(len(mq19))
  pair,delta=walker.propose(fixed,side)
  temperature=0.4*(1-step%period/period)**2+0.04
  if delta>=0 or rng.random()<math.exp(delta/temperature):
   walker.accept(pair,delta)
   if walker.score>=mq6:
    mq6,best=(walker.score,walker.mq0[:])
    if mq6==limit:
     break
  if rng.randrange(16)==0:
   direction=-direction
  if not 0<=position+direction<k-1:
   direction=-direction
  position+=direction
  walker.move(position)
 return[aid for aid in best if aid>=0]
def solve_without_binary(n,d,c,k,mq18,mq2,mq17):
 mq8=solve_before_pair_annealing(n,d,c,k,mq18[:],mq2,mq17[:])
 if k<=2 or n<=16:
  return mq8
 mq10,_,ops,_,_=build(n,d,mq2)
 mq19=list(zip(mq10,ops))
 size=n-d+1
 mq0=[(x*size+y)*4+r for x,y,r in mq8]
 mq0=anneal_walk(n,d,k,mq18+mq17,mq2,mq19,mq0)
 mq0=refine(n,d,k,mq18+mq17,mq2,mq19,mq0,passes=2)
 return[mq19[aid][1]for aid in mq0]
def binary_transitions():
 mq12=[]
 for r in range(4):
  table=[]
  for value in range(512):
   result=0
   for u in range(3):
    for v in range(3):
     x,y=((u,v),(v,2-u),(2-u,2-v),(2-v,u))[r]
     result|=(value>>u*3+v&1)<<x*3+y
   table.append(result)
  mq12.append(table)
 patches=[]
 for x in range(2):
  for y in range(2):
   base=4*x+y
   scatter=[(v&7)<<base|(v&56)<<base+1|(v&448)<<base+2 for v in range(512)]
   paint=[[scatter[v]for v in mq12[r]]for r in range(4)]
   patches.append((base,65535^scatter[511],paint))
 def expand(my):
  board,mq17=(my&65535,my>>16)
  for position,(base,mask,paint)in enumerate(patches):
   patch=board>>base&7|board>>base+1&56|board>>base+2&448
   retained=board&mask
   for mq11 in range(4):
    child=retained|paint[mq11][mq17]|mq12[-mq11&3][patch]<<16
    yield(position*4+mq11,child)
 return expand
def binary_bfs(mq18,mq2,mq17,k):
 mq1=sum((v<<i for i,v in enumerate(mq18+mq17)))
 wanted=sum((v<<i for i,v in enumerate(mq2)))
 if mq1&65535==wanted:
  return[]
 required=mq1.bit_count()-wanted.bit_count()
 if not 0<=required<=9:
  return None
 expand=binary_transitions()
 forward={mq1:(None,None)}
 frontier=[mq1]
 first_depth=min(3,k)
 def prefix(my):
  path=[]
  while forward[my][0]is not None:
   my,action=forward[my]
   path.append(action)
  return path[::-1]
 for _ in range(first_depth):
  next_layer=[]
  for my in frontier:
   for action,child in expand(my):
    if child in forward:
     continue
    forward[child]=(my,action)
    if child&65535==wanted:
     return prefix(child)
    next_layer.append(child)
  frontier=next_layer
 goals=[wanted|v<<16 for v in range(512)if v.bit_count()==required]
 backward={my:(None,None)for my in goals}
 frontier=goals
 for _ in range(min(2,k-first_depth)):
  next_layer=[]
  for my in frontier:
   for action,child in expand(my):
    if child in backward:
     continue
    backward[child]=(my,action)
    if child in forward:
     answer=prefix(child)
     while backward[child][0]is not None:
      child,action=backward[child]
      answer.append(action)
     return answer
    next_layer.append(child)
  frontier=next_layer
 return None
def solve_weighted_parent(n,d,c,k,mq18,mq2,mq17):
 if n==4 and d==3 and(c==2):
  path=binary_bfs(mq18,mq2,mq17,k)
  if path is not None:
   return[(aid//8,aid//4%2,aid%4)for aid in path]
 return solve_without_binary(n,d,c,k,mq18,mq2,mq17)
class WeightedRefineState:
 def __init__(mz,n,d,mq1,mq2,weights,mq19,order):
  nn,dd=(n*n,d*d)
  mz.nn,mz.dd=(nn,dd)
  mz.mq18,mz.mq17=(mq1[:nn],mq1[nn:])
  mz.mu,mz.wstamp=(mq2[:],[6]*dd)
  mz.weights,mz.wstamp_weights=(weights[:],[0]*dd)
  mz.mq19,mz.order=(mq19,order)
  mz.all_bits=(1<<len(mq19))-1
  key=(n,d)
  geometry=_REFINE_GEOMETRY.get(key)
  if geometry is None:
   mq16=[[0]*nn for _ in range(dd)]
   region_bits=[15<<4*r for r in range(len(mq19)//4)]
   regions=[mq19[i][0]for i in range(0,len(mq19),4)]
   cover=[[]for _ in range(nn)]
   for region,patch in enumerate(regions):
    for p in patch:
     cover[p].append(region)
   for aid,(patch,_)in enumerate(mq19):
    bit=1<<aid
    for j,p in enumerate(patch):
     mq16[j][p]|=bit
   geometry=(mq16,region_bits,regions,cover)
   _REFINE_GEOMETRY[key]=geometry
  mz.mq16,mz.region_bits,mz.regions,mz.cover=geometry
  mz.values=[[0]*7 for _ in range(dd)]
  mz.goals=[[0]*7 for _ in range(dd)]
  mz.weight_bits=[[0]*3 for _ in range(dd)]
  for j in range(dd):
   values,goals,importance=(mz.values[j],mz.goals[j],mz.weight_bits[j])
   for p,mask in enumerate(mz.mq16[j]):
    values[mz.mq18[p]]|=mask
    goals[mz.mu[p]]|=mask
    importance[mz.weights[p]]|=mask
  mz.tie_masks=[0]*len(mq19).bit_length()
  for rank,aid in enumerate(order):
   bit=1<<aid
   while rank:
    low=rank&-rank
    mz.tie_masks[low.bit_length()-1]|=bit
    rank^=low
  mz.mv=[sum((mz.weights[p]*(mz.mq18[p]==mz.mu[p])for p in mq16))for mq16 in mz.regions]
  mz.old_planes=[0]*6
  for region,count in enumerate(mz.mv):
   value=2*dd-count
   for plane in range(5):
    if value&1<<plane:
     mz.old_planes[plane]|=mz.region_bits[region]
 def apply(mz,action,mu=False):
  changed={}
  mq16,cover,mv=(mz.mq16,mz.cover,mz.mv)
  if mu:
   mq18,mq17=(mz.mu,mz.wstamp)
   weights,stamp_weights=(mz.weights,mz.wstamp_weights)
   for j,p in enumerate(mz.mq19[action][0]):
    old,new=(mq18[p],mq17[j])
    old_weight,new_weight=(weights[p],stamp_weights[j])
    if old!=new:
     for ref in range(mz.dd):
      mask=mq16[ref][p]
      mz.goals[ref][old]^=mask
      mz.goals[ref][new]^=mask
    if old_weight!=new_weight:
     for ref in range(mz.dd):
      mask=mq16[ref][p]
      mz.weight_bits[ref][old_weight]^=mask
      mz.weight_bits[ref][new_weight]^=mask
    actual=mz.mq18[p]
    delta=new_weight*(actual==new)-old_weight*(actual==old)
    if delta:
     for region in cover[p]:
      changed[region]=changed.get(region,0)+delta
    mq17[j],mq18[p]=(old,new)
    stamp_weights[j],weights[p]=(old_weight,new_weight)
  else:
   mq18,mq17=(mz.mq18,mz.mq17)
   for j,p in enumerate(mz.mq19[action][0]):
    old,new=(mq18[p],mq17[j])
    if old==new:
     continue
    for ref in range(mz.dd):
     mask=mq16[ref][p]
     mz.values[ref][old]^=mask
     mz.values[ref][new]^=mask
    delta=mz.weights[p]*((new==mz.mu[p])-(old==mz.mu[p]))
    if delta:
     for region in cover[p]:
      changed[region]=changed.get(region,0)+delta
    mq17[j],mq18[p]=(old,new)
  for region,delta in changed.items():
   if not delta:
    continue
   mq15=mv[region]
   mv[region]+=delta
   change=2*mz.dd-mq15^2*mz.dd-mv[region]
   while change:
    bit=change&-change
    mz.old_planes[bit.bit_length()-1]^=mz.region_bits[region]
    change^=bit
 def best(mz):
  planes=[0]*6
  for j in range(mz.dd):
   match=mz.goals[j][mz.mq17[j]]
   parts=[(match&mz.weight_bits[j][1],0),(match&mz.weight_bits[j][2],1)]
   weight=mz.wstamp_weights[j]
   if weight:
    parts.append((mz.values[j][mz.wstamp[j]],weight-1))
   for carry,plane in parts:
    while carry:
     old=planes[plane]
     planes[plane]=old^carry
     carry&=old
     plane+=1
  carry=0
  for plane in range(6):
   a,b=(planes[plane],mz.old_planes[plane])
   different=a^b
   planes[plane]=different^carry
   carry=a&b|different&carry
  mq5,value=(mz.all_bits,0)
  for plane in range(5,-1,-1):
   hits=mq5&planes[plane]
   if hits:
    mq5=hits
    value|=1<<plane
  stamp_loss=sum((w*(a==b)for w,a,b in zip(mz.wstamp_weights,mz.mq17,mz.wstamp)))
  gain=value-2*mz.dd-stamp_loss
  if gain<0:
   return(-1,0)
  for mask in reversed(mz.tie_masks):
   if not mq5&mq5-1:
    break
   preferred=mq5&~mask
   if preferred:
    mq5=preferred
  return((mq5&-mq5).bit_length()-1,gain)
def weighted_refine(n,d,k,mq1,mq2,weights,mq19,mq0,passes=1):
 nn,dd=(n*n,d*d)
 seed=sum(((i+1)*v for i,v in enumerate(mq1)))+k*131
 seed+=sum(((i+7)*weight for i,weight in enumerate(weights)))*17
 rng=random.Random(seed)
 for iteration in range(passes):
  mq0=mq0+[-1]*min(8,k-len(mq0))
  final=mq1[:]
  for action in mq0:
   if action>=0:
    _st(final,nn,mq19[action][0])
  if all((a==b for a,b in zip(final,mq2))):
   return[action for action in mq0 if action>=0]
  order=list(range(len(mq19)))
  rng.shuffle(order)
  my=WeightedRefineState(n,d,final,mq2,weights,mq19,order)
  for i in range(len(mq0)-1,-1,-1):
   old=mq0[i]
   if old>=0:
    my.apply(old)
   chosen,_=my.best()
   mq0[i]=chosen
   if chosen>=0:
    my.apply(chosen,mu=True)
  mq0=[action for action in mq0 if action>=0]
 return mq0
def solve_before_triple_walking(n,d,c,k,mq18,mq2,mq17):
 mq3=solve_weighted_parent(n,d,c,k,mq18[:],mq2,mq17[:])
 if k<=2:
  return mq3
 nn,dd=(n*n,d*d)
 mq10,_,ops,_,_=build(n,d,mq2)
 mq19=list(zip(mq10,ops))
 side=n-d+1
 mq0=[(x*side+y)*4+r for x,y,r in mq3]
 mq1,final=(mq18+mq17,mq18+mq17)
 for aid in mq0:
  _st(final,nn,mq10[aid])
 mq6=sum((a==b for a,b in zip(final,mq2)))
 _bs=mq0
 supply,wanted=([0]*c,[0]*c)
 for color in mq1:
  supply[color]+=1
 for color in mq2:
  wanted[color]+=1
 upper=sum((min(a,b)for a,b in zip(supply,wanted)))
 if mq6==upper:
  return mq3
 coverage=[min(p,n-d)-max(0,p-d+1)+1 for p in range(n)]
 maximum=max(coverage)**2
 boundary=[1+(coverage[row]*coverage[col]<maximum)for row in range(n)for col in range(n)]
 unresolved=[1+(a!=b)for a,b in zip(final,mq2)]
 seen_weights=set()
 for weights in(unresolved,boundary):
  signature=tuple(weights)
  if min(weights)==max(weights)or signature in seen_weights:
   continue
  seen_weights.add(signature)
  mq4=weighted_refine(n,d,k,mq1,mq2,weights,mq19,mq0)
  mq4=refine(n,d,k,mq1,mq2,mq19,mq4,passes=2)
  final=mq1[:]
  for aid in mq4:
   _st(final,nn,mq10[aid])
  score=sum((a==b for a,b in zip(final,mq2)))
  if score>mq6:
   mq6,_bs=(score,mq4)
   if score==upper:
    break
 return[ops[aid]for aid in _bs]
class TripleWalker:
 def __init__(mz,n,d,mq1,mq2,mq19,mq0,order):
  mz.mq0=mq0[:]
  mz.mq19=mq19
  mz.position=0
  mz.my=RefineState(n,d,mq1,mq2,mq19,order)
  final=mq1[:]
  for aid in mq0:
   if aid>=0:
    _st(final,n*n,mq19[aid][0])
  mz.score=sum((a==b for a,b in zip(final,mq2)))
  for aid in reversed(mq0[3:]):
   if aid>=0:
    mz.my.apply(aid,mu=True)
  mz.boundary_score=sum((x==y for x,y in zip(mz.my.mq18+mz.my.mq17,mz.my.mu+mz.my.wstamp)))
 def move(mz,position):
  if position>mz.position:
   steps=range(mz.position,position)
  else:
   steps=range(mz.position-1,position-1,-1)
  for i in steps:
   a,b=(mz.mq0[i],mz.mq0[i+3])
   if a>=0:
    mz.boundary_score+=_og(mz.my,a)
    mz.my.apply(a)
   if b>=0:
    mz.boundary_score+=_og(mz.my,b)
    mz.my.apply(b,mu=True)
  mz.position=position
 def informed(mz,side):
  my=mz.my
  opposite=mz.mq0[mz.position if side else mz.position+2]
  mu=not bool(side)
  undo=refine_trial(my,opposite,mu=mu)
  fixed,_=my.best()
  refine_restore(my,undo)
  return fixed
 def propose(mz,first,last):
  my=mz.my
  old=mz.score-mz.boundary_score
  gain=_og(my,first)
  outer=refine_trial(my,first)
  gain+=_og(my,last)
  inner=refine_trial(my,last,mu=True)
  middle,extra=my.best()
  refine_restore(my,inner)
  refine_restore(my,outer)
  return((first,middle,last),gain+extra-old)
 def accept(mz,triple,delta):
  mz.mq0[mz.position:mz.position+3]=triple
  mz.score+=delta
def anneal_triples(n,d,k,mq1,mq2,mq19,mq0,proposals=None):
 import math
 if k<3:
  return mq0
 limit=color_bound(mq1,mq2)
 final=mq1[:]
 for aid in mq0:
  if aid>=0:
   _st(final,n*n,mq19[aid][0])
 if sum((a==b for a,b in zip(final,mq2)))==limit:
  return[aid for aid in mq0 if aid>=0]
 rng=random.Random(sum(((i+31)*v for i,v in enumerate(mq1)))+k*1123+19271)
 order=list(range(len(mq19)))
 rng.shuffle(order)
 mq0=mq0+[-1]*(k-len(mq0))
 walker=TripleWalker(n,d,mq1,mq2,mq19,mq0,order)
 if proposals is None:
  proposals=min(6000,max(600,1350000//(n*n)))
 mq6,best=(walker.score,walker.mq0[:])
 period=max(1,proposals//3)
 position=rng.randrange(k-2)
 walker.move(position)
 direction=1
 size=n-d+1
 for step in range(proposals):
  if step and step%period==0:
   rng.shuffle(order)
   walker=TripleWalker(n,d,mq1,mq2,mq19,best,order)
   position=rng.randrange(k-2)
   walker.move(position)
  first,last=(walker.mq0[position],walker.mq0[position+2])
  side=step%2
  old=last if side else first
  mode=rng.randrange(5)
  if mode==0 and old>=0:
   x,y,r=mq19[old][1]
   x=min(size-1,max(0,x+rng.choice((-2,-1,0,0,1,2))))
   y=min(size-1,max(0,y+rng.choice((-2,-1,0,0,1,2))))
   fixed=(x*size+y)*4+rng.randrange(4)
  elif mode==1:
   fixed=walker.informed(side)
  elif mode==4:
   fixed=-1
  else:
   fixed=rng.randrange(len(mq19))
  if side:
   last=fixed
  else:
   first=fixed
  triple,delta=walker.propose(first,last)
  temperature=0.4*(1-step%period/period)**2+0.04
  if delta>=0 or rng.random()<math.exp(delta/temperature):
   walker.accept(triple,delta)
   if walker.score>=mq6:
    mq6,best=(walker.score,walker.mq0[:])
    if mq6==limit:
     break
  if k>3:
   if rng.randrange(16)==0:
    direction=-direction
   if not 0<=position+direction<k-2:
    direction=-direction
   position+=direction
   walker.move(position)
 return[aid for aid in best if aid>=0]
def solve_without_wildcard(n,d,c,k,mq18,mq2,mq17):
 mq8=solve_before_triple_walking(n,d,c,k,mq18[:],mq2,mq17[:])
 if k<=2:
  return mq8
 mq10,_,ops,_,_=build(n,d,mq2)
 mq19=list(zip(mq10,ops))
 size=n-d+1
 mq0=[(x*size+y)*4+r for x,y,r in mq8]
 mq0=anneal_triples(n,d,k,mq18+mq17,mq2,mq19,mq0)
 mq0=refine(n,d,k,mq18+mq17,mq2,mq19,mq0,passes=2)
 return[mq19[aid][1]for aid in mq0]
def packed_transitions():
 mq12=[]
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
  mq12.append(rows)
 board_mask=(1<<48)-1
 patches=[]
 for x in range(2):
  for y in range(2):
   shift=3*(4*x+y)
   mask=board_mask^(511|511<<12|511<<24)<<shift
   patches.append((shift,mask))
 def rotate(value,r):
  tables=mq12[r]
  return tables[0][value&511]|tables[1][value>>9&511]|tables[2][value>>18]
 def expand(my):
  board,mq17=(my&board_mask,my>>48)
  rotated=[rotate(mq17,r)for r in range(4)]
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
  for my in frontier:
   path=backward[my]
   for aid,child in expand(my):
    if child in backward:
     continue
    new_path=path+bytes((aid,))
    backward[child]=new_path
    next_layer.append(child)
    mu=child
    constraints=bytearray()
    for position in range(25):
     color=mu&7
     mu>>=3
     if color!=7:
      constraints.append(position*6+color)
    yield(depth,new_path,bytes(constraints))
  frontier=next_layer
def wildcard_finish(mq18,mq2,mq17,k,depth=8):
 global _PACKED_EXPAND,_WILDCARD_BACKWARD
 if mq18==mq2:
  return[]
 if color_bound(mq18+mq17,mq2)<16:
  return None
 if _PACKED_EXPAND is None:
  _PACKED_EXPAND=packed_transitions()
 expand=_PACKED_EXPAND
 mq1=sum((v<<3*i for i,v in enumerate(mq18+mq17)))
 wanted=sum((v<<3*i for i,v in enumerate(mq2)))
 board_mask=(1<<48)-1
 forward={mq1:b''}
 frontier=[mq1]
 forward_depth=min(4,k,depth)
 for _ in range(forward_depth):
  next_layer=[]
  for my in frontier:
   path=forward[my]
   for aid,child in expand(my):
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
 for index,my in enumerate(states):
  offset,bit=(index>>3,1<<(index&7))
  for row in buffers:
   row[my&7][offset]|=bit
   my>>=3
 indexes=[int.from_bytes(buf,'little')for row in buffers for buf in row]
 mv=[bits.bit_count()for bits in indexes]
 counts_get=mv.__getitem__
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
def solve_without_suffix_finish(n,d,c,k,mq18,mq2,mq17):
 mq3=solve_without_wildcard(n,d,c,k,mq18,mq2,mq17)
 if n!=4 or d!=3 or len(mq3)>=k:
  return mq3
 mq10,_,ops,_,_=build(n,d,mq2)
 board,buffer=(mq18[:],mq17[:])
 for x,y,r in mq3:
  transition(board,buffer,mq10[(x*2+y)*4+r])
 tail=wildcard_finish(board,mq2,buffer,k-len(mq3))
 return mq3+[ops[aid]for aid in tail]if tail is not None else mq3
def solve_forward_parent(n,d,c,k,mq18,mq2,mq17):
 mq3=solve_without_suffix_finish(n,d,c,k,mq18,mq2,mq17)
 if n!=4 or d!=3 or k<6 or(color_bound(mq18+mq17,mq2)<16):
  return mq3
 mq10,_,ops,_,_=build(n,d,mq2)
 board,buffer=(mq18[:],mq17[:])
 for x,y,r in mq3:
  transition(board,buffer,mq10[(x*2+y)*4+r])
 if board==mq2:
  return mq3
 tried=set()
 for remove in(2,4,8,12):
  length=max(0,len(mq3)-remove)
  if length in tried:
   continue
  tried.add(length)
  board,buffer=(mq18[:],mq17[:])
  for x,y,r in mq3[:length]:
   transition(board,buffer,mq10[(x*2+y)*4+r])
  tail=wildcard_finish(board,mq2,buffer,k-length)
  if tail is not None:
   return mq3[:length]+[ops[aid]for aid in tail]
 return mq3
def forward_sweep(n,d,mq1,mq2,mq19,mq0,order):
 nn=n*n
 mu=mq2+[6]*(d*d)
 for old in reversed(mq0):
  if old>=0:
   _st(mu,nn,mq19[old][0])
 my=RefineState(n,d,mq1,mu[:nn],mq19,order)
 my.wstamp=mu[nn:]
 result=mq0[:]
 for i,old in enumerate(mq0):
  if old>=0:
   my.apply(old,mu=True)
  chosen,_=my.best()
  result[i]=chosen
  if chosen>=0:
   my.apply(chosen)
 return result
def forward_refine(n,d,k,mq1,mq2,mq19,mq0,passes=1,seed_offset=0):
 nn=n*n
 limit=color_bound(mq1,mq2)
 seed=sum(((i+1)*v for i,v in enumerate(mq1)))+k*131+1000003+seed_offset
 rng=random.Random(seed)
 mq0=[aid for aid in mq0 if aid>=0]
 for iteration in range(passes):
  final=mq1[:]
  for aid in mq0:
   _st(final,nn,mq19[aid][0])
  if sum((a==b for a,b in zip(final,mq2)))==limit:
   return mq0
  padded=mq0+[-1]*min(8,k-len(mq0))
  order=list(range(len(mq19)))
  rng.shuffle(order)
  mq0=forward_sweep(n,d,mq1,mq2,mq19,padded,order)
  mq0=[aid for aid in mq0 if aid>=0]
 return mq0
def solve_without_late_beam(n,d,c,k,mq18,mq2,mq17):
 mq3=solve_forward_parent(n,d,c,k,mq18[:],mq2,mq17[:])
 if k<=2:
  return mq3
 nn=n*n
 mq1=mq18+mq17
 mq10,_,ops,_,_=build(n,d,mq2)
 mq19=list(zip(mq10,ops))
 side=n-d+1
 mq4=[(x*side+y)*4+r for x,y,r in mq3]
 final=mq1[:]
 for aid in mq4:
  _st(final,nn,mq10[aid])
 mq6=sum((a==b for a,b in zip(final,mq2)))
 limit=color_bound(mq1,mq2)
 if mq6==limit:
  return mq3
 _bs=mq4
 for iteration in range(2):
  mq4=forward_refine(n,d,k,mq1,mq2,mq19,mq4,seed_offset=iteration*104729)
  mq4=refine(n,d,k,mq1,mq2,mq19,mq4,passes=1,seed_offset=3301+iteration*7919)
  final=mq1[:]
  for aid in mq4:
   _st(final,nn,mq10[aid])
  score=sum((a==b for a,b in zip(final,mq2)))
  if score>mq6:
   mq6,_bs=(score,mq4)
   if score==limit:
    break
 return[ops[aid]for aid in _bs]
def packed3_transitions(n):
 mq12=[]
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
  mq12.append(tables)
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
  tables=mq12[r]
  return tables[0][value&511]|tables[1][value>>9&511]|tables[2][value>>18]
 def expand(my):
  board,mq17=(my&board_mask,my>>shift_stamp)
  rotated=[rotate(mq17,r)for r in range(4)]
  scatter=[v&511|(v>>9&511)<<stride|v>>18<<2*stride for v in rotated]
  for p,(shift,mask)in enumerate(patches):
   shifted=board>>shift
   patch=shifted&511|(shifted>>stride&511)<<9|(shifted>>2*stride&511)<<18
   retained=board&mask
   for r in range(4):
    yield(4*p+r,retained|scatter[r]<<shift|rotate(patch,-r&3)<<shift_stamp)
 return expand
def late_beam_finish(n,mq18,mq2,mq17,k):
 if k<=0:
  return None
 nn=n*n
 _is=sum((a==b for a,b in zip(mq18,mq2)))
 if _is==color_bound(mq18+mq17,mq2):
  return None
 expand=packed3_transitions(n)
 mq1=sum((v<<3*i for i,v in enumerate(mq18+mq17)))
 wanted=sum((v<<3*i for i,v in enumerate(mq2)))
 comparison_mask=sum((1<<3*i for i in range(nn)))
 rng=random.Random(mq1+k*997)
 import heapq
 frontier=[(mq1,b'')]
 visited={mq1}
 for depth in range(min(6,k)):
  mq5={}
  for my,path in frontier:
   for aid,child in expand(my):
    if child in visited or child in mq5:
     continue
    new_path=path+bytes((aid,))
    diff=child^wanted
    score=nn-((diff|diff>>1|diff>>2)&comparison_mask).bit_count()
    if score>_is:
     return list(new_path)
    mq5[child]=(score,rng.getrandbits(32),new_path)
  if not mq5:
   break
  mq13=heapq.nlargest(256,mq5,key=mq5.get)
  frontier=[(my,mq5[my][2])for my in mq13]
  visited.update(mq13)
 return None
def solve_without_hot_restart(n,d,c,k,mq18,mq2,mq17):
 mq3=solve_without_late_beam(n,d,c,k,mq18,mq2,mq17)
 if 5<=n<=9 and d==3:
  early=runtime_early_bound(n,d,k,mq18,mq2,mq17,mq3)
  if early is not None:
   return early
 if not 5<=n<=9 or d!=3 or len(mq3)>=k:
  return mq3
 mq10,_,ops,_,_=build(n,d,mq2)
 board,buffer=(mq18[:],mq17[:])
 width=n-d+1
 for x,y,r in mq3:
  transition(board,buffer,mq10[(x*width+y)*4+r])
 missing=sum((a!=b for a,b in zip(board,mq2)))
 if not 1<=missing<=8:
  return mq3
 mq4=mq3[:]
 for _ in range(4):
  tail=late_beam_finish(n,board,mq2,buffer,k-len(mq4))
  if tail is None:
   break
  for aid in tail:
   transition(board,buffer,mq10[aid])
   mq4.append(ops[aid])
 return mq4
def anneal_hot_triples(n,d,k,mq1,mq2,mq19,mq0,proposals=None):
 import math
 if k<3:
  return mq0
 limit=color_bound(mq1,mq2)
 final=mq1[:]
 for aid in mq0:
  if aid>=0:
   _st(final,n*n,mq19[aid][0])
 if sum((a==b for a,b in zip(final,mq2)))==limit:
  return[aid for aid in mq0 if aid>=0]
 rng=random.Random(sum(((i+67)*v for i,v in enumerate(mq1)))+k*1559+925713)
 order=list(range(len(mq19)))
 rng.shuffle(order)
 mq0=mq0+[-1]*(k-len(mq0))
 walker=TripleWalker(n,d,mq1,mq2,mq19,mq0,order)
 if proposals is None:
  proposals=min(3000,max(300,675000//(n*n)))
 mq6,best=(walker.score,walker.mq0[:])
 period=max(1,proposals//3)
 position=rng.randrange(k-2)
 walker.move(position)
 direction=1
 size=n-d+1
 for step in range(proposals):
  if step and step%period==0:
   rng.shuffle(order)
   walker=TripleWalker(n,d,mq1,mq2,mq19,best,order)
   position=rng.randrange(k-2)
   walker.move(position)
  first,last=(walker.mq0[position],walker.mq0[position+2])
  side=step%2
  old=last if side else first
  mode=rng.randrange(5)
  if mode==0 and old>=0:
   x,y,r=mq19[old][1]
   x=min(size-1,max(0,x+rng.choice((-2,-1,0,0,1,2))))
   y=min(size-1,max(0,y+rng.choice((-2,-1,0,0,1,2))))
   fixed=(x*size+y)*4+rng.randrange(4)
  elif mode==1:
   fixed=walker.informed(side)
  elif mode==4:
   fixed=-1
  else:
   fixed=rng.randrange(len(mq19))
  if side:
   last=fixed
  else:
   first=fixed
  triple,delta=walker.propose(first,last)
  temperature=0.86*(1-step%period/period)**2+0.04
  if delta>=0 or rng.random()<math.exp(delta/temperature):
   walker.accept(triple,delta)
   if walker.score>=mq6:
    mq6,best=(walker.score,walker.mq0[:])
    if mq6==limit:
     break
  if k>3:
   if rng.randrange(16)==0:
    direction=-direction
   if not 0<=position+direction<k-2:
    direction=-direction
   position+=direction
   walker.move(position)
 return[aid for aid in best if aid>=0]
def hot_triple_repair(n,d,k,mq1,mq2,mq19,mq0,proposals=None):
 if k<3:
  return mq0
 final=mq1[:]
 for aid in mq0:
  if aid>=0:
   _st(final,n*n,mq19[aid][0])
 parent_score=sum((a==b for a,b in zip(final,mq2)))
 if parent_score==color_bound(mq1,mq2):
  return mq0
 mq4=anneal_hot_triples(n,d,k,mq1,mq2,mq19,mq0,proposals)
 mq4=refine(n,d,k,mq1,mq2,mq19,mq4,passes=2)
 final=mq1[:]
 for aid in mq4:
  if aid>=0:
   _st(final,n*n,mq19[aid][0])
 if sum((a==b for a,b in zip(final,mq2)))>parent_score:
  return mq4
 return mq0
def solve_without_commutator(n,d,c,k,mq18,mq2,mq17):
 mq3=solve_without_hot_restart(n,d,c,k,mq18[:],mq2,mq17[:])
 if k<3:
  return mq3
 mq10,_,ops,_,_=build(n,d,mq2)
 mq19=list(zip(mq10,ops))
 width=n-d+1
 mq0=[(x*width+y)*4+r for x,y,r in mq3]
 found=hot_triple_repair(n,d,k,mq18+mq17,mq2,mq19,mq0)
 if found==mq0:
  return mq3
 return[ops[aid]for aid in found if aid>=0]
def commutator_word_gain(mq18,mq2,mq17,mq10,word,touched):
 before=sum((mq18[p]==mq2[p]for p in touched))
 for aid in word:
  transition(mq18,mq17,mq10[aid])
 after=sum((mq18[p]==mq2[p]for p in touched))
 for aid in reversed(word):
  transition(mq18,mq17,mq10[aid])
 return after-before
def commutator_tail(n,d,mq18,mq2,mq17,mq10,seed,pair_limit=20000):
 if pair_limit<=0:
  return None
 width=n-d+1
 missing=[p for p in range(n*n)if mq18[p]!=mq2[p]]
 if not missing:
  return None
 mq1=n*n-len(missing)
 possible=color_bound(mq18+mq17,mq2)-mq1
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
 mw=0
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
    touched=tuple(sorted(set(mq10[first])|set(mq10[second])))
    touched_cache[regions]=touched
   for left,right in((first,second),(second,first)):
    word=(left,right,left,right)
    gain=commutator_word_gain(mq18,mq2,mq17,mq10,word,touched)
    if gain>mw:
     mw,best_word=(gain,word)
     if mw==possible:
      return best_word
 return best_word
def solve_four_parent(n,d,c,k,mq18,mq2,mq17):
 mq3=solve_without_commutator(n,d,c,k,mq18,mq2,mq17)
 if n>16 or k-len(mq3)<4:
  return mq3
 mq10,_,mq8,_,_=build(n,d,mq2)
 width=n-d+1
 board,buffer=(mq18[:],mq17[:])
 for x,y,r in mq3:
  transition(board,buffer,mq10[(x*width+y)*4+r])
 matches=sum((a==b for a,b in zip(board,mq2)))
 if not 1<=n*n-matches<=12 or matches>=color_bound(mq18+mq17,mq2):
  return mq3
 seed=sum(((i+41)*v for i,v in enumerate(mq18+mq2+mq17)))+n*1009+d*9176+k*131
 word=commutator_tail(n,d,board,mq2,buffer,mq10,seed)
 if word is None:
  return mq3
 return mq3+[mq8[aid]for aid in word]
class FourWindowWalker:
 def __init__(mz,n,d,mq1,mq2,mq19,mq0,order):
  mz.mq0=mq0[:]
  mz.mq19=mq19
  mz.position=0
  nn=n*n
  final=mq1[:]
  for aid in mq0:
   if aid>=0:
    _st(final,nn,mq19[aid][0])
  mz.score=sum((a==b for a,b in zip(final,mq2)))
  mu=mq2+[6]*(d*d)
  for aid in reversed(mq0[4:]):
   if aid>=0:
    _st(mu,nn,mq19[aid][0])
  mz.my=RefineState(n,d,mq1,mu[:nn],mq19,order)
  mz.my.wstamp=mu[nn:]
  mz.boundary_score=sum((a==b for a,b in zip(mq1,mu)))
 def move(mz,position):
  if position>mz.position:
   steps=range(mz.position,position)
  else:
   steps=range(mz.position-1,position-1,-1)
  for i in steps:
   a,b=(mz.mq0[i],mz.mq0[i+4])
   if a>=0:
    mz.boundary_score+=_og(mz.my,a)
    mz.my.apply(a)
   if b>=0:
    mz.boundary_score+=_og(mz.my,b)
    mz.my.apply(b,mu=True)
  mz.position=position
 def propose(mz,first,last,mq5):
  my=mz.my
  old=mz.score-mz.boundary_score
  gain=_og(my,first)
  outer=refine_trial(my,first)
  gain+=_og(my,last)
  inner=refine_trial(my,last,mu=True)
  second,third=optimize_pair(my,mz.mq0[mz.position+1],mz.mq0[mz.position+2],mq5)
  gain+=_og(my,second)
  middle=refine_trial(my,second)
  gain+=_og(my,third)
  refine_restore(my,middle)
  refine_restore(my,inner)
  refine_restore(my,outer)
  return((first,second,third,last),gain-old)
 def accept(mz,window,delta):
  mz.mq0[mz.position:mz.position+4]=window
  mz.score+=delta
def repair_four_windows(n,d,k,mq1,mq2,mq19,mq0,proposals=None):
 import math
 if k<4:
  return mq0
 padded=mq0+[-1]*min(8,k-len(mq0))
 rng=random.Random(sum(((i+43)*v for i,v in enumerate(mq1)))+k*1733+74821)
 order=list(range(len(mq19)))
 rng.shuffle(order)
 walker=FourWindowWalker(n,d,mq1,mq2,mq19,padded,order)
 limit=color_bound(mq1,mq2)
 if walker.score==limit:
  return mq0
 if proposals is None:
  proposals=min(1800,max(120,180000//(n*n)))
 mq6,best=(walker.score,walker.mq0[:])
 size=n-d+1
 length=len(padded)
 position=rng.randrange(length-3)
 walker.move(position)
 direction=1
 for step in range(proposals):
  first,last=(walker.mq0[position],walker.mq0[position+3])
  side=step%2
  old=last if side else first
  mode=rng.randrange(5)
  if mode==0 and old>=0:
   x,y,r=mq19[old][1]
   x=min(size-1,max(0,x+rng.choice((-1,0,1))))
   y=min(size-1,max(0,y+rng.choice((-1,0,1))))
   fixed=(x*size+y)*4+rng.randrange(4)
  elif mode==1:
   my=walker.my
   p=rng.randrange(n*n)
   for _ in range(10):
    p=rng.randrange(n*n)
    if my.mu[p]<6 and my.mq18[p]!=my.mu[p]:
     break
   x=min(size-1,max(0,p//n-rng.randrange(d)))
   y=min(size-1,max(0,p%n-rng.randrange(d)))
   fixed=(x*size+y)*4+rng.randrange(4)
  elif mode==4:
   fixed=-1
  else:
   fixed=rng.randrange(len(mq19))
  if side:
   last=fixed
  else:
   first=fixed
  if step%11==10:
   if side:
    first=rng.randrange(len(mq19))
   else:
    last=rng.randrange(len(mq19))
  mq5=[(walker.mq0[position+1],0),(walker.mq0[position+2],1),(-1,0),(-1,1),(rng.randrange(len(mq19)),rng.randrange(2))]
  window,delta=walker.propose(first,last,mq5)
  temperature=0.04+0.76*(1-step/max(1,proposals-1))**2
  if delta>=0 or rng.random()<math.exp(delta/temperature):
   walker.accept(window,delta)
   if walker.score>=mq6:
    mq6,best=(walker.score,walker.mq0[:])
    if mq6==limit:
     break
  if length>4:
   if rng.randrange(16)==0:
    direction=-direction
   if not 0<=position+direction<length-3:
    direction=-direction
   position+=direction
   walker.move(position)
 return[aid for aid in best if aid>=0]
def solve_without_deeper_beam(n,d,c,k,mq18,mq2,mq17):
 mq3=solve_four_parent(n,d,c,k,mq18[:],mq2,mq17[:])
 if k<4:
  return mq3
 nn=n*n
 mq1=mq18+mq17
 mq10,_,ops,_,_=build(n,d,mq2)
 mq19=list(zip(mq10,ops))
 width=n-d+1
 mq0=[(x*width+y)*4+r for x,y,r in mq3]
 final=mq1[:]
 for aid in mq0:
  _st(final,nn,mq10[aid])
 baseline=sum((a==b for a,b in zip(final,mq2)))
 if baseline==color_bound(mq1,mq2):
  return mq3
 mq4=repair_four_windows(n,d,k,mq1,mq2,mq19,mq0)
 if mq4==mq0:
  return mq3
 mq4=refine(n,d,k,mq1,mq2,mq19,mq4,passes=1,seed_offset=2947)
 final=mq1[:]
 for aid in mq4:
  _st(final,nn,mq10[aid])
 if sum((a==b for a,b in zip(final,mq2)))<=baseline:
  return mq3
 return[ops[aid]for aid in mq4]
def deeper_beam_finish(n,mq18,mq2,mq17,k):
 if k<=0:
  return None
 nn=n*n
 _is=sum((a==b for a,b in zip(mq18,mq2)))
 if _is==color_bound(mq18+mq17,mq2):
  return None
 expand=packed3_transitions(n)
 mq1=sum((v<<3*i for i,v in enumerate(mq18+mq17)))
 wanted=sum((v<<3*i for i,v in enumerate(mq2)))
 comparison_mask=sum((1<<3*i for i in range(nn)))
 rng=random.Random(mq1+k*997)
 import heapq
 frontier=[(mq1,b'')]
 visited={mq1}
 for depth in range(min(8,k)):
  mq5={}
  for my,path in frontier:
   for aid,child in expand(my):
    if child in visited or child in mq5:
     continue
    new_path=path+bytes((aid,))
    diff=child^wanted
    score=nn-((diff|diff>>1|diff>>2)&comparison_mask).bit_count()
    if score>_is:
     return list(new_path)
    mq5[child]=(score,rng.getrandbits(32),new_path)
  if not mq5:
   break
  mq13=heapq.nlargest(512,mq5,key=mq5.get)
  frontier=[(my,mq5[my][2])for my in mq13]
  visited.update(mq13)
 return None
def solve_route_parent(n,d,c,k,mq18,mq2,mq17):
 mq3=solve_without_deeper_beam(n,d,c,k,mq18,mq2,mq17)
 if not 5<=n<=9 or d!=3 or k-len(mq3)<3:
  return mq3
 mq10,_,ops,_,_=build(n,d,mq2)
 board,buffer=(mq18[:],mq17[:])
 width=n-d+1
 for x,y,r in mq3:
  transition(board,buffer,mq10[(x*width+y)*4+r])
 missing=sum((a!=b for a,b in zip(board,mq2)))
 if not 1<=missing<=8:
  return mq3
 tail=deeper_beam_finish(n,board,mq2,buffer,k-len(mq3))
 if tail is None:
  return mq3
 for aid in tail:
  transition(board,buffer,mq10[aid])
 if sum((a==b for a,b in zip(board,mq2)))<=n*n-missing:
  return mq3
 return mq3+[ops[aid]for aid in tail]
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
     mq1={p:p for p in cells}
     mq1.update({j:j for j in range(d*d)})
     for backward in range(2):
      a,b=(right,left)if backward else(left,right)
      my=mq1.copy()
      for count in range(1,max(repeats)+1):
       for patch in(a,b):
        for j,p in enumerate(patch):
         my[j],my[p]=(my[p],my[j])
       if count not in repeats:
        continue
       mapping=[]
       for p in sorted(cells):
        q=my[p]
        if q==p:
         continue
        src=n*n+q if isinstance(q,int)else q[0]*n+q[1]
        mapping.append((p[0]*n+p[1],src,isinstance(q,int)))
       if mapping:
        patterns.append((dx,dy,r,s,backward,count,mapping))
 return patterns
def route_tail(n,d,mq18,mq2,mq17,k,repeats=(3,),rounds=3):
 if k<6:
  return[]
 active=tuple((x for x in repeats if 2*x<=k))
 if not active:
  return[]
 patterns=route_patterns(n,d,active)
 width=n-d+1
 my=mq18+mq17
 wanted=[0]*6
 for p,color in enumerate(mq2):
  wanted[color]|=1<<p
 def shift(bits,offset):
  return bits>>offset if offset>=0 else bits<<-offset
 offsets={p for*_,mapping in patterns for p,_,_ in mapping}
 sources={q for*_,mapping in patterns for _,q,buffer in mapping if not buffer}
 mu={p:tuple((shift(bits,p)for bits in wanted))for p in offsets}
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
 mq12=[[p*n+q for u in range(d)for v in range(d)for p,q in[((u,v),(v,d-1-u),(d-1-u,d-1-v),(d-1-v,u))[r]]]for r in range(4)]
 answer=[]
 for _ in range(rounds):
  have=[0]*6
  agreement=0
  for p,color in enumerate(my[:n*n]):
   have[color]|=1<<p
   if color==mq2[p]:
    agreement|=1<<p
  if agreement==(1<<n*n)-1:
   break
  values={q:tuple((shift(bits,q)for bits in have))for q in sources}
  old={p:shift(agreement,p)for p in offsets}
  matches={}
  mw=0
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
     new=mu[p][my[q]]
    else:
     key=(p,q)
     new=matches.get(key)
     if new is None:
      new=0
      for want,value in zip(mu[p],values[q]):
       new|=want&value
      matches[key]=new
    for carry in(new&anchors,anchors&~old[p]):
     level=0
     while carry:
      before=planes[level]
      planes[level]=before^carry
      carry&=before
      level+=1
   mq5,value=(anchors,0)
   for level in range(len(planes)-1,-1,-1):
    hits=mq5&planes[level]
    if hits:
     mq5=hits
     value|=1<<level
   gain=value-len(mapping)
   if gain>mw:
    mw=gain
    base=(mq5&-mq5).bit_length()-1
    x,y=divmod(base,n)
    left,right=((x,y,r),(x+dx,y+dy,s))
    best=([right,left]if backward else[left,right])*count
  if best is None:
   break
  answer.extend(best)
  for x,y,r in best:
   base=x*n+y
   for j,offset in enumerate(mq12[r]):
    p=base+offset
    my[n*n+j],my[p]=(my[p],my[n*n+j])
 return answer
def cancel_inverse_pairs(mq0):
 compact=[]
 for aid in mq0:
  if compact and compact[-1]==aid:
   compact.pop()
  else:
   compact.append(aid)
 return compact
def best_insertion(n,d,mq1,mq2,mq19,mq0,seed=0):
 final=mq1[:]
 for aid in mq0:
  _st(final,n*n,mq19[aid][0])
 order=list(range(len(mq19)))
 random.Random(seed).shuffle(order)
 my=RefineState(n,d,final,mq2,mq19,[])
 ranks=[0]*len(mq19)
 for rank,aid in enumerate(order):
  ranks[aid]=rank
 best=(0,-1,-1)
 for pos in range(len(mq0),-1,-1):
  aid,gain=temporal_best(my,ranks,best[0])
  if gain>best[0]:
   best=(gain,pos,aid)
  if pos:
   old=mq0[pos-1]
   temporal_boundary(my,old)
 return best
def deletion_deltas(n,d,mq1,mq2,mq19,mq0):
 final=mq1[:]
 for aid in mq0:
  _st(final,n*n,mq19[aid][0])
 my=RefineState(n,d,final,mq2,mq19,[])
 deltas=[0]*len(mq0)
 for pos in range(len(mq0)-1,-1,-1):
  old=mq0[pos]
  deltas[pos]=_og(my,old)
  temporal_boundary(my,old)
 return deltas
def temporal_repair(n,d,k,mq1,mq2,mq19,mq0,rounds=1,removals=0):
 nn=n*n
 mq0=mq0[:]
 final=mq1[:]
 for aid in mq0:
  _st(final,nn,mq19[aid][0])
 score=sum((a==b for a,b in zip(final,mq2)))
 upper=color_bound(mq1,mq2)
 for iteration in range(rounds):
  if score==upper:
   break
  seed=sum(((p+11)*v for p,v in enumerate(mq1)))+iteration*10891
  mw,_bs=(0,mq0)
  if len(mq0)<k:
   gain,pos,aid=best_insertion(n,d,mq1,mq2,mq19,mq0,seed)
   if gain:
    mw,_bs=(gain,mq0[:pos]+[aid]+mq0[pos:])
  if removals and mq0:
   deltas=deletion_deltas(n,d,mq1,mq2,mq19,mq0)
   order=sorted(range(len(mq0)),key=lambda p:(deltas[p],-p),reverse=True)
   for remove in order[:removals]:
    child=mq0[:remove]+mq0[remove+1:]
    gain,pos,aid=best_insertion(n,d,mq1,mq2,mq19,child,seed+remove)
    gain+=deltas[remove]
    if gain>mw:
     mw,_bs=(gain,child[:pos]+[aid]+child[pos:]if aid>=0 else child)
  if mw<=0:
   break
  mq0=_bs
  score+=mw
 return mq0
def solve(n,d,c,k,mq18,mq2,mq17):
 mq3=solve_route_parent(n,d,c,k,mq18[:],mq2,mq17[:])
 if k<=2:
  return mq3
 mq10,_,ops,_,_=build(n,d,mq2)
 side=n-d+1
 mq0=cancel_inverse_pairs([(x*side+y)*4+r for x,y,r in mq3])
 mq1=mq18+mq17
 mq0=temporal_repair(n,d,k,mq1,mq2,list(zip(mq10,ops)),mq0,5,5)
 final=mq1[:]
 for aid in mq0:
  _st(final,n*n,mq10[aid])
 mq4=[ops[aid]for aid in mq0]
 if sum((a==b for a,b in zip(final,mq2)))>=color_bound(mq1,mq2):
  return mq4
 rounds=30
 for powers,cap in[((3,),rounds)]+[(tuple([power]),1)for power in[6,6,9,5,12,3,6,9,12]]:
  if k-len(mq4)<2*min(powers):
   continue
  tail=route_tail(n,d,final[:n*n],mq2,final[n*n:],k-len(mq4),powers,cap)
  mq4.extend(tail)
  for x,y,r in tail:
   _st(final,n*n,mq10[(x*side+y)*4+r])
 return mq4
def runtime_early_bound(n,d,k,mq18,mq2,mq17,mq3):
 mq10,_,ops,_,_=build(n,d,mq2)
 side=n-d+1
 mq0=cancel_inverse_pairs([(x*side+y)*4+r for x,y,r in mq3])
 if k-len(mq0)<6:
  return None
 final=mq18+mq17
 for aid in mq0:
  _st(final,n*n,mq10[aid])
 upper=color_bound(mq18+mq17,mq2)
 mq4=[ops[aid]for aid in mq0]
 if sum((a==b for a,b in zip(final,mq2)))==upper:
  return mq4
 for powers,cap in[((3,),30)]+[((power,),1)for power in(6,6,9,5,12,3,6,9,12)]:
  if k-len(mq4)<2*min(powers):
   continue
  tail=route_tail(n,d,final[:n*n],mq2,final[n*n:],k-len(mq4),powers,cap)
  mq4.extend(tail)
  for x,y,r in tail:
   _st(final,n*n,mq10[(x*side+y)*4+r])
  if sum((a==b for a,b in zip(final,mq2)))==upper:
   return mq4
 return None
def temporal_best(mz,ranks,minimum):
 planes=[0]*5
 for j in range(mz.dd):
  for carry in(mz.values[j][mz.wstamp[j]],mz.goals[j][mz.mq17[j]]):
   plane=0
   while carry:
    old=planes[plane]
    planes[plane]=old^carry
    carry&=old
    plane+=1
 carry=0
 for plane in range(5):
  a,b=(planes[plane],mz.old_planes[plane])
  different=a^b
  planes[plane]=different^carry
  carry=a&b|different&carry
 mq5,value=(mz.all_bits,0)
 for plane in range(4,-1,-1):
  hits=mq5&planes[plane]
  if hits:
   mq5=hits
   value|=1<<plane
 gain=value-mz.dd-sum((a==b for a,b in zip(mz.mq17,mz.wstamp)))
 if gain<0:
  return(-1,0)
 if gain<=minimum:
  return(-1,gain)
 chosen=(mq5&-mq5).bit_length()-1
 rank=ranks[chosen]
 mq5&=mq5-1
 while mq5 and rank:
  aid=(mq5&-mq5).bit_length()-1
  if ranks[aid]<rank:
   chosen,rank=(aid,ranks[aid])
  mq5&=mq5-1
 return(chosen,gain)
def temporal_boundary(my,action):
 mq18,mq17=(my.mq18,my.mq17)
 wanted,carried=(my.mu,my.wstamp)
 mq16,values,goals=(my.mq16,my.values,my.goals)
 planes,cover_bits=(my.old_planes,my.cover_bits)
 for j,p in enumerate(my.mq19[action][0]):
  old,new=(mq18[p],mq17[j])
  old_goal,new_goal=(wanted[p],carried[j])
  changed_value=old!=new
  changed_goal=old_goal!=new_goal
  if not changed_value and(not changed_goal):
   continue
  if changed_value and changed_goal:
   for positions_row,value_row,goal_row in zip(mq16,values,goals):
    mask=positions_row[p]
    value_row[old]^=mask
    value_row[new]^=mask
    goal_row[old_goal]^=mask
    goal_row[new_goal]^=mask
  elif changed_value:
   for positions_row,row in zip(mq16,values):
    mask=positions_row[p]
    row[old]^=mask
    row[new]^=mask
  else:
   for positions_row,row in zip(mq16,goals):
    mask=positions_row[p]
    row[old_goal]^=mask
    row[new_goal]^=mask
  delta=(new==new_goal)-(old==old_goal)
  if delta:
   carry=cover_bits[p]
   plane=0
   if delta>0:
    while carry:
     mq15=planes[plane]
     planes[plane]=mq15^carry
     carry&=~mq15
     plane+=1
   else:
    while carry:
     mq15=planes[plane]
     planes[plane]=mq15^carry
     carry&=mq15
     plane+=1
  mq18[p],mq17[j]=(new,old)
  wanted[p],carried[j]=(new_goal,old_goal)
def i1_packed_expand(n,d):
 rowbits=3*d
 rowmask=(1<<rowbits)-1
 mq12=[]
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
  mq12.append(tables)
 stamp_shift=3*n*n
 board_mask=(1<<stamp_shift)-1
 stride=3*n
 if d==2:
  def rotate(value,r):
   t=mq12[r]
   return t[0][value&63]|t[1][value>>6]
  def gather(value):
   return value&63|(value>>stride&63)<<6
  def scatter(value):
   return value&63|value>>6<<stride
 else:
  def rotate(value,r):
   t=mq12[r]
   return t[0][value&511]|t[1][value>>9&511]|t[2][value>>18]
  def gather(value):
   return value&511|(value>>stride&511)<<9|(value>>2*stride&511)<<18
  def scatter(value):
   return value&511|(value>>9&511)<<stride|value>>18<<2*stride
 patch_mask=sum((rowmask<<stride*u for u in range(d)))
 patches=[]
 for x in range(n-d+1):
  for y in range(n-d+1):
   shift=3*(n*x+y)
   patches.append((shift,board_mask^patch_mask<<shift))
 def apply(my,aid):
  p,r=divmod(aid,4)
  shift,mask=patches[p]
  board,mq17=(my&board_mask,my>>stamp_shift)
  patch=gather(board>>shift)
  return board&mask|scatter(rotate(mq17,r))<<shift|rotate(patch,-r&3)<<stamp_shift
 def expand(my):
  board,mq17=(my&board_mask,my>>stamp_shift)
  paints=[scatter(rotate(mq17,r))for r in range(4)]
  for p,(shift,mask)in enumerate(patches):
   patch=gather(board>>shift)
   retained=board&mask
   for r in range(4):
    yield(4*p+r,retained|paints[r]<<shift|rotate(patch,-r&3)<<stamp_shift)
 expand.apply=apply
 return expand
def i1_search_block(n,d,mq1,wanted,depth,width=8,node_budget=160000,seed=0,expand=None,mq3=()):
 import heapq,random,itertools
 if expand is None:
  expand=i1_packed_expand(n,d)
 packed=sum((v<<3*i for i,v in enumerate(mq1)))
 goal=sum((v<<3*i for i,v in enumerate(wanted)))
 mask=sum((1<<3*i for i,v in enumerate(wanted)if v!=6))
 scored=mask.bit_count()
 def score(my):
  diff=my^goal
  return scored-((diff|diff>>1|diff>>2)&mask).bit_count()
 mq6=score(packed)
 best=[]
 upper=sum((min(mq1.count(v),wanted.count(v))for v in range(6)))
 frontier=[(packed,())]
 visited={packed}
 rng=random.Random(seed)
 used=0
 mq3=tuple(mq3[:depth])
 refstate=packed
 for level in range(max(0,depth)):
  if used>=node_budget or mq6==upper:
   break
  mq5={}
  refnode=None
  if level<len(mq3):
   aid=mq3[level]
   if level and aid==mq3[level-1]:
    mq3=mq3[:level]
   else:
    refstate=expand.apply(refstate,aid)
    used+=1
    refnode=(refstate,mq3[:level+1])
    value=score(refstate)
    if value>mq6:
     mq6,best=(value,list(refnode[1]))
     if value==upper:
      return(best,mq6,used)
  for parent,(my,path)in enumerate(frontier):
   for aid,child in itertools.islice(expand(my),max(0,node_budget-used)):
    used+=1
    if path and aid==path[-1]or child in visited or child in mq5:
     continue
    value=score(child)
    mq5[child]=(value,rng.getrandbits(32),parent,aid)
    if value>mq6:
     mq6,best=(value,list(path)+[aid])
     if value==upper:
      return(best,mq6,used)
   if used>=node_budget:
    break
  chosen=heapq.nlargest(max(1,width),mq5,key=mq5.get)
  next_frontier=[]
  for my in chosen:
   _,_,parent,aid=mq5[my]
   next_frontier.append((my,frontier[parent][1]+(aid,)))
  if refnode is not None and refnode[0]not in chosen:
   if len(next_frontier)>=max(1,width):
    next_frontier.pop()
   next_frontier.append(refnode)
  if not next_frontier:
   break
  frontier=next_frontier
  visited.update((my for my,_ in frontier))
 return(best,mq6,used)
def i1_block_repair(n,d,c,k,mq1,mq2,mq19,mq0,rounds=4,width=8,node_budget=160000):
 import random
 nn,dd=(n*n,d*d)
 final_wanted=list(mq2)+[6]*dd
 def swap(my,aid):
  for j,p in enumerate(mq19[aid][0]):
   my[p],my[nn+j]=(my[nn+j],my[p])
 def snapshots(path):
  my=list(mq1)
  forward=[my[:]]
  for aid in path:
   swap(my,aid)
   forward.append(my[:])
  mu=final_wanted[:]
  reverse=[None]*(len(path)+1)
  reverse[-1]=mu[:]
  for j in range(len(path)-1,-1,-1):
   swap(mu,path[j])
   reverse[j]=mu[:]
  return(forward,reverse)
 best=[]
 for aid in mq0:
  if aid>=0:
   if best and best[-1]==aid:
    best.pop()
   else:
    best.append(aid)
 forward,reverse=snapshots(best)
 mq6=sum((a==b for a,b in zip(forward[-1],final_wanted)))
 upper=sum((min(mq1.count(v),mq2.count(v))for v in range(c)))
 q=len(mq19)
 minimum=q*(1+max(1,width)*max(0,min(4,k)-1))+min(4,k)
 rounds=min(max(0,rounds),max(1,node_budget//max(1,minimum)))
 if not rounds or k<=0 or mq6==upper:
  return best
 seed=sum(((i+43)*v for i,v in enumerate(mq1)))+k*8161+n*319+d
 rng=random.Random(seed)
 expand=i1_packed_expand(n,d)
 for trial in range(rounds):
  allowance=node_budget//(rounds-trial)
  affordable=max(0,1+(allowance-q-32)//(max(1,width)*q))
  requested=(4,8,16,32)[trial%4]
  length=max((v for v in(4,8,16,32)if v<=min(requested,affordable)),default=min(requested,affordable))
  length=min(k,length)
  if length<=0:
   break
  span=min(length,len(best))
  left=len(best)-span if trial%4 in(0,3)else rng.randrange(len(best)-span+1)
  right=left+span
  depth=min(length,k-len(best)+span)
  block,value,used=i1_search_block(n,d,forward[left],reverse[right],depth,width,allowance,seed+trial*104729,expand,best[left:right])
  node_budget-=used
  if value>mq6:
   mq4=best[:left]+block+best[right:]
   ahead,behind=snapshots(mq4)
   actual=sum((a==b for a,b in zip(ahead[-1],final_wanted)))
   if len(mq4)<=k and actual>mq6:
    best,mq6=(mq4,actual)
    forward,reverse=(ahead,behind)
  if mq6==upper:
   break
 return best
_i1_parent=solve
def solve(n,d,c,k,mq18,mq2,mq17):
 mq3=_i1_parent(n,d,c,k,mq18[:],mq2,mq17[:])
 if k<4:
  return mq3
 mq10,_,ops,_,_=build(n,d,mq2)
 span=n-d+1
 mq0=[(x*span+y)*4+r for x,y,r in mq3]
 mq4=i1_block_repair(n,d,c,k,mq18+mq17,mq2,list(zip(mq10,ops)),mq0,rounds=8,width=8,node_budget=160000)
 return[ops[aid]for aid in mq4]
def session_suffix(n,d,c,k,mq18,mq2,mq17,mq3,width=4,depth=10,budget=120000):
 if k<4:
  return mq3
 nn=n*n
 mq1=mq18+mq17
 mq10,_,ops,_,_=build(n,d,mq2)
 span=n-d+1
 mq0=[(x*span+y)*4+r for x,y,r in mq3]
 cut=max(0,len(mq0)-depth)
 start=mq1[:]
 for aid in mq0[:cut]:
  _st(start,nn,mq10[aid])
 final=start[:]
 for aid in mq0[cut:]:
  _st(final,nn,mq10[aid])
 value=sum((a==b for a,b in zip(final,mq2)))
 if value==color_bound(mq1,mq2):
  return mq3
 block,score,_=i1_search_block(n,d,start,mq2+[6]*(d*d),min(depth,k-cut),width,budget,sum(((i+59)*v for i,v in enumerate(mq1))),mq3=mq0[cut:])
 return mq3[:cut]+[ops[aid]for aid in block]if score>value else mq3
_session_parent=solve
def solve(n,d,c,k,mq18,mq2,mq17):
 if n==d:
  return exact_two(n,d,c,min(k,2),mq18,mq2,mq17)
 mq3=_session_parent(n,d,c,k,mq18[:],mq2,mq17[:])
 mq3=session_suffix(n,d,c,k,mq18,mq2,mq17,mq3)
 mq10,_,ops,_,_=build(n,d,mq2)
 side=n-d+1
 mq0=[(x*side+y)*4+r for x,y,r in mq3]
 mq0=segment_rotations(n,d,mq18+mq17,mq2,list(zip(mq10,ops)),mq0)
 return[ops[aid]for aid in mq0]
def segment_rotations(n,d,mq1,mq2,mq19,mq0):
 nn,dd=(n*n,d*d)
 my=SequenceState(mq1,mq2,mq19,mq0,nn)
 if my.score==color_bound(mq1,mq2):
  return mq0
 mq12=[[p*d+q for u in range(d)for v in range(d)for p,q in[((u,v),(v,d-1-u),(d-1-u,d-1-v),(d-1-v,u))[r]]]for r in range(4)]
 best=(0,0,0,0)
 for left in range(len(mq0)):
  before=my.prefix[left]
  for mq11 in(1,2,3):
   changed={nn+j:before[nn+p]for j,p in enumerate(mq12[-mq11])if before[nn+j]!=before[nn+p]}
   for right in range(left,len(mq0)):
    for j,p in enumerate(mq19[mq0[right]][0]):
     old=changed.pop(nn+j,None)
     new=changed.pop(p,None)
     if old is not None:
      changed[p]=old
     if new is not None:
      changed[nn+j]=new
    base=my.prefix[right+1]
    mu=my.mu[right+1]
    gain=sum(((v==mu[p])-(base[p]==mu[p])for p,v in changed.items()if p<nn))
    for j,p in enumerate(mq12[mq11]):
     gain+=(changed.get(nn+p,base[nn+p])==mu[nn+j])-(base[nn+j]==mu[nn+j])
    if gain>best[0]:
     best=(gain,left,right+1,mq11)
 gain,left,right,mq11=best
 if gain:
  mq4=mq0[:]
  mq4[left:right]=[aid//4*4+(aid+mq11)%4 for aid in mq0[left:right]]
  actual=my.delta(left,mq4[left:right])
  if actual==gain:
   return mq4
 return mq0
'Long-horizon, bit-parallel beam candidate construction.'
import random
def million_choices(my,rng,branch=6):
 planes=[0]*5
 for j,color in enumerate(my.mq17):
  carry=my.target_bits[j][color]
  plane=0
  while carry:
   old=planes[plane]
   planes[plane]=old^carry
   carry&=old
   plane+=1
 carry=0
 for plane in range(4):
  a,b=(planes[plane],my.old_planes[plane])
  different=a^b
  planes[plane]=different^carry
  carry=a&b|different&carry
 planes[4]=carry
 mq14=my.all_actions
 out=[]
 count=len(my.mq19)
 seen={}
 while len(out)<branch and mq14:
  mq5,value=(mq14,0)
  for plane in range(4,-1,-1):
   hits=mq5&planes[plane]
   if hits:
    mq5=hits
    value|=1<<plane
  mq14^=mq5
  take=min(branch-len(out),4)
  while mq5 and take:
   offset=rng.randrange(count)
   after=mq5>>offset
   rank=(after&-after).bit_length()-1+offset if after else(mq5&-mq5).bit_length()-1
   mq5^=1<<rank
   aid=my.order[rank]
   mq9=tuple((my.mq18[p]for p in my.mq19[aid][0]))
   if seen.get(mq9,0)>=2:
    continue
   seen[mq9]=seen.get(mq9,0)+1
   out.append((aid,value-my.size))
   take-=1
  if out and value-my.size<out[0][1]-1:
   break
 return out
def million_beam(n,d,c,k,mq18,mq2,mq17,mq3,width=12,branch=6,future_weight=4,enhance=False):
 if k<3 or n==d:
  return mq3
 base=sum((a==b for a,b in zip(mq18,mq2)))
 upper=color_bound(mq18+mq17,mq2)
 mq10,_,mq8,_,_=build(n,d,mq2)
 mq19=list(zip(mq10,mq8))
 side=n-d+1
 mq1=mq18+mq17
 def score(path):
  my=mq1[:]
  for aid in path:
   _st(my,n*n,mq10[aid])
  return sum((a==b for a,b in zip(my,mq2)))
 best=[(x*side+y)*4+r for x,y,r in mq3]
 mq6=score(best)
 if mq6==upper:
  return mq3
 my=State(n,d,c,mq18[:],mq2,mq17[:])
 rng=random.Random(sum(((i+51)*v for i,v in enumerate(mq18+mq17)))+k*917)
 beam=[(my,[])]
 beam_best,beam_score=([],base)
 for depth in range(k):
  mq5=[]
  seen=set()
  for my,path in beam:
   for aid,gain in million_choices(my,rng,branch):
    if path and aid==path[-1]:
     continue
    child=clone_state(my)
    child.apply(aid)
    key=bytes(child.mq18+child.mq17)
    if key in seen:
     continue
    seen.add(key)
    path2=path+[aid]
    if child.matches>beam_score:
     beam_best,beam_score=(path2,child.matches)
    if beam_score==upper:
     return[mq8[x]for x in beam_best]
    future=max(0,child.best()[0])if depth+1<k else 0
    priority=child.matches*8+future_weight*future
    mq5.append((priority,rng.random(),child,path2))
  if not mq5:
   break
  mq5.sort(key=lambda x:(x[0],x[1]),reverse=True)
  beam=[]
  stamp_counts={}
  deferred=[]
  for _,_,my,path in mq5:
   sig=tuple(my.mq17)
   if stamp_counts.get(sig,0)>=max(2,width//4):
    deferred.append((my,path))
    continue
   stamp_counts[sig]=stamp_counts.get(sig,0)+1
   beam.append((my,path))
   if len(beam)>=width:
    break
  if len(beam)<width:
   beam.extend(deferred[:width-len(beam)])
 mq4=refine(n,d,k,mq1,mq2,mq19,beam_best,passes=6)
 mq4=pair_sweep(n,d,k,mq1,mq2,mq19,mq4,passes=2,width=24)
 if enhance:
  mq4=anneal_walk(n,d,k,mq1,mq2,mq19,mq4)
  mq4=refine(n,d,k,mq1,mq2,mq19,mq4,passes=2)
  mq4=triple_refine(n,d,k,mq1,mq2,mq19,mq4,passes=2)
  mq4=refine(n,d,k,mq1,mq2,mq19,mq4,passes=2)
 value=score(mq4)
 if value>mq6:
  best=mq4
 return[mq8[x]for x in best]
import heapq
import random
def quotient_expander(n,d):
 rowbits=3*d
 rowmask=(1<<rowbits)-1
 mq12=[]
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
  mq12.append(tables)
 stamp_shift=3*n*n
 board_mask=(1<<stamp_shift)-1
 stride=3*n
 if d==2:
  def rotate(value,r):
   t=mq12[r]
   return t[0][value&63]|t[1][value>>6]
  def gather(value):
   return value&63|(value>>stride&63)<<6
  def scatter(value):
   return value&63|value>>6<<stride
 else:
  def rotate(value,r):
   t=mq12[r]
   return t[0][value&511]|t[1][value>>9&511]|t[2][value>>18]
  def gather(value):
   return value&511|(value>>stride&511)<<9|(value>>2*stride&511)<<18
  def scatter(value):
   return value&511|(value>>9&511)<<stride|value>>18<<2*stride
 patch_mask=sum((rowmask<<stride*u for u in range(d)))
 patches=[(3*(n*x+y),board_mask^patch_mask<<3*(n*x+y))for x in range(n-d+1)for y in range(n-d+1)]
 norms={}
 def normal(mq17):
  if mq17 not in norms:
   variants=[rotate(mq17,r)for r in range(4)]
   value=min(variants)
   turn=variants.index(value)
   for r,variant in enumerate(variants):
    if variant not in norms:
     norms[variant]=(value,turn-r&3)
  return norms[mq17]
 def expand(my):
  board,mq17=(my&board_mask,my>>stamp_shift)
  paints=[scatter(rotate(mq17,r))for r in range(4)]
  for p,(shift,mask)in enumerate(patches):
   patch=gather(board>>shift)
   picked,turn=normal(patch)
   retained=board&mask|picked<<stamp_shift
   for r in range(4):
    yield(4*p+r,retained|paints[r]<<shift,turn+r&3)
 expand.normal=normal
 return expand
def fast_quotient_beam(n,d,mq1,mq2,depth,width=512,budget=800000,seed=941,weight=1):
 nn=n*n
 pack=lambda a:sum((v<<3*i for i,v in enumerate(a)))
 expand=quotient_expander(n,d)
 buf,phase=expand.normal(pack(mq1[nn:]))
 first=pack(mq1[:nn])|buf<<3*nn
 goal=pack(mq2)
 mask=sum((1<<3*i for i in range(nn)))
 rng=random.Random(seed)
 selectedmask=sum((1<<3*i for i in range(nn)if rng.randrange(4)==0))if weight else 0
 def matches(my):
  diff=my^goal
  return nn-((diff|diff>>1|diff>>2)&mask).bit_count()
 bestscore=matches(first)
 best=[]
 upper=color_bound(mq1,mq2)
 front=[(first,(),phase)]
 seen={first}
 used=0
 for level in range(depth):
  mq5={}
  for my,path,phase in front:
   for aid,child,turn in expand(my):
    used+=1
    if used>budget:
     return(best,bestscore,used)
    if child in seen or child in mq5:
     continue
    diff=child^goal
    wrong=(diff|diff>>1|diff>>2)&mask
    score=nn-wrong.bit_count()
    actual=aid//4*4+(aid+phase)%4
    if score>bestscore:
     bestscore,best=(score,list(path)+[actual])
     if score==upper:
      return(best,bestscore,used)
    rank=score*8-(wrong&selectedmask).bit_count()*weight
    mq5[child]=(rank,rng.getrandbits(32),path+(actual,),phase+turn&3)
  if not mq5:
   break
  chosen=heapq.nlargest(width,mq5,key=mq5.get)
  front=[(my,mq5[my][2],mq5[my][3])for my in chosen]
  seen.update(chosen)
 return(best,bestscore,used)
def small_beam_stage(n,d,c,k,mq18,mq2,mq17,mq3):
 if not(4<=n<=12 and 4<=k<=16):
  return mq3
 mq10,_,ops,_,_=build(n,d,mq2)
 span=n-d+1
 final=mq18+mq17
 for x,y,r in mq3:
  _st(final,n*n,mq10[(x*span+y)*4+r])
 value=sum((a==b for a,b in zip(final,mq2)))
 if value==color_bound(mq18+mq17,mq2):
  return mq3
 width=2048 if d==3 and n<=6 else 512
 path,score,_=fast_quotient_beam(n,d,mq18+mq17,mq2,k,width,1000000,941,1)
 if score>value:
  mq4=[ops[aid]for aid in path]
  return mq4
 return mq3
def macro_prefix(n,d,c,k,mq18,mq2,mq17,mq3,cuts=(0.25,0.5,0.75),mixed=False):
 nn=n*n
 mq10,_,ops,_,_=build(n,d,mq2)
 width=n-d+1
 mq1=mq18+mq17
 final=mq1[:]
 snapshots=[final[:]]
 for x,y,r in mq3:
  _st(final,nn,mq10[(x*width+y)*4+r])
  snapshots.append(final[:])
 score=sum((a==b for a,b in zip(final,mq2)))
 upper=color_bound(mq1,mq2)
 if score==upper or k<12:
  return mq3
 best=mq3
 for fraction in cuts:
  cut=int(len(mq3)*fraction)
  my=snapshots[cut]
  if sum((a==b for a,b in zip(my,mq2)))+(2 if d==3 else 1)*(k-cut)<=score:
   continue
  mq4=mq3[:cut]
  tail=route_tail(n,d,my[:nn],mq2,my[nn:],k-cut,(3,),30)
  mq4=mq4+tail
  my=my[:]
  for x,y,r in tail:
   _st(my,nn,mq10[(x*width+y)*4+r])
  if mixed:
   for power in(6,9,5,12,3,6,9):
    tail=route_tail(n,d,my[:nn],mq2,my[nn:],k-len(mq4),(power,),2)
    mq4+=tail
    for x,y,r in tail:
     _st(my,nn,mq10[(x*width+y)*4+r])
  value=sum((a==b for a,b in zip(my,mq2)))
  if value>score:
   score,best=(value,mq4)
  if value==upper:
   break
 return best
def objective_walk(n,d,c,k,mq1,mq2,mq10,mq0,refine,weighted_refine,mq19,trials=12,mode=0,passes=3):
 if k<4:
  return mq0
 nn=n*n
 upper=sum((min(mq1.count(v),mq2.count(v))for v in range(c)))
 def evaluate(path):
  row=mq1[:]
  for aid in path:
   for j,p in enumerate(mq10[aid]):
    row[p],row[nn+j]=(row[nn+j],row[p])
  return(sum((a==b for a,b in zip(row,mq2))),row)
 best=mq0[:]
 mq6,final=evaluate(best)
 if mq6==upper:
  return best
 mx=best[:]
 rng=random.Random(sum(((i+101)*v for i,v in enumerate(mq1)))+k*2381)
 for trial in range(trials):
  rate=(0.08,0.15,0.3,0.5)[trial%4]
  weights=[1+(rng.random()<rate)for _ in range(nn)]
  mq4=weighted_refine(n,d,k,mq1,mq2,weights,mq19,mx,passes=1)
  mq4=refine(n,d,k,mq1,mq2,mq19,mq4,passes=passes,seed_offset=trial*17981+80311)
  value,row=evaluate(mq4)
  if value>=mq6:
   best,mq6,final=(mq4[:],value,row)
   if value==upper:
    break
  mx=mq4 if value>=mq6-1 else best[:]
  if trial%4==3:
   mx=best[:]
 return best
_million_parent=solve
def solve(n,d,c,k,mq18,mq2,mq17):
 large=n>=24 and d==3 and(k>=120)
 mq3=(_i1_parent if n>=20 and d==3 and k>=120 else _million_parent)(n,d,c,k,mq18[:],mq2,mq17[:])
 mq3=million_beam(n,d,c,k,mq18,mq2,mq17,mq3,width=16 if large else 24)
 mq3=small_beam_stage(n,d,c,k,mq18,mq2,mq17,mq3)
 mq3=macro_prefix(n,d,c,k,mq18,mq2,mq17,mq3,cuts=(0,0.25,0.5,0.75,0.9),mixed=True)
 if not large:
  mq10,_,ops,_,_=build(n,d,mq2)
  side=n-d+1
  mq0=[(x*side+y)*4+r for x,y,r in mq3]
  mq0=objective_walk(n,d,c,k,mq18+mq17,mq2,mq10,mq0,refine,weighted_refine,list(zip(mq10,ops)),trials=8,mode=0,passes=3)
  mq3=[ops[aid]for aid in mq0]
 return mq3
def main():
 data=list(map(int,sys.stdin.buffer.read().split()))
 n,d,c,k=data[:4]
 nn=n*n
 mq8=solve(n,d,c,k,data[4:4+nn],data[4+nn:4+2*nn],data[4+2*nn:])
 print(len(mq8))
 for operation in mq8:
  print(*operation)
if __name__=='__main__':
 main()
