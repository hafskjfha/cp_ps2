"""Conjugates of a six-stamp double-transposition macro."""
_PAIR_GEOMETRY=None

def paired_repair(n,d,k,grid,target,stamp,actions,budget=1000000,minimum_gain=1):
 nn=n*n;dd=d*d;width=n-d+1;size=nn+dd
 def canonical(a,b,c,e):
  if a>b:a,b=b,a
  if c>e:c,e=e,c
  return(a,b,c,e)if a<c else(c,e,a,b)
 global _PAIR_GEOMETRY
 if _PAIR_GEOMETRY is not None and _PAIR_GEOMETRY[0]==(n,d):
  direct,renames=_PAIR_GEOMETRY[1:]
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
  _PAIR_GEOMETRY=(n,d),direct,renames
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

if __name__=='__main__':
 import sys,json,importlib.util,time
 from pathlib import Path
 ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
 from tools.simulate import parse_instance,simulate,match_count
 s=importlib.util.spec_from_file_location('m',ROOT/'solvers/experiments/m2_combined_readable.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
 cache={r['id']:r for r in json.load(open(ROOT/'results/m2_gap_combined_cache.json'))['results']};base={r['id']:r for r in json.load(open(ROOT/'results/m2_combined_stable.json'))['results']};rows=[]
 for meta in json.load(open(ROOT/'cases/manifest.json'))['cases']:
  if meta['d']!=3 or meta['n']<5 or meta['k']<6:continue
  i=parse_instance((ROOT/meta['path']).read_text());reference=cache[meta['id']]['operations'];old=base[meta['id']];upper=m.color_bound(i.a+i.s,i.t)
  if old['matches']==upper:continue
  inds,_,ops,_,_=m.build(i.n,i.d,i.t);answer=reference;best=old['matches'];start=time.perf_counter();attempts=0
  cuts=[len(reference)]
  if i.n<=10:cuts+=list(range(min(len(reference),i.k-6),-1,-1))
  for cut in dict.fromkeys(cuts):
   if i.k-cut<6:continue
   grid,stamp=simulate(i,reference[:cut]);score=match_count(i,grid)
   if score+4<=best:continue
   attempts+=1
   path,value,used=paired_repair(i.n,i.d,i.k-cut,grid,i.t,stamp,inds,minimum_gain=best-score+1)
   candidate=reference[:cut]+[ops[a]for a in path];assert match_count(i,simulate(i,candidate)[0])==value
   if value>best:best=value;answer=candidate
  if not attempts:continue
  row=dict(id=meta['id'],gain=1000000*best//i.n**2-old['score'],matches=best,base=old['matches'],runtime=time.perf_counter()-start,attempts=attempts,operations=answer);rows.append(row);print({k:v for k,v in row.items()if k!='operations'},flush=True)
 (ROOT/'results/m2_gap_pairedswap.json').write_text(json.dumps(dict(results=rows),indent=2))
