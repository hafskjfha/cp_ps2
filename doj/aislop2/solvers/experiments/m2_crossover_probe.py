"""Canonical cached genetic recombination experiment."""
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
m=load('m2_runtime_readable');cross=load('m2_crossover')
base={r['id']:r for r in json.loads((ROOT/'results/m2_parent_cache.json').read_text())['results']}
old={r['id']:r for r in json.loads((ROOT/'results/seven_parent_cache.json').read_text())['results']}
sym={r['id']:r for r in json.loads((ROOT/'results/m2_symmetry_solve_original_iterated_dev_2.json').read_text())['rows']}
rows=[]
for meta in json.loads((ROOT/'cases/manifest.json').read_text())['cases']:
    if 'dev' not in meta['suites']:continue
    p=parse_instance((ROOT/meta['path']).read_text());b=base[meta['id']]
    if b['matches']==m.color_bound(p.a+p.s,p.t) or p.k<8:continue
    alternatives=[old[meta['id']]['operations']]+[x['operations'] for x in sym.get(meta['id'],{}).get('variants',[])]
    st=time.perf_counter();ops=cross.improve(m,p.n,p.d,p.c,p.k,p.a,p.t,p.s,b['operations'],alternatives)
    elapsed=time.perf_counter()-st
    raw=(str(len(ops))+'\n'+'\n'.join(' '.join(map(str,op)) for op in ops)+'\n').encode();validate_output(p,raw)
    value=match_count(p,simulate(p,ops)[0]);delta=1000000*value//p.n**2-b['score']
    rows.append(dict(id=meta['id'],delta=delta,matches=value,runtime_sec=elapsed,operations=ops))
    print(meta['id'],delta,round(elapsed,3),flush=True)
    (ROOT/'results/m2_crossover_dev.json').write_text(json.dumps(dict(rows=rows,delta=sum(r['delta'] for r in rows))))
print('total',sum(r['delta'] for r in rows),flush=True)
