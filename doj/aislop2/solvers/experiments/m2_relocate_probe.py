import argparse,importlib.util,json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from tools.simulate import parse_instance,simulate,match_count
from tools.validate_output import validate_output
from solvers.experiments.m2_relocate import improve
p=argparse.ArgumentParser();p.add_argument('--suite',default='dev');p.add_argument('--rounds',type=int,default=6);p.add_argument('--plateau',action='store_true');args=p.parse_args()
spec=importlib.util.spec_from_file_location('m',ROOT/'solvers/experiments/m2_sequence_runtime_final.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
base={r['id']:r for r in json.loads((ROOT/'results/m2_gap_combined_cache.json').read_text())['results']};rows=[]
for meta in json.loads((ROOT/'cases/manifest.json').read_text())['cases']:
    if args.suite not in meta['suites']:continue
    ins=parse_instance((ROOT/meta['path']).read_text());b=base[meta['id']]
    if ins.k<3 or b['matches']==m.color_bound(ins.a+ins.s,ins.t):continue
    st=time.perf_counter();ops=improve(m,ins.n,ins.d,ins.c,ins.k,ins.a,ins.t,ins.s,b['operations'],args.rounds,args.plateau);elapsed=time.perf_counter()-st
    raw=(str(len(ops))+'\n'+'\n'.join(' '.join(map(str,op))for op in ops)+'\n').encode();validate_output(ins,raw)
    value=match_count(ins,simulate(ins,ops)[0]);delta=1000000*value//ins.n**2-1000000*b['matches']//ins.n**2
    rows.append(dict(id=meta['id'],matches=value,delta=delta,runtime_sec=elapsed,operations=ops));print(meta['id'],delta,round(elapsed,3),flush=True)
    (ROOT/f'results/m2_relocate_{args.suite}_{args.rounds}_{int(args.plateau)}.json').write_text(json.dumps(dict(rows=rows,delta=sum(r['delta']for r in rows))),encoding='utf8')
print('total',sum(r['delta']for r in rows),flush=True)
