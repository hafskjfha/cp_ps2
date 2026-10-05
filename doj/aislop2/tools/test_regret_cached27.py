import importlib.util,json,time,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from tools.simulate import parse_instance,simulate,match_count
name=sys.argv[1] if len(sys.argv)>1 else 'regret_lookahead'
spec=importlib.util.spec_from_file_location('r',ROOT/('solvers/experiments/'+name+'.py'));s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
helper=getattr(s,name)
cache={c['id']:c for c in json.loads((ROOT/'results/temporal_parent27_cache.json').read_text())['results']};rows=[]
for m in json.loads((ROOT/'cases/manifest.json').read_text())['cases']:
 row=cache[m['id']];i=parse_instance((ROOT/m['path']).read_text())
 if i.k<4 or row['matches']==s.color_bound(i.a+i.s,i.t):continue
 idx,_,ops,_,_=s.build(i.n,i.d,i.t);actions=list(zip(idx,ops));side=i.n-i.d+1
 seq=[]
 for x,y,r in row['operations']:
  aid=(x*side+y)*4+r
  if seq and seq[-1]==aid:seq.pop()
  else:seq.append(aid)
 start=time.perf_counter();out=helper(i.n,i.d,i.k,i.a+i.s,i.t,actions,seq);elapsed=time.perf_counter()-start
 score=1000000*match_count(i,simulate(i,[ops[aid] for aid in out])[0])//(i.n*i.n)
 rows.append(dict(id=m['id'],delta=score-row['score'],runtime=elapsed,operations=[ops[aid] for aid in out]))
 if rows[-1]['delta']:print({k:v for k,v in rows[-1].items() if k!='operations'},flush=True)
 if len(rows)%25==0:print('progress',len(rows),flush=True)
 (ROOT/('results/'+name+'_parent27_diagnostic.json')).write_text(json.dumps(dict(results=rows,total_delta=sum(r['delta'] for r in rows)),indent=2))
print('total',sum(r['delta'] for r in rows))
