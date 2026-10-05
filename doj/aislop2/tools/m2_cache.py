"""Cache checkpoint055 operations, reusing only identical verified stdout hashes."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.simulate import parse_instance, simulate, match_count
from tools.validate_output import validate_output

solver = ROOT / 'submissions/runtime_055_254652429.py'
expected = {r['id']: r for r in json.loads((ROOT / 'results/checkpoints/runtime_055_254652429.benchmark.json').read_text())['results']}
old = {r['id']: r for r in json.loads((ROOT / 'results/seven_parent_cache.json').read_text())['results']}
out = ROOT / 'results/m2_parent_cache.json'
rows = []
for meta in json.loads((ROOT / 'cases/manifest.json').read_text())['cases']:
    want = expected[meta['id']]
    previous = old.get(meta['id'])
    if previous and previous['output_sha256'] == want['output_sha256']:
        rows.append(previous)
    else:
        data = (ROOT / meta['path']).read_bytes()
        ins = parse_instance(data.decode())
        start = time.perf_counter()
        p = subprocess.run([sys.executable, '-I', '-B', str(solver)], input=data, capture_output=True, timeout=30)
        assert not p.returncode and not p.stderr
        operations = validate_output(ins, p.stdout)
        board, stamp = simulate(ins, operations)
        matches = match_count(ins, board)
        digest = hashlib.sha256(p.stdout).hexdigest()
        assert matches == want['matches'] and digest == want['output_sha256'], meta['id']
        rows.append(dict(id=meta['id'], operations=operations, matches=matches, score=1000000*matches//ins.n**2,
                         board=board, stamp=stamp, runtime_sec=time.perf_counter()-start,
                         input_sha256=hashlib.sha256(data).hexdigest(), output_sha256=digest))
        print(meta['id'], 'cached', flush=True)
    out.write_text(json.dumps(dict(diagnostic_only=True, solver_sha256=hashlib.sha256(solver.read_bytes()).hexdigest(), results=rows))+'\n')
print('complete', len(rows), sum(r['score'] for r in rows), flush=True)
