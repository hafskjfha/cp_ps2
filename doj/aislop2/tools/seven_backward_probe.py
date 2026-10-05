"""Canonical diagnostic for independent backwards construction."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.simulate import parse_instance,simulate,match_count
from tools.validate_output import validate_output
def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=argparse.ArgumentParser();p.add_argument('--width',type=int,default=24);p.add_argument('--limit',type=int,default=100);p.add_argument('--future',type=int,default=3);p.add_argument('--suite',default='dev');p.add_argument('--mixed',type=int,default=0);p.add_argument('--engine',default='seven_backward');args=p.parse_args()
m=load(ROOT/'solvers/experiments/million_safe_readable.py','parent')
b=load(ROOT/f'solvers/experiments/{args.engine}.py','backward')
parent={r['id']:r for r in json.loads((ROOT/'results/checkpoints/runtime_053_254103898.benchmark.json').read_text())['results']}
rows=[]
for meta in [x for x in json.loads((ROOT/'cases/manifest.json').read_text())['cases']if args.suite in x['suites']][:args.limit]:
    case=parse_instance((ROOT/meta['path']).read_text())
    base=parent[meta['id']]
    upper=m.color_bound(case.a+case.s,case.t)
    if base['matches']==upper or case.k<3 or case.n==case.d:continue
    start=time.perf_counter()
    ops=b.construct(m,case.n,case.d,case.c,case.k,case.a,case.t,case.s,width=args.width,future_weight=args.future,mixed=args.mixed)
    elapsed=time.perf_counter()-start
    validate_output(case,(str(len(ops))+'\n'+'\n'.join(' '.join(map(str,op))for op in ops)+'\n').encode())
    score=1000000*match_count(case,simulate(case,ops)[0])//case.n**2
    delta=max(0,score-base['score'])
    rows.append(dict(id=meta['id'],score=score,delta=delta,runtime_sec=elapsed,operations=ops))
    if delta or len(rows)%10==0:print(meta['id'],score,delta,round(elapsed,3),'total',sum(r['delta']for r in rows),flush=True)
out=dict(diagnostic_only=True,parameters=vars(args),gain=sum(r['delta']for r in rows),runtime_sec=sum(r['runtime_sec']for r in rows),max_runtime_sec=max((r['runtime_sec']for r in rows),default=0),results=rows)
(ROOT/f'results/{args.engine}_{args.width}_{args.future}_{args.suite}_m{args.mixed}.json').write_text(json.dumps(out)+'\n')
print({k:v for k,v in out.items()if k!='results'},flush=True)
