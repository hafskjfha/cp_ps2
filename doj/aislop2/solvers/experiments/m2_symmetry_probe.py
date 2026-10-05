"""Diagnostic symmetry/relabeling restarts, scored by the canonical simulator."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.simulate import parse_instance, simulate, match_count
from tools.validate_output import validate_output


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--suite', default='dev')
    p.add_argument('--method', default='solve_original_iterated')
    p.add_argument('--variants', type=int, default=3)
    p.add_argument('--limit', type=int, default=1000)
    args = p.parse_args()
    spec = importlib.util.spec_from_file_location('m2solver', ROOT/'solvers/experiments/m2_runtime_readable.py')
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    baseline = {r['id']:r for r in json.loads((ROOT/'results/m2_parent_cache.json').read_text())['results']}
    rows = []
    for meta in json.loads((ROOT/'cases/manifest.json').read_text())['cases']:
        if args.suite not in meta['suites']: continue
        ins = parse_instance((ROOT/meta['path']).read_text())
        old = baseline[meta['id']]
        if old['matches'] == m.color_bound(ins.a+ins.s,ins.t) or ins.k < 3: continue
        best = old['matches']; row = dict(id=meta['id'], baseline=old['matches'], variants=[])
        for variant in range(args.variants):
            # Geometry transpose on odd variants; independently relabel colors.
            transpose = variant % 2
            colors = [(v+1+variant//2)%ins.c for v in range(ins.c)]
            def transform(grid, n):
                return [colors[grid[x+n*y] if transpose else grid[x*n+y]] for x in range(n) for y in range(n)]
            a,t,s = transform(ins.a,ins.n),transform(ins.t,ins.n),transform(ins.s,ins.d)
            start = time.perf_counter()
            ops = getattr(m,args.method)(ins.n,ins.d,ins.c,ins.k,a,t,s)
            if transpose: ops = [(y,x,(-r)%4) for x,y,r in ops]
            elapsed = time.perf_counter()-start
            raw = (str(len(ops))+'\n'+'\n'.join(' '.join(map(str,op)) for op in ops)+'\n').encode()
            validate_output(ins,raw)
            matches = match_count(ins,simulate(ins,ops)[0]);best=max(best,matches)
            row['variants'].append(dict(variant=variant,matches=matches,runtime_sec=elapsed,operations=ops))
            if best==m.color_bound(ins.a+ins.s,ins.t):break
        row.update(matches=best,delta=1000000*best//ins.n**2-old['score'])
        rows.append(row)
        out=ROOT/f'results/m2_symmetry_{args.method}_{args.suite}_{args.variants}.json'
        out.write_text(json.dumps(dict(rows=rows,delta=sum(r['delta'] for r in rows))))
        print(meta['id'],row['delta'],[round(v['runtime_sec'],3) for v in row['variants']],flush=True)
        if len(rows)>=args.limit:break
    print('total',sum(r['delta'] for r in rows),'cases',len(rows),flush=True)


if __name__=='__main__':main()
