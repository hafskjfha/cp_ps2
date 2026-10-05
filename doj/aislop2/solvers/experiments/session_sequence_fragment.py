
def segment_rotations(n,d,initial,target,actions,sequence):
 nn,dd=n*n,d*d
 state=SequenceState(initial,target,actions,sequence,nn)
 if state.score==color_bound(initial,target):
  return sequence
 rotations=[[p*d+q for u in range(d)for v in range(d)for p,q in[((u,v),(v,d-1-u),(d-1-u,d-1-v),(d-1-v,u))[r]]]for r in range(4)]
 best=(0,0,0,0)
 for left in range(len(sequence)):
  before=state.prefix[left]
  for rotation in (1,2,3):
   changed={nn+j:before[nn+p]for j,p in enumerate(rotations[-rotation])if before[nn+j]!=before[nn+p]}
   for right in range(left,len(sequence)):
    for j,p in enumerate(actions[sequence[right]][0]):
     old=changed.pop(nn+j,None)
     new=changed.pop(p,None)
     if old is not None:
      changed[p]=old
     if new is not None:
      changed[nn+j]=new
    base=state.prefix[right+1]
    wishes=state.wishes[right+1]
    gain=sum((v==wishes[p])-(base[p]==wishes[p])for p,v in changed.items()if p<nn)
    for j,p in enumerate(rotations[rotation]):
     gain+=(changed.get(nn+p,base[nn+p])==wishes[nn+j])-(base[nn+j]==wishes[nn+j])
    if gain>best[0]:
     best=(gain,left,right+1,rotation)
 gain,left,right,rotation=best
 if gain:
  candidate=sequence[:]
  candidate[left:right]=[aid//4*4+(aid+rotation)%4 for aid in sequence[left:right]]
  actual=state.delta(left,candidate[left:right])
  if actual==gain:
   return candidate
 return sequence
