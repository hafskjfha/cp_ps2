import argparse
import json
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from solvers.experiments.m2_construct_probe import load
from tools.simulate import parse_instance,simulate,match_count
from tools.validate_output import validate_output

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--width',type=int,default=24)
    ap.add_argument('--cuts',default='.25,.5,.75');ap.add_argument('--suite',default='dev')
    ap.add_argument('--limit',type=int,default=100);ap.add_argument('--ids',default='')
    args=ap.parse_args()
    m=load('base','solvers/experiments/seven_construct_fast_bytearray_readable.py')
    exp=load('split','solvers/experiments/m2_construct_split.py')
    cache={r['id']:r for r in json.loads((ROOT/'results/m2_parent_cache.json').read_text())['results']}
    report=dict(settings=vars(args),diagnostic_only=True,cases=[])
    dest=ROOT/('results/m2_construct_split_%s_w%d_c%s.json'%(args.suite,args.width,args.cuts.replace('.','p').replace(',','_')))
    for meta in json.loads((ROOT/'cases/manifest.json').read_text())['cases']:
        if args.suite not in meta['suites']:continue
        if args.ids and meta['id']not in args.ids.split(','):continue
        ins=parse_instance((ROOT/meta['path']).read_text());ref=cache[meta['id']]
        if ins.k<12 or ins.n<8 or ref['matches']==m.color_bound(ins.a+ins.s,ins.t):continue
        start=time.perf_counter()
        operations=exp.improve(m,ins.n,ins.d,ins.c,ins.k,ins.a,ins.t,ins.s,ref['operations'],args.width,tuple(map(float,args.cuts.split(','))))
        elapsed=time.perf_counter()-start
        output=str(len(operations))+'\n'+'\n'.join(' '.join(map(str,op))for op in operations)+'\n'
        validate_output(ins,output.encode());matches=match_count(ins,simulate(ins,operations)[0])
        assert matches>=ref['matches']
        delta=1000000*matches//ins.n**2-ref['score']
        report['cases'].append(dict(id=meta['id'],n=ins.n,d=ins.d,k=ins.k,parent=ref['matches'],matches=matches,delta=delta,runtime_sec=elapsed,operations=operations))
        report.update(total_delta=sum(r['delta']for r in report['cases']),wins=sum(r['delta']>0 for r in report['cases']),runtime_sec=sum(r['runtime_sec']for r in report['cases']),max_runtime_sec=max(r['runtime_sec']for r in report['cases']))
        dest.write_text(json.dumps(report));print(meta['id'],matches-ref['matches'],delta,round(elapsed,3),flush=True)
        if len(report['cases'])>=args.limit:break
    print({k:v for k,v in report.items()if k!='cases'},flush=True)
if __name__=='__main__':main()
