"""Diagnostic-only cache of canonically checked parent operations, never promotion evidence."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.simulate import parse_instance,simulate,match_count
from tools.validate_output import validate_output


def main():
    p=argparse.ArgumentParser()
    p.add_argument('solver',type=Path)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--jobs',type=int,default=1)
    args=p.parse_args()
    metadata=json.loads((ROOT/'cases/manifest.json').read_text())['cases']
    solver=args.solver.resolve()
    digest=hashlib.sha256(solver.read_bytes()).hexdigest()
    def evaluate(meta):
        text=(ROOT/meta['path']).read_bytes()
        case=parse_instance(text.decode())
        start=time.perf_counter()
        child=subprocess.run([sys.executable,'-I','-B',str(solver)],input=text,capture_output=True,timeout=5)
        if child.returncode or child.stderr:raise ValueError((meta['id'],child.stderr[:1000]))
        operations=validate_output(case,child.stdout)
        grid,stamp=simulate(case,operations)
        matches=match_count(case,grid)
        return dict(id=meta['id'],operations=operations,board=grid,stamp=stamp,matches=matches,
                    score=1000000*matches//case.n**2,runtime_sec=time.perf_counter()-start,
                    input_sha256=hashlib.sha256(text).hexdigest(),output_sha256=hashlib.sha256(child.stdout).hexdigest())
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        rows=list(pool.map(evaluate,metadata))
    result=dict(diagnostic_only=True,solver_sha256=digest,results=rows)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print('cached',len(rows),'total',sum(r['score'] for r in rows),'max',max(r['runtime_sec'] for r in rows),flush=True)


if __name__=='__main__':main()
