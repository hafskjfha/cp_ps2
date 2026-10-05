"""Canonical diagnostic of independent two-layer assignment construction."""
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
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

p=argparse.ArgumentParser()
p.add_argument('--limit',type=int,default=20)
p.add_argument('--rounds',type=int,default=3)
p.add_argument('--starts',type=int,default=2)
p.add_argument('--density',type=float,default=1.25)
p.add_argument('--free-rotations',action='store_true')
p.add_argument('--output',default='results/seven_sequence_layered_dev.json')
args=p.parse_args()
m=load(ROOT/'solvers/experiments/seven_construct_combined_readable.py','parent')
layered=load(ROOT/'solvers/experiments/seven_sequence_layered.py','layered')
best=json.loads((ROOT/'results/best.json').read_text())
baseline={r['id']:r for r in json.loads((ROOT/best['benchmark']).read_text())['results']}
rows=[]
for meta in json.loads((ROOT/'cases/manifest.json').read_text())['cases']:
    if 'dev' not in meta['suites']:continue
    case=parse_instance((ROOT/meta['path']).read_text())
    upper=m.color_bound(case.a+case.s,case.t)
    if baseline[meta['id']]['matches']==upper or case.k<8 or case.k*case.d**2<args.density*case.n**2:continue
    if len(rows)>=args.limit:break
    started=time.perf_counter()
    candidate=layered.improve(case.n,case.d,case.c,case.k,case.a,case.t,case.s,rounds=args.rounds,starts=args.starts,density=args.density,free_rotations=args.free_rotations)
    raw_matches=match_count(case,simulate(case,candidate)[0])
    indices,_,ops,_,_=m.build(case.n,case.d,case.t)
    side=case.n-case.d+1;sequence=[(x*side+y)*4+r for x,y,r in candidate]
    actions=list(zip(indices,ops));initial=case.a+case.s
    sequence=m.refine(case.n,case.d,case.k,initial,case.t,actions,sequence,passes=6)
    sequence=m.pair_sweep(case.n,case.d,case.k,initial,case.t,actions,sequence,passes=2,width=24)
    candidate=[ops[a] for a in sequence]
    elapsed=time.perf_counter()-started
    output=str(len(candidate))+'\n'+'\n'.join(' '.join(map(str,a)) for a in candidate)+'\n'
    validate_output(case,output.encode())
    matches=match_count(case,simulate(case,candidate)[0]);score=1000000*matches//case.n**2
    parent=baseline[meta['id']]['score']
    rows.append(dict(id=meta['id'],raw_matches=raw_matches,matches=matches,score=score,parent_score=parent,raw_delta=score-parent,retained_delta=max(0,score-parent),runtime_sec=elapsed,operations=candidate))
    report=dict(diagnostic_only=True,config=vars(args),baseline=best['file'],cases=len(rows),gain=sum(r['retained_delta'] for r in rows),wins=sum(r['retained_delta']>0 for r in rows),max_runtime_sec=max(r['runtime_sec'] for r in rows),runtime_sec=sum(r['runtime_sec'] for r in rows),results=rows)
    (ROOT/args.output).write_text(json.dumps(report,indent=2)+'\n')
    print(meta['id'],'raw',raw_matches,'refined',matches,'parent',baseline[meta['id']]['matches'],'delta',score-parent,'sec',round(elapsed,3),flush=True)
print({k:v for k,v in report.items() if k!='results'},flush=True)
