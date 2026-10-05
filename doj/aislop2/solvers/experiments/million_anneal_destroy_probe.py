import json
import runpy
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.simulate import parse_instance, simulate, match_count
from tools.validate_output import validate_output

m = runpy.run_path(str(ROOT / 'submissions/best_052_252937025.py'))
g = runpy.run_path(str(ROOT / 'solvers/experiments/million_anneal_fragment.py'))
source = ROOT / 'results/million_parent_cache.json'
if not source.exists():
    source = ROOT / 'results/session_parent_dev_cache.json'
cache = json.loads(source.read_text())
if 'results' in cache:
    cache['cases'] = cache.pop('results')
    for row in cache['cases']:
        row['path'] = 'cases/generated/' + row['id'] + '.in'
proposals = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
temperature = float(sys.argv[2]) if len(sys.argv) > 2 else 0.45
limit = int(sys.argv[3]) if len(sys.argv) > 3 else 100
rows = []
for row in cache['cases'][:limit]:
    inst = parse_instance((ROOT / row['path']).read_text())
    n, d, c, k = inst.n, inst.d, inst.c, inst.k
    indices, _, ops, _, _ = m['build'](n, d, inst.t)
    side = n - d + 1
    sequence = [(x * side + y) * 4 + r for x, y, r in row['operations']]
    start = time.perf_counter()
    candidate = g['destroy_rebuild'](n, d, c, k, inst.a + inst.s, inst.t, indices, sequence, m['refine'], list(zip(indices, ops)), trials=proposals, passes=3, temperature=temperature)
    elapsed = time.perf_counter() - start
    operations = [ops[a] for a in candidate]
    output = str(len(operations)) + '\n' + '\n'.join(' '.join(map(str, a)) for a in operations) + '\n'
    validate_output(inst, output.encode())
    matches = match_count(inst, simulate(inst, operations)[0])
    parent = row['matches']
    assert matches >= parent
    delta = 1000000 * matches // (n * n) - 1000000 * parent // (n * n)
    item = dict(id=row['id'], n=n, d=d, k=k, matches=matches, parent=parent, delta=delta,
                runtime_sec=elapsed, operations=operations)
    rows.append(item)
    if delta or elapsed > 1.5:
        print(row['id'], delta, round(elapsed, 3), flush=True)
summary = dict(proposals=proposals, temperature=temperature, parent_cache=str(source),
               total_delta=sum(r['delta'] for r in rows), wins=sum(r['delta'] > 0 for r in rows),
               max_runtime_sec=max(r['runtime_sec'] for r in rows),
               total_runtime_sec=sum(r['runtime_sec'] for r in rows), cases=rows)
out = ROOT / ('results/million_anneal_destroy_%d_%d_%d.json' % (proposals, int(temperature * 100), limit))
out.write_text(json.dumps(summary))
print({k: v for k, v in summary.items() if k != 'cases'}, flush=True)
