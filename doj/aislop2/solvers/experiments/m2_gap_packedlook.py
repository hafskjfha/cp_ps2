"""Wide packed beam with exact two-step rank, compact domains only."""
import random,heapq

def beam(n,d,c,k,grid,target,stamp,expand,width=256,back=True,seed=1933,weight=3):
 nn=n*n;dd=d*d;size=nn+dd
 pack=lambda a:sum(v<<(3*i) for i,v in enumerate(a))
 initial=pack(grid+stamp);wanted=pack(target+[6]*dd)
 first,goal=(wanted,initial) if back else(initial,wanted)
 mask=sum(1<<(3*i) for i in range(size));upper=sum(min((grid+stamp).count(v),target.count(v)) for v in range(c))
 def score(state):
  diff=state^goal;return size-((diff|diff>>1|diff>>2)&mask).bit_count()
 rng=random.Random(seed);front=[(first,())];seen={first};best=score(first);answer=[];used=0
 for depth in range(k):
  records={}
  for state,path in front:
   for aid,child in expand(state):
    used+=1
    if path and aid==path[-1] or child in seen or child in records:continue
    value=score(child)
    records[child]=(value,rng.getrandbits(32),path+(aid,))
    if value>best:
     best=value;answer=list(path)+( [aid] )
     if best==upper:return(answer[::-1] if back else answer),best,used
  chosen=heapq.nlargest(width*3,records,key=records.get)
  if depth+1<k:
   ranks=[]
   for state in chosen:
    value,tie,path=records[state]
    future=value
    for aid,child in expand(state):
     used+=1
     if aid!=path[-1]:future=max(future,score(child))
    ranks.append((8*value+weight*(future-value),tie,state,path))
   ranks.sort(reverse=True)
   front=[(state,path)for _,_,state,path in ranks[:width]]
  else:front=[(state,records[state][2])for state in chosen[:width]]
  seen.update(state for state,path in front)
 return(answer[::-1] if back else answer),best,used

if __name__=='__main__':
 import sys,json,importlib.util,time
 from pathlib import Path
 ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
 from tools.simulate import parse_instance,simulate,match_count
 spec=importlib.util.spec_from_file_location('parent',ROOT/'solvers/experiments/seven_construct_fast_bytearray_readable.py')
 parent=importlib.util.module_from_spec(spec);spec.loader.exec_module(parent)
 ids=sys.argv[1].split(',') if len(sys.argv)>1 else ['case_308','case_145','case_225','case_037','case_276']
 width=int(sys.argv[2]) if len(sys.argv)>2 else 256
 back=bool(int(sys.argv[3])) if len(sys.argv)>3 else True
 weight=int(sys.argv[4]) if len(sys.argv)>4 else 3
 base={r['id']:r for r in json.load(open(ROOT/'results/checkpoints/runtime_055_254652429.benchmark.json'))['results']}
 results=[]
 for meta in json.load(open(ROOT/'cases/manifest.json'))['cases']:
  if meta['id'] not in ids:continue
  i=parse_instance((ROOT/meta['path']).read_text());start=time.perf_counter()
  aids,value,used=beam(i.n,i.d,i.c,i.k,i.a,i.t,i.s,parent.i1_packed_expand(i.n,i.d),width,back,weight=weight)
  ops=parent.build(i.n,i.d,i.t)[2];path=[ops[a]for a in aids]
  actual=match_count(i,simulate(i,path)[0]);assert actual==value
  row=dict(id=meta['id'],matches=value,base=base[meta['id']]['matches'],delta=1000000*value//i.n**2-base[meta['id']]['score'],runtime=time.perf_counter()-start,used=used,operations=path);results.append(row);print({k:v for k,v in row.items()if k!='operations'},flush=True)
 (ROOT/f'results/m2_gap_look_w{width}_b{int(back)}_wt{weight}.json').write_text(json.dumps(dict(results=results),indent=2))
