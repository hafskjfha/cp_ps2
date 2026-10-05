"""Small-support macro replacement in short arbitrary sequence windows."""
import sys,json,importlib.util,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from tools.simulate import parse_instance,simulate,match_count
for nm,path in [('m','m2_combined_readable.py'),('h','m2_gap_pairedswap.py')]:
 spec=importlib.util.spec_from_file_location(nm,ROOT/'solvers/experiments'/path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);globals()[nm]=mod

def improve(inst,reference,attempts=6):
 n=inst.n;d=inst.d;nn=n*n;inds,_,ops,_,_=m.build(n,d,inst.t);side=n-d+1
 ids=[(x*side+y)*4+r for x,y,r in reference];first=inst.a+inst.s;wanted=inst.t+[6]*9
 st=first[:];fwd=[st[:]]
 for aid in ids:m._st(st,nn,inds[aid]);fwd.append(st[:])
 rev=[None]*(len(ids)+1);st=wanted[:];rev[-1]=st[:]
 for j in range(len(ids)-1,-1,-1):m._st(st,nn,inds[ids[j]]);rev[j]=st[:]
 best=sum(a==b for a,b in zip(fwd[-1],wanted));answer=reference;windows=[]
 for size in (6,8,10):
  for left in range(len(ids)-size+1):
   right=left+size;base=sum(a==b for a,b in zip(fwd[left],rev[right]))
   if base+4>best:windows.append((base,-size,left,right))
 windows.sort(reverse=True);used=0
 for base,negsize,left,right in windows[:attempts]:
  state=fwd[left];goal=rev[right];depth=right-left+inst.k-len(ids)
  aids,value,count=h.paired_repair(n,d,depth,state[:nn],goal,state[nn:],inds,budget=350000,minimum_gain=best-base+1);used+=count
  if value>best:
   candidate=reference[:left]+[ops[a]for a in aids]+reference[right:]
   actual=match_count(inst,simulate(inst,candidate)[0]);assert actual==value
   best=value;answer=candidate
 return answer,best,min(attempts,len(windows)),used
if __name__=='__main__':
 limit=int(sys.argv[1])if len(sys.argv)>1 else 100
 base={r['id']:r for r in json.load(open(ROOT/'results/m2_combined_stable.json'))['results']};cache={r['id']:r for r in json.load(open(ROOT/'results/m2_gap_combined_cache.json'))['results']};rows=[]
 for meta in json.load(open(ROOT/'cases/manifest.json'))['cases'][:limit]:
  if meta['d']!=3 or meta['n']<5 or meta['k']<6:continue
  inst=parse_instance((ROOT/meta['path']).read_text());old=base[meta['id']]
  if old['matches']==m.color_bound(inst.a+inst.s,inst.t):continue
  start=time.perf_counter();ops,value,count,used=improve(inst,cache[meta['id']]['operations'])
  if not count:continue
  row=dict(id=meta['id'],delta=1000000*value//inst.n**2-old['score'],matches=value,base=old['matches'],runtime=time.perf_counter()-start,attempts=count,used=used,operations=ops);rows.append(row);print({k:v for k,v in row.items()if k!='operations'},flush=True)
 (ROOT/f'results/m2_gap_pairedwindow_{limit}.json').write_text(json.dumps(dict(results=rows),indent=2))
