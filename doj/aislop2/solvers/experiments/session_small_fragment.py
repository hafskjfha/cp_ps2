def short_exact(n,d,c,k,grid,target,stamp,floor=0):
 expand=i1_packed_expand(n,d)
 nn=n*n
 initial=sum(v<<3*i for i,v in enumerate(grid+stamp))
 goal=sum(v<<3*i for i,v in enumerate(target+[6]*(d*d)))
 upper=color_bound(grid+stamp,target)
 if floor>=upper:return None,floor
 def records(start,depth):
  seen={start:()}
  layer=[start]
  for step in range(depth):
   following=[]
   for state in layer:
    prefix=seen[state]
    for aid,child in expand(state):
     if child not in seen:
      seen[child]=prefix+(aid,)
      following.append(child)
   layer=following
  return seen
 forward=records(initial,(k+1)//2)
 states=list(forward)
 size=(len(states)+7)//8
 buffers=[[bytearray(size)for _ in range(c)]for _ in range(nn+d*d)]
 for index,state in enumerate(states):
  offset,bit=index>>3,1<<(index&7)
  for row in buffers:
   row[state&7][offset]|=bit
   state>>=3
 masks=[[int.from_bytes(v,'little')for v in row]for row in buffers]
 allbits=(1<<len(states))-1
 answer=None
 for state,suffix in records(goal,k//2).items():
  planes=[0]*(nn.bit_length()+1)
  for row in masks:
   color=state&7
   state>>=3
   if color==6:continue
   carry=row[color]
   plane=0
   while carry:
    old=planes[plane]
    planes[plane]=old^carry
    carry&=old
    plane+=1
  hits,value=allbits,0
  for plane in range(len(planes)-1,-1,-1):
   subset=hits&planes[plane]
   if subset:
    value|=1<<plane
    hits=subset
  if value>floor:
   floor=value
   answer=list(forward[states[(hits&-hits).bit_length()-1]]+suffix[::-1])
   if floor==upper:break
 return answer,floor
