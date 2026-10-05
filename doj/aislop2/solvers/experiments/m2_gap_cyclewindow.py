"""Replace weak operation windows with exact small-support permutations."""
import sys,json,importlib.util,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from tools.simulate import parse_instance,simulate,match_count
s=importlib.util.spec_from_file_location('m',ROOT/'solvers/experiments/m2_gap_cycle_integrated_readable.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

def improve(inst,reference,attempts=4):
 n=inst.n;d=inst.d;nn=n*n;dd=d*d
 inds,_,ops,_,_=m.build(n,d,inst.t);side=n-d+1
 aids=[(x*side+y)*4+r for x,y,r in reference]
 first=inst.a+inst.s;wanted=inst.t+[6]*dd
 forward=[first[:]];st=first[:]
 for a in aids:m._st(st,nn,inds[a]);forward.append(st[:])
 reverse=[None]*(len(aids)+1);st=wanted[:];reverse[-1]=st[:]
 for j in range(len(aids)-1,-1,-1):m._st(st,nn,inds[aids[j]]);reverse[j]=st[:]
 best=sum(a==b for a,b in zip(forward[-1],wanted));basebest=best;answer=reference
 windows=[]
 for length in (12,14,16,20,24):
  for left in range(len(aids)-length+1):
   right=left+length;baseline=sum(a==b for a,b in zip(forward[left],reverse[right]))
   if baseline+3<=best:continue
   windows.append((baseline,-length,left,right))
 windows.sort(reverse=True)
 count=0
 for baseline,minuslen,left,right in windows[:attempts]:
  count+=1
  state=forward[left];goal=reverse[right];depth=right-left+inst.k-len(aids)
  path,value,_,_=m.m2_small_cycle_repair(n,d,depth,state[:nn],goal,state[nn:],inds,minimum_gain=best-baseline+1)
  if value>best:
   candidate=reference[:left]+[ops[a]for a in path]+reference[right:]
   actual=match_count(inst,simulate(inst,candidate)[0]);assert actual==value,(actual,value)
   answer=candidate;best=value
 return answer,best,count,len(windows)

if __name__=='__main__':
 limit=int(sys.argv[1])if len(sys.argv)>1 else 100
 base={r['id']:r for r in json.load(open(ROOT/'results/checkpoints/runtime_055_254652429.benchmark.json'))['results']};cache={r['id']:r for r in json.load(open(ROOT/'results/m2_parent_cache.json'))['results']};rows=[]
 for meta in json.load(open(ROOT/'cases/manifest.json'))['cases'][:limit]:
  if meta['d']!=3 or meta['n']<5 or meta['k']<12:continue
  inst=parse_instance((ROOT/meta['path']).read_text());old=base[meta['id']]
  if old['matches']==m.color_bound(inst.a+inst.s,inst.t):continue
  start=time.perf_counter();ops,value,count,windows=improve(inst,cache[meta['id']]['operations'])
  row=dict(id=meta['id'],delta=1000000*value//inst.n**2-old['score'],matches=value,base=old['matches'],runtime=time.perf_counter()-start,attempts=count,windows=windows,operations=ops);rows.append(row);print({k:v for k,v in row.items()if k!='operations'},flush=True)
 (ROOT/f'results/m2_gap_cyclewindow_{limit}.json').write_text(json.dumps(dict(results=rows),indent=2))

