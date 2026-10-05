"""Single-worker canonical diagnostics; does not qualify a checkpoint."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from tools.simulate import parse_instance,simulate,match_count
from tools.validate_output import validate_output

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--width',type=int,default=24)
    parser.add_argument('--branch',type=int,default=8)
    parser.add_argument('--strength',type=float,default=.15)
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--mode',type=int,default=0)
    parser.add_argument('--suite',default='dev')
    parser.add_argument('--limit',type=int,default=100)
    parser.add_argument('--ids',default='')
    parser.add_argument('--helper',default='reverse')
    args=parser.parse_args()
    m=load('base','solvers/experiments/seven_construct_fast_bytearray_readable.py')
    exp=load('helper','solvers/experiments/m2_construct_'+args.helper+'.py')
    floors={r['id']:r for r in json.loads((ROOT/'results/checkpoints/runtime_055_254652429.benchmark.json').read_text())['results']}
    report=dict(settings=vars(args),diagnostic_only=True,cases=[])
    dest=ROOT/('results/m2_construct_%s_%s_w%d_b%d_s%s_seed%d_m%d.json'%(args.helper,args.suite,args.width,args.branch,str(args.strength).replace('.','p'),args.seed,args.mode))
    for row in json.loads((ROOT/'cases/manifest.json').read_text())['cases']:
        if args.suite not in row['suites']:continue
        if args.ids and row['id']not in args.ids.split(','):continue
        ins=parse_instance((ROOT/row['path']).read_text())
        floor=floors[row['id']]['matches'];upper=m.color_bound(ins.a+ins.s,ins.t)
        if upper<=floor or ins.k<3 or ins.n==ins.d:continue
        start=time.perf_counter()
        operations=exp.construct(m,ins.n,ins.d,ins.c,ins.k,ins.a,ins.t,ins.s,args.width,args.branch,args.strength,args.seed,args.mode)
        elapsed=time.perf_counter()-start
        output=str(len(operations))+'\n'+'\n'.join(' '.join(map(str,op))for op in operations)+'\n'
        validate_output(ins,output.encode())
        matches=match_count(ins,simulate(ins,operations)[0])
        delta=1000000*max(floor,matches)//ins.n**2-1000000*floor//ins.n**2
        item=dict(id=row['id'],family=row['family'],n=ins.n,d=ins.d,k=ins.k,parent=floor,matches=matches,delta=delta,runtime_sec=elapsed,operations=operations)
        report['cases'].append(item)
        report.update(total_delta=sum(r['delta']for r in report['cases']),wins=sum(r['delta']>0 for r in report['cases']),runtime_sec=sum(r['runtime_sec']for r in report['cases']),max_runtime_sec=max(r['runtime_sec']for r in report['cases']))
        dest.write_text(json.dumps(report))
        print(row['id'],matches-floor,delta,round(elapsed,3),flush=True)
        if len(report['cases'])>=args.limit:break
    print({k:v for k,v in report.items()if k!='cases'},flush=True)

if __name__=='__main__':main()
