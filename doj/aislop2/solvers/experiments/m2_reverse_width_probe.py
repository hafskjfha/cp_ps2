"""Whole-pipeline qualification diagnostic for a wider reverse constructor."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from tools.simulate import parse_instance,simulate,match_count
from tools.validate_output import validate_output
p=argparse.ArgumentParser();p.add_argument('--suite',default='dev');p.add_argument('--width',type=int,default=128);args=p.parse_args()
spec=importlib.util.spec_from_file_location('m2reverse',ROOT/'solvers/experiments/m2_runtime_readable.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
base={r['id']:r for r in json.loads((ROOT/'results/m2_parent_cache.json').read_text())['results']};rows=[]
original=m.seven_backward_construct
def construct(*a,**kw):kw['width']=args.width;return original(*a,**kw)
m.seven_backward_construct=construct
for meta in json.loads((ROOT/'cases/manifest.json').read_text())['cases']:
    if args.suite not in meta['suites']:continue
    p=parse_instance((ROOT/meta['path']).read_text());b=base[meta['id']]
    if p.n<10 or p.k<12 or 100*sum(a==t for a,t in zip(p.a,p.t))>=88*m.color_bound(p.a+p.s,p.t):continue
    pats={tuple(p.t[(x+i)*p.n+y+j]for i in range(p.d)for j in range(p.d))for x in range(p.n-p.d+1)for y in range(p.n-p.d+1)}
    if len(pats)>4*p.c:continue
    st=time.perf_counter();ops=m.solve(p.n,p.d,p.c,p.k,p.a,p.t,p.s);elapsed=time.perf_counter()-st
    raw=(str(len(ops))+'\n'+'\n'.join(' '.join(map(str,op))for op in ops)+'\n').encode();validate_output(p,raw)
    value=match_count(p,simulate(p,ops)[0]);delta=1000000*value//p.n**2-b['score']
    rows.append(dict(id=meta['id'],delta=delta,matches=value,runtime_sec=elapsed,operations=ops))
    print(meta['id'],delta,round(elapsed,3),flush=True)
    (ROOT/f'results/m2_reverse_width_{args.suite}_{args.width}.json').write_text(json.dumps(dict(rows=rows,delta=sum(r['delta']for r in rows))))
print('total',sum(r['delta']for r in rows),flush=True)
