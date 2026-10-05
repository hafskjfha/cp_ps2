"""Canonical cached objective-dropout experiment."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from tools.simulate import parse_instance,simulate,match_count
from tools.validate_output import validate_output
def load(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/('solvers/experiments/'+name+'.py'))
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=argparse.ArgumentParser();p.add_argument('--suite',default='dev');p.add_argument('--trials',type=int,default=16);args=p.parse_args()
m=load('m2_runtime_readable');drop=load('m2_dropout')
base={r['id']:r for r in json.loads((ROOT/'results/m2_parent_cache.json').read_text())['results']};rows=[]
for meta in json.loads((ROOT/'cases/manifest.json').read_text())['cases']:
    if args.suite not in meta['suites']:continue
    p=parse_instance((ROOT/meta['path']).read_text());b=base[meta['id']]
    if b['matches']==m.color_bound(p.a+p.s,p.t) or p.k<4:continue
    st=time.perf_counter();ops=drop.improve(m,p.n,p.d,p.c,p.k,p.a,p.t,p.s,b['operations'],args.trials);elapsed=time.perf_counter()-st
    raw=(str(len(ops))+'\n'+'\n'.join(' '.join(map(str,op)) for op in ops)+'\n').encode();validate_output(p,raw)
    value=match_count(p,simulate(p,ops)[0]);delta=1000000*value//p.n**2-b['score'];assert delta>=0
    rows.append(dict(id=meta['id'],delta=delta,matches=value,runtime_sec=elapsed,operations=ops))
    print(meta['id'],delta,round(elapsed,3),flush=True)
    (ROOT/f'results/m2_dropout_{args.suite}_{args.trials}.json').write_text(json.dumps(dict(rows=rows,delta=sum(r['delta'] for r in rows))))
print('total',sum(r['delta'] for r in rows),flush=True)
