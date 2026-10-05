"""Diagnostic fixed-case comparison with cached verified parent operation paths."""
import argparse,hashlib,importlib.util,json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.simulate import parse_instance,simulate,match_count
p=argparse.ArgumentParser();p.add_argument('--suite',default='dev');p.add_argument('--limit',type=int);p.add_argument('--start',type=int,default=0);p.add_argument('--output',default='results/regret_color_variants.json');args=p.parse_args()
def module(path,name):
 spec=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
s=module('solvers/experiments/regret_color.py','candidate')
cachepath=ROOT/'results/regret_parent_paths.json'
cache=json.loads(cachepath.read_text()) if cachepath.exists() else {}
rows=[]
cases=[c for c in json.loads((ROOT/'cases/manifest.json').read_text())['cases'] if args.suite in c['suites']]
cases=cases[args.start:args.start+args.limit if args.limit else None]
for i,meta in enumerate(cases):
 text=(ROOT/meta['path']).read_text();instance=parse_instance(text);key=hashlib.sha256(text.encode()).hexdigest()
 n,d,c,k=instance.n,instance.d,instance.c,instance.k
 if key not in cache:
  cache[key]=s._regret_parent(n,d,c,k,instance.a[:],instance.t[:],instance.s[:])
  cachepath.write_text(json.dumps(cache))
 ops=cache[key]
 board,_=simulate(instance,ops);base=match_count(instance,board)
 indices,_,actions,_,_=s.build(n,d,instance.t);actions=list(zip(indices,actions));side=n-d+1
 sequence=[(x*side+y)*4+r for x,y,r in ops]
 row=dict(id=meta['id'],n=n,d=d,c=c,k=k,parent_matches=base)
 for rounds in (2,6):
  start=time.perf_counter();out=s.regret_color_repair(n,d,c,k,instance.a+instance.s,instance.t,actions,sequence,rounds)
  elapsed=time.perf_counter()-start
  result=match_count(instance,simulate(instance,[actions[aid][1] for aid in out])[0]);assert result>=base
  row[str(rounds)]=dict(matches=result,delta=(1000000*result//(n*n))-(1000000*base//(n*n)),runtime=elapsed)
 rows.append(row)
 if any(row[str(q)]['delta'] for q in (2,6)):print(row,flush=True)
 if i%20==19:print('progress',i+1,flush=True)
 Path(args.output).write_text(json.dumps(dict(results=rows,totals={str(q):sum(r[str(q)]['delta'] for r in rows) for q in (2,6)}),indent=2))
print('done',{str(q):sum(r[str(q)]['delta'] for r in rows) for q in (2,6)})
