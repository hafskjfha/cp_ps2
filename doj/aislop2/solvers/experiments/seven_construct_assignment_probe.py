"""One-process provisional benchmark; no immutable benchmark changes."""
import argparse
import importlib.util
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from tools.simulate import parse_instance,simulate,match_count
from tools.validate_output import validate_output

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--mode',type=int,default=2)
    parser.add_argument('--width',type=int,default=24)
    parser.add_argument('--branch',type=int,default=8)
    parser.add_argument('--strength',type=float,default=.15)
    parser.add_argument('--limit',type=int,default=20)
    parser.add_argument('--seed',type=int,default=0)
    args=parser.parse_args()
    m=load('base','solvers/experiments/million_runtime_readable.py')
    exp=load('construction','solvers/experiments/seven_construct_assignment.py')
    current=json.loads((ROOT/'results/million_safe_stable.json').read_text())
    floor={r['id']:r for r in current['results']}
    rows=[]
    for row in json.loads((ROOT/'cases/manifest.json').read_text())['cases']:
        if 'dev' not in row['suites']:
            continue
        ins=parse_instance((ROOT/row['path']).read_text())
        parent=floor[row['id']]['matches']
        upper=m.color_bound(ins.a+ins.s,ins.t)
        if upper<=parent or ins.k<3 or ins.n==ins.d:
            continue
        start=time.perf_counter()
        aids=exp.construct(m,ins.n,ins.d,ins.c,ins.k,ins.a,ins.t,ins.s,
                           args.mode,args.width,args.branch,args.strength,args.seed)
        elapsed=time.perf_counter()-start
        _,_,ops,_,_=m.build(ins.n,ins.d,ins.t)
        operations=[ops[aid] for aid in aids]
        output=str(len(operations))+'\n'+'\n'.join(' '.join(map(str,x)) for x in operations)+'\n'
        validate_output(ins,output.encode())
        matches=match_count(ins,simulate(ins,operations)[0])
        delta=1000000*max(parent,matches)//(ins.n*ins.n)-1000000*parent//(ins.n*ins.n)
        item=dict(id=row['id'],n=ins.n,d=ins.d,k=ins.k,upper=upper,matches=matches,parent=parent,
                  delta=delta,raw_delta=matches-parent,runtime_sec=elapsed,operations=operations)
        rows.append(item)
        print(row['id'],matches-parent,delta,round(elapsed,3),flush=True)
        if len(rows)>=args.limit:
            break
    summary=dict(settings=vars(args),cases=rows,total_delta=sum(r['delta'] for r in rows),
                 wins=sum(r['delta']>0 for r in rows),runtime_sec=sum(r['runtime_sec'] for r in rows),
                 max_runtime_sec=max((r['runtime_sec'] for r in rows),default=0))
    output=ROOT/('results/seven_construct_assignment_m%d_w%d_s%s_seed%d_n%d.json' %
                 (args.mode,args.width,str(args.strength).replace('.','p'),args.seed,args.limit))
    output.write_text(json.dumps(summary))
    print({k:v for k,v in summary.items() if k!='cases'},flush=True)

if __name__=='__main__':
    main()

