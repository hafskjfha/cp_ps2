"""Evaluate a new postprocessor on canonical parent outputs; diagnostic only."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.simulate import parse_instance,simulate,match_count

p=argparse.ArgumentParser()
p.add_argument('source',type=Path)
p.add_argument('--cache',type=Path,default=ROOT/'results/temporal_parent27_cache.json')
p.add_argument('--parent-function',default='solve_route_parent')
p.add_argument('--output',type=Path,required=True)
args=p.parse_args()
spec=importlib.util.spec_from_file_location('candidate',args.source)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
data=json.loads(args.cache.read_text());rows=[]
for item in data['results']:
    case=parse_instance((ROOT/'cases/generated'/f"{item['id']}.in").read_text())
    setattr(module,args.parent_function,lambda *unused,record=item: [tuple(a) for a in record['operations']])
    started=time.perf_counter()
    operations=module.solve(case.n,case.d,case.c,case.k,case.a[:],case.t[:],case.s[:])
    elapsed=time.perf_counter()-started
    assert len(operations)<=case.k
    final,_=simulate(case,operations)
    matches=match_count(case,final);score=1000000*matches//case.n**2
    row=dict(id=item['id'],delta=score-item['score'],score=score,matches=matches,
             runtime_sec=elapsed,operations=operations)
    rows.append(row)
report=dict(diagnostic_only=True,source_sha256=hashlib.sha256(args.source.read_bytes()).hexdigest(),
            cases=len(rows),total_score=sum(r['score'] for r in rows),score_delta=sum(r['delta'] for r in rows),
            wins=sum(r['delta']>0 for r in rows),losses=sum(r['delta']<0 for r in rows),
            max_runtime_sec=max(r['runtime_sec'] for r in rows),results=rows)
args.output.write_text(json.dumps(report,indent=2)+'\n')
print({k:v for k,v in report.items() if k!='results'},flush=True)
