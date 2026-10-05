"""Coordinate descent over repeated-pair six-operation macros."""
import sys,json,importlib.util,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from tools.simulate import parse_instance,simulate,match_count
spec=importlib.util.spec_from_file_location('m',ROOT/'solvers/experiments/seven_construct_fast_bytearray_readable.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
_CACHE={}
def patterns(n,d):
 if(n,d)in _CACHE:return _CACHE[n,d]
 nn=n*n;out=[];offsets=[[(u,v),(v,d-1-u),(d-1-u,d-1-v),(d-1-v,u)]for u in range(d)for v in range(d)]
 for dx in range(d):
  for dy in range(1 if dx==0 else 1-d,d):
   for r in range(4):
    left=[xy[r]for xy in offsets]
    for s in range(4):
     right=[(dx+xy[s][0],dy+xy[s][1])for xy in offsets];cells=set(left+right)
     for rev in range(2):
      a,b=(right,left)if rev else(left,right);state={p:p for p in cells};state.update({j:j for j in range(d*d)})
      for _ in range(3):
       for patch in(a,b):
        for j,p in enumerate(patch):state[j],state[p]=state[p],state[j]
      mapping=[]
      for p,q in state.items():
       if p==q:continue
       dst=nn+p if isinstance(p,int)else p[0]*n+p[1];src=nn+q if isinstance(q,int)else q[0]*n+q[1]
       mapping.append((dst,src))
      if mapping:out.append((dx,dy,r,s,rev,mapping))
 _CACHE[n,d]=out;return out

def choose(n,d,initial,wanted):
 nn=n*n;width=n-d+1;pats=patterns(n,d)
 shifts=lambda bits,off:bits>>off if off>=0 else bits<<-off
 have=[0]*6;wish=[0]*6;agree=0
 for p,v in enumerate(initial[:nn]):have[v]|=1<<p
 for p,v in enumerate(wanted[:nn]):
  if v!=6:wish[v]|=1<<p
  if initial[p]==v:agree|=1<<p
 offsets={p for *_,mp in pats for p,_ in mp if p<nn};sources={q for *_,mp in pats for _,q in mp if q<nn}
 wishes={p:tuple(shifts(b,p)for b in wish)for p in offsets};values={q:tuple(shifts(b,q)for b in have)for q in sources};old={p:shifts(agree,p)for p in offsets};legal={};cache={};best=-10**9;word=None
 for dx,dy,r,s,rev,mp in pats:
  if(dx,dy)not in legal:
   left,right=max(0,-dy),min(width,width-dy)
   row=((1<<(right-left))-1)<<left if right>left else 0
   legal[dx,dy]=sum(row<<(x*n)for x in range(max(0,width-dx)))
  anchors=legal[dx,dy]
  if not anchors:continue
  planes=[0]*(2*len(mp)+1).bit_length()
  for p,q in mp:
   if p>=nn:
    prior=anchors if initial[p]==wanted[p]else 0
    new=anchors if q>=nn and initial[q]==wanted[p]else 0
    if q<nn and wanted[p]!=6:new=values[q][wanted[p]]
   else:
    prior=old[p]
    if q>=nn:new=wishes[p][initial[q]]
    else:
     key=(p,q)
     if key not in cache:
      hits=0
      for a,b in zip(wishes[p],values[q]):hits|=a&b
      cache[key]=hits
     new=cache[key]
   for carry in (new&anchors,anchors&~prior):
    i=0
    while carry:planes[i],carry=planes[i]^carry,planes[i]&carry;i+=1
  cand=anchors;value=0
  for i in range(len(planes)-1,-1,-1):
   hits=cand&planes[i]
   if hits:cand=hits;value|=1<<i
  gain=value-len(mp)
  if gain>best:
   best=gain;base=(cand&-cand).bit_length()-1;x,y=divmod(base,n);a=(x*width+y)*4+r;b=((x+dx)*width+y+dy)*4+s
   word=([b,a]if rev else[a,b])*3
 return word,best

def improve(inst,reference):
 n=inst.n;d=inst.d;nn=n*n;indices,_,ops,_,_=m.build(n,d,inst.t);width=n-d+1;path=[(x*width+y)*4+r for x,y,r in reference];wanted=inst.t+[6]*(d*d)
 best=match_count(inst,simulate(inst,reference)[0]);attempts=0
 hits=[j for j in range(len(path)-5)if path[j:j+2]*3==path[j:j+6]]
 for left in hits:
  st=inst.a+inst.s
  for a in path[:left]:m._st(st,nn,indices[a])
  goal=wanted[:]
  for a in reversed(path[left+6:]):m._st(goal,nn,indices[a])
  base=sum(a==b for a,b in zip(st,goal));block,gain=choose(n,d,st,goal);attempts+=1
  if base+gain>best:
   candidate=path[:left]+block+path[left+6:];actual=match_count(inst,simulate(inst,[ops[a]for a in candidate])[0]);assert actual==base+gain,(actual,base,gain)
   best=actual;path=candidate
 return [ops[a]for a in path],best,attempts
if __name__=='__main__':
 limit=int(sys.argv[1])if len(sys.argv)>1 else 100
 base={r['id']:r for r in json.load(open(ROOT/'results/checkpoints/runtime_055_254652429.benchmark.json'))['results']};cache={r['id']:r for r in json.load(open(ROOT/'results/m2_parent_cache.json'))['results']};rows=[]
 for meta in json.load(open(ROOT/'cases/manifest.json'))['cases'][:limit]:
  if meta['d']!=3 or meta['n']<5 or meta['k']<6:continue
  inst=parse_instance((ROOT/meta['path']).read_text());old=base[meta['id']]
  if old['matches']==m.color_bound(inst.a+inst.s,inst.t):continue
  start=time.perf_counter();ops,value,count=improve(inst,cache[meta['id']]['operations'])
  if not count:continue
  row=dict(id=meta['id'],delta=1000000*value//inst.n**2-old['score'],matches=value,base=old['matches'],runtime=time.perf_counter()-start,attempts=count,operations=ops);rows.append(row);print({k:v for k,v in row.items()if k!='operations'},flush=True)
 (ROOT/f'results/m2_gap_macrorefine_{limit}.json').write_text(json.dumps(dict(results=rows),indent=2))
