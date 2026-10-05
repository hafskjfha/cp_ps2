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
p=argparse.ArgumentParser();p.add_argument('--suite',default='dev');p.add_argument('--width',type=int,default=256);p.add_argument('--retain',action='store_true');args=p.parse_args()
spec=importlib.util.spec_from_file_location('m2reverse',ROOT/'solvers/experiments/m2_sequence_runtime_final.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
base={r['id']:r for r in json.loads((ROOT/'results/m2_parent_cache.json').read_text())['results']};rows=[]
exec((ROOT/'solvers/experiments/m2_sequence_packed_back.py').read_text(),m.__dict__)
m.FastBack=m.PackedFastBack
original=m.seven_backward_construct
def construct(*a,**kw):
    n,d,c,k,grid,target,stamp=a[:7]
    if d!=3:return original(*a,**kw)
    width=min(args.width,128) if n>=24 and k>=120 else args.width
    kw['width']=width;candidate=original(*a,**kw)
    if not args.retain:return candidate
    kw['width']=48;reference=original(*a,**kw)
    indices,_,_,_,_=m.build(n,d,target);side=n-d+1
    def score(path):
        state=grid+stamp
        for x,y,r in path:m._st(state,n*n,indices[(x*side+y)*4+r])
        return sum(a==b for a,b in zip(state,target))
    return candidate if score(candidate)>score(reference) else reference
m.seven_backward_construct=construct
for meta in json.loads((ROOT/'cases/manifest.json').read_text())['cases']:
    if args.suite not in meta['suites']:continue
    p=parse_instance((ROOT/meta['path']).read_text());b=base[meta['id']]
    if p.d!=3 or p.n<10 or p.k<12 or 100*sum(a==t for a,t in zip(p.a,p.t))>=88*m.color_bound(p.a+p.s,p.t):continue
    pats={tuple(p.t[(x+i)*p.n+y+j]for i in range(p.d)for j in range(p.d))for x in range(p.n-p.d+1)for y in range(p.n-p.d+1)}
    if len(pats)>4*p.c:continue
    st=time.perf_counter();ops=m.solve(p.n,p.d,p.c,p.k,p.a,p.t,p.s);elapsed=time.perf_counter()-st
    raw=(str(len(ops))+'\n'+'\n'.join(' '.join(map(str,op))for op in ops)+'\n').encode();validate_output(p,raw)
    value=match_count(p,simulate(p,ops)[0]);delta=1000000*value//p.n**2-b['score']
    rows.append(dict(id=meta['id'],delta=delta,matches=value,runtime_sec=elapsed,operations=ops))
    print(meta['id'],delta,round(elapsed,3),flush=True)
    (ROOT/f'results/m2_reverse_packed_{args.suite}_{args.width}_retain{int(args.retain)}.json').write_text(json.dumps(dict(rows=rows,delta=sum(r['delta']for r in rows))))
print('total',sum(r['delta']for r in rows),flush=True)
