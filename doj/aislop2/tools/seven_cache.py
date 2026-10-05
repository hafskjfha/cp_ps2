"""Progressive diagnostic operation cache; not qualification evidence."""
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

solver=ROOT/'submissions/runtime_053_254103898.py'
expected={r['id']:r for r in json.loads((ROOT/'results/checkpoints/runtime_053_254103898.benchmark.json').read_text())['results']}
metas=json.loads((ROOT/'cases/manifest.json').read_text())['cases']
result={'diagnostic_only':True,'solver_sha256':hashlib.sha256(solver.read_bytes()).hexdigest(),'results':[]}
dest=ROOT/'results/seven_parent_cache.json'
for meta in metas:
    data=(ROOT/meta['path']).read_bytes()
    case=parse_instance(data.decode())
    start=time.perf_counter()
    p=subprocess.run([sys.executable,'-I','-B',str(solver)],input=data,capture_output=True,timeout=20)
    assert p.returncode==0 and not p.stderr,(meta['id'],p.stderr)
    ops=validate_output(case,p.stdout)
    board,stamp=simulate(case,ops)
    matches=match_count(case,board)
    assert matches==expected[meta['id']]['matches'],meta['id']
    result['results'].append(dict(id=meta['id'],operations=ops,matches=matches,score=1000000*matches//case.n**2,board=board,stamp=stamp,runtime_sec=time.perf_counter()-start,input_sha256=hashlib.sha256(data).hexdigest(),output_sha256=hashlib.sha256(p.stdout).hexdigest()))
    dest.write_text(json.dumps(result)+'\n')
    if len(result['results'])%20==0:print('cached',len(result['results']),flush=True)
print('complete',sum(r['score'] for r in result['results']),flush=True)
