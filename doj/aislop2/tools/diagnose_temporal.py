"""Canonical diagnostic using previously validated parent sequences."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.simulate import parse_instance,simulate,match_count

p=argparse.ArgumentParser()
p.add_argument('--cache',type=Path,default=ROOT/'results/temporal_parent39_cache.json')
p.add_argument('--rounds',type=int,default=1)
p.add_argument('--removals',type=int,default=0)
p.add_argument('--output',type=Path,required=True)
args=p.parse_args()
spec=importlib.util.spec_from_file_location('temporal',ROOT/'solvers/experiments/temporal_insert.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
data=json.loads(args.cache.read_text())
rows=[]
for item in data['results']:
    case=parse_instance((ROOT/'cases/generated'/f"{item['id']}.in").read_text())
    if item['matches']==module.color_bound(case.a+case.s,case.t):continue
    operations=module.cancel_inverse_pairs(item['operations'])
    if not args.removals and len(operations)>=case.k:continue
    indices,_,ops,_,_=module.build(case.n,case.d,case.t)
    side=case.n-case.d+1
    sequence=[(x*side+y)*4+r for x,y,r in operations]
    started=time.perf_counter()
    candidate=module.temporal_repair(case.n,case.d,case.k,case.a+case.s,case.t,list(zip(indices,ops)),
                                     sequence,args.rounds,args.removals)
    elapsed=time.perf_counter()-started
    final,_=simulate(case,[ops[aid] for aid in candidate])
    matches=match_count(case,final)
    score=1000000*matches//case.n**2
    row=dict(id=item['id'],delta=score-item['score'],matches_delta=matches-item['matches'],runtime_sec=elapsed,
             canceled=len(item['operations'])-len(operations),operations=len(candidate))
    rows.append(row)
    if row['delta']:print(row,flush=True)
report=dict(diagnostic_only=True,cases=len(rows),score_delta=sum(r['delta'] for r in rows),
            wins=sum(r['delta']>0 for r in rows),losses=sum(r['delta']<0 for r in rows),
            max_runtime_sec=max((r['runtime_sec'] for r in rows),default=0),results=rows)
args.output.write_text(json.dumps(report,indent=2)+'\n')
print({k:v for k,v in report.items() if k!='results'},flush=True)
