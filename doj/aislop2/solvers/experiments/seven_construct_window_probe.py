"""Canonical diagnostic on cached seeds, scored against the current55 floor."""
import argparse
import importlib.util
import json
import sys
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from tools.simulate import parse_instance,simulate,match_count
from tools.validate_output import validate_output

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--limit',type=int,default=20)
    parser.add_argument('--rounds',type=int,default=3)
    parser.add_argument('--width',type=int,default=24)
    parser.add_argument('--ids',default='')
    parser.add_argument('--neutral',action='store_true')
    args=parser.parse_args()
    m=load('base','solvers/experiments/seven_construct_fast_bytearray_readable.py')
    exp=load('window','solvers/experiments/seven_construct_window.py')
    cache={r['id']:r for r in json.loads((ROOT/'results/seven_parent_cache.json').read_text())['results']}
    for r in json.loads((ROOT/'results/seven_construct_integrated_early_w16_n100_fast_complement.json').read_text())['cases']:
        if r['matches']>cache[r['id']]['matches']:cache[r['id']]=r
    floor={r['id']:r for r in json.loads((ROOT/'results/seven_combined_stable.json').read_text())['results']}
    rows=[]
    for meta in json.loads((ROOT/'cases/manifest.json').read_text())['cases']:
        if 'dev'not in meta['suites']:continue
        if args.ids and meta['id']not in args.ids.split(','):continue
        ins=parse_instance((ROOT/meta['path']).read_text())
        current=floor[meta['id']]['matches']
        if ins.n<6 or ins.k<8 or current==m.color_bound(ins.a+ins.s,ins.t):continue
        seed=cache[meta['id']];side=ins.n-ins.d+1
        indices,_,ops,_,_=m.build(ins.n,ins.d,ins.t)
        path=[(x*side+y)*4+r for x,y,r in seed['operations']]
        stats={};start=time.perf_counter()
        candidate=exp.window_repair(m,ins.n,ins.d,ins.c,ins.k,ins.a+ins.s,ins.t,indices,path,args.rounds,args.width,stats=stats,neutral=args.neutral)
        elapsed=time.perf_counter()-start
        operations=[ops[aid]for aid in candidate]
        output=str(len(operations))+'\n'+'\n'.join(' '.join(map(str,op))for op in operations)+'\n'
        validate_output(ins,output.encode())
        matches=match_count(ins,simulate(ins,operations)[0])
        assert matches>=seed['matches']
        delta=1000000*max(current,matches)//(ins.n*ins.n)-1000000*current//(ins.n*ins.n)
        search_delta=1000000*max(current,matches)//(ins.n*ins.n)-1000000*max(current,seed['matches'])//(ins.n*ins.n)
        row=dict(id=meta['id'],seed_matches=seed['matches'],parent=current,matches=matches,delta=delta,
                 search_delta=search_delta,runtime_sec=elapsed,operations=operations,**stats)
        rows.append(row);print(meta['id'],matches-current,delta,round(elapsed,3),stats['accepted_windows'],flush=True)
        if len(rows)>=args.limit:break
    report=dict(settings=vars(args),diagnostic_only=True,seed_cache='best_known053_and16complementary_paths',
                baseline='measured combined55',cases=rows,total_delta=sum(r['delta']for r in rows),
                new_search_delta=sum(r['search_delta']for r in rows),
                wins=sum(r['delta']>0 for r in rows),runtime_sec=sum(r['runtime_sec']for r in rows),
                max_runtime_sec=max((r['runtime_sec']for r in rows),default=0))
    name='results/seven_construct_window_w%d_r%d_n%d%s.json'%(args.width,args.rounds,args.limit,'_neutral'if args.neutral else '')
    (ROOT/name).write_text(json.dumps(report,indent=2));print({k:v for k,v in report.items()if k!='cases'},flush=True)

if __name__=='__main__':main()
