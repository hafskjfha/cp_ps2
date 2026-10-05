"""Exact six-cycle replacement of short sequence windows."""
import sys,json,importlib.util,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from tools.simulate import parse_instance,simulate,match_count
for nm,path in [('m','m2_combined_readable.py'),('h','m2_gap_sixcycle.py')]:
 spec=importlib.util.spec_from_file_location(nm,ROOT/'solvers/experiments'/path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);globals()[nm]=mod

def improve(inst,reference,rounds=2):
 n=inst.n;nn=n*n;inds,_,ops,_,_=m.build(n,3,inst.t);side=n-2;best=match_count(inst,simulate(inst,reference)[0]);wanted=inst.t+[6]*9;attempts=0
 for _ in range(rounds):
  ids=[(x*side+y)*4+r for x,y,r in reference];st=inst.a+inst.s;fwd=[st[:]]
  for a in ids:m._st(st,nn,inds[a]);fwd.append(st[:])
  st=wanted[:];rev=[None]*(len(ids)+1);rev[-1]=st[:]
  for j in range(len(ids)-1,-1,-1):m._st(st,nn,inds[ids[j]]);rev[j]=st[:]
  answer=None
  for left in range(len(ids)-5):
   right=left+6;initial=fwd[left];goal=rev[right];base=sum(a==b for a,b in zip(initial,goal))
   if base+3<=best:continue
   word,gain=h.six_choose(n,initial,goal,minimum_gain=best-base+1);attempts+=1
   if word is not None:
    candidate=reference[:left]+list(word)+reference[right:];actual=match_count(inst,simulate(inst,candidate)[0]);assert actual==base+gain
    if actual>best:best=actual;answer=candidate
  if answer is None:break
  reference=answer
 return reference,best,attempts
if __name__=='__main__':
 limit=int(sys.argv[1])if len(sys.argv)>1 else 320
 base={r['id']:r for r in json.load(open(ROOT/'results/m2_combined_stable.json'))['results']};cache={r['id']:r for r in json.load(open(ROOT/'results/m2_gap_combined_cache.json'))['results']};rows=[]
 for meta in json.load(open(ROOT/'cases/manifest.json'))['cases'][:limit]:
  if meta['d']!=3 or meta['n']<5 or meta['k']<6:continue
  inst=parse_instance((ROOT/meta['path']).read_text());old=base[meta['id']]
  if old['matches']==m.color_bound(inst.a+inst.s,inst.t):continue
  start=time.perf_counter();ops,value,count=improve(inst,cache[meta['id']]['operations'])
  if not count:continue
  row=dict(id=meta['id'],delta=1000000*value//inst.n**2-old['score'],matches=value,base=old['matches'],runtime=time.perf_counter()-start,attempts=count,operations=ops);rows.append(row);print({k:v for k,v in row.items()if k!='operations'},flush=True)
 (ROOT/f'results/m2_gap_sixwindow_{limit}.json').write_text(json.dumps(dict(results=rows),indent=2))
