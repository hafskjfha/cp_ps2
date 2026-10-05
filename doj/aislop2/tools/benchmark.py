"""Run a frozen suite: python tools/benchmark.py solvers/current.py --suite stable."""
import argparse
import hashlib
import json
import statistics
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.simulate import parse_instance, simulate, match_count
from tools.validate_output import validate_output


def evaluate_case(solver, meta, timeout, root=ROOT):
    path = root / meta['path']
    data = path.read_bytes()
    if 'sha256' in meta and hashlib.sha256(data).hexdigest() != meta['sha256']:
        raise ValueError('Frozen testcase hash mismatch: ' + str(path))
    instance = parse_instance(data.decode('ascii'))
    result = {key: meta[key] for key in ('id', 'family', 'n', 'd', 'c', 'k')}
    result.update(valid=False, score=0, matches=0, total_cells=instance.n**2,
                  input_sha256=hashlib.sha256(data).hexdigest())
    started = time.perf_counter()
    try:
        process = subprocess.run([sys.executable, '-I', '-B', str(Path(solver).resolve())],
                                 input=data, capture_output=True, timeout=timeout)
        result['runtime_sec'] = time.perf_counter() - started
        if process.returncode:
            raise ValueError('exit code %s: %s' % (process.returncode, process.stderr[:500].decode(errors='replace')))
        operations = validate_output(instance, process.stdout)
        grid, _ = simulate(instance, operations)
        matches = match_count(instance, grid)
        result.update(valid=True, matches=matches, score=1000000*matches//(instance.n**2),
                      operations=len(operations), output_bytes=len(process.stdout),
                      output_sha256=hashlib.sha256(process.stdout).hexdigest())
        if process.stderr:
            result['stderr'] = process.stderr[:500].decode(errors='replace')
    except subprocess.TimeoutExpired:
        result.update(error='timeout', runtime_sec=time.perf_counter()-started)
    except ValueError as exc:
        result.update(error=str(exc), runtime_sec=time.perf_counter()-started)
    return result


def summarize(rows):
    times = [row['runtime_sec'] for row in rows]
    return dict(cases=len(rows), total_score=sum(row['score'] for row in rows),
                avg_score=sum(row['score'] for row in rows)/max(1, len(rows)),
                invalid=sum(not row['valid'] for row in rows),
                runtime_sec=sum(times), avg_runtime_sec=statistics.mean(times) if times else 0,
                max_runtime_sec=max(times, default=0))


def breakdown(rows):
    result = {}
    for field in ('d', 'c', 'n_bucket', 'k_bucket', 'family'):
        groups = {}
        for row in rows:
            if field == 'n_bucket':
                key = '3-9' if row['n'] < 10 else '10-19' if row['n'] < 20 else '20-30'
            elif field == 'k_bucket':
                key = '1-10' if row['k'] <= 10 else '11-60' if row['k'] <= 60 else '61-180'
            else:
                key = str(row[field])
            groups.setdefault(key, []).append(row)
        result[field] = {key: summarize(group) for key, group in sorted(groups.items())}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('solver', type=Path)
    parser.add_argument('--manifest', type=Path, default=ROOT/'cases/manifest.json')
    parser.add_argument('--suite', choices=['smoke', 'dev', 'stable'], default='smoke')
    parser.add_argument('--timeout', type=float, default=5.0)
    parser.add_argument('--jobs', type=int, default=1)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--limit', type=int)
    args = parser.parse_args()
    if args.jobs < 1 or args.timeout <= 0:
        parser.error('jobs and timeout must be positive')
    manifest_data = args.manifest.read_bytes()
    manifest = json.loads(manifest_data)
    cases = [c for c in manifest['cases'] if args.suite in c['suites']]
    if args.limit is not None:
        cases = cases[:args.limit]
    if not cases:
        parser.error('selected suite is empty')
    # All cases execute the exact same bytes, even if an experiment is edited
    # while a benchmark is running. Checkpoint promotion checks this digest.
    solver_data = args.solver.read_bytes()
    solver_digest = hashlib.sha256(solver_data).hexdigest()
    started = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix='stamp-benchmark-') as directory:
        snapshot = Path(directory) / args.solver.name
        snapshot.write_bytes(solver_data)
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            rows = list(pool.map(lambda c: evaluate_case(snapshot, c, args.timeout), cases))
    result = dict(solver=str(args.solver), solver_sha256=solver_digest,
                  manifest_sha256=hashlib.sha256(manifest_data).hexdigest(), suite=args.suite,
                  timeout_sec=args.timeout, jobs=args.jobs, python=sys.version,
                  wall_runtime_sec=time.perf_counter()-started, **summarize(rows),
                  breakdown=breakdown(rows), results=rows)
    fingerprints = [(row['id'], row['input_sha256'], row.get('output_sha256'), row['score']) for row in rows]
    result['result_sha256'] = hashlib.sha256(json.dumps(fingerprints, separators=(',', ':')).encode()).hexdigest()
    output = args.output or ROOT/'results'/('%s_%s.json' % (args.solver.stem, args.suite))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    (ROOT/'results/latest.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print('%s %s: total=%d avg=%.2f invalid=%d/%d runtime=%.3fs max=%.3fs wall=%.3fs' %
          (args.solver.name, args.suite, result['total_score'], result['avg_score'], result['invalid'],
           result['cases'], result['runtime_sec'], result['max_runtime_sec'], result['wall_runtime_sec']))
    print('family: ' + ', '.join('%s=%.1f' % (k,v['avg_score']) for k,v in result['breakdown']['family'].items()))
    print('saved', output)
    return 1 if result['invalid'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
