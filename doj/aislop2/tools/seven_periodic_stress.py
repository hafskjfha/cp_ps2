"""Run frozen periodic holdouts sequentially through the canonical readiness runner.

Use --dry-run to verify only generated input hashes and gate metadata, without
starting a solver. This independent holdout never changes the benchmark suite.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.check_submission import inspect_source, run_solver
from tools.simulate import Instance, format_instance, parse_instance


def make_periodic(meta):
    n, d, c, k = (meta[key] for key in ('n', 'd', 'c', 'k'))
    rng = random.Random(meta['seed'])
    grid = [rng.randrange(c) for _ in range(n*n)]
    stamp = [rng.randrange(c)]*(d*d) if meta['repeated_stamp'] else [rng.randrange(c) for _ in range(d*d)]
    palette = list(range(c))
    rng.shuffle(palette)
    family = meta['family']
    target = []
    for row in range(n):
        for col in range(n):
            value = {'diagonal': row+col, 'horizontal': row, 'vertical': col,
                     'blocks': row//2+col//2, 'tile': (row%2)*3+col%3}[family]
            target.append(palette[value % c])
    return Instance(n, d, c, k, grid, target, stamp)


def describe(meta, instance):
    n, d, c = instance.n, instance.d, instance.c
    patterns = {tuple(instance.t[(x+i)*n+y+j] for i in range(d) for j in range(d))
                for x in range(n-d+1) for y in range(n-d+1)}
    initial = instance.a + instance.s
    bound = sum(min(initial.count(v), instance.t.count(v)) for v in range(c))
    matches = sum(a == b for a, b in zip(instance.a, instance.t))
    return dict(id=meta['id'], family=meta['family'], seed=meta['seed'],
                repeated_stamp=meta['repeated_stamp'], initial_matches=matches,
                color_bound=bound, target_patch_patterns=len(patterns),
                gate_active=n >= 10 and instance.k >= 12 and 100*matches < 88*bound and len(patterns) <= 4*c,
                input_sha256=hashlib.sha256(format_instance(instance).encode('ascii')).hexdigest())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('solver', type=Path, nargs='?', default=ROOT/'solvers/experiments/seven_reverse_integrated.py')
    parser.add_argument('--config', type=Path, default=ROOT/'results/seven_periodic_stress_config.json')
    parser.add_argument('--output', type=Path, default=ROOT/'results/seven_periodic_stress.json')
    parser.add_argument('--timeout', type=float, default=5.0)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--stop-on-failure', action='store_true')
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error('--timeout must be positive')
    frozen = args.config.read_bytes()
    config = json.loads(frozen)
    cases = []
    for meta in config['cases']:
        instance = make_periodic(meta)
        parse_instance(format_instance(instance))
        info = describe(meta, instance)
        if info['input_sha256'] != meta['input_sha256']:
            raise ValueError('Frozen input hash mismatch: ' + meta['id'])
        if not info['gate_active']:
            raise ValueError('Holdout unexpectedly misses reverse gate: ' + meta['id'])
        cases.append((meta, instance, info))
    if args.dry_run:
        print('Verified', len(cases), 'frozen periodic inputs; all enter the reverse-constructor gate; no solver runs.')
        return 0
    solver = args.solver.resolve()
    static = inspect_source(solver)
    if not static['valid']:
        raise ValueError('Submission source rejected: ' + json.dumps(static))
    data = solver.read_bytes()
    if hashlib.sha256(data).hexdigest() != static['sha256']:
        raise ValueError('Solver changed during source inspection.')
    report = dict(solver=str(solver), solver_sha256=static['sha256'], static=static,
                  config_sha256=hashlib.sha256(frozen).hexdigest(), python=sys.version,
                  timeout_sec=args.timeout, jobs=1, cases_total=len(cases), results=[])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='stamp-periodic-stress-') as directory:
        snapshot = Path(directory)/solver.name
        snapshot.write_bytes(data)
        for meta, instance, info in cases:
            row, output = run_solver(snapshot, instance, args.timeout, directory)
            row.update(info)
            row['output_sha256'] = hashlib.sha256(output).hexdigest()
            report['results'].append(row)
            report.update(cases_run=len(report['results']),
                          cases_passed=sum(r['valid'] for r in report['results']),
                          max_runtime_sec=max(r['runtime_sec'] for r in report['results']),
                          total_runtime_sec=sum(r['runtime_sec'] for r in report['results']))
            report['valid'] = report['cases_run'] == len(cases) and report['cases_passed'] == len(cases)
            args.output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf8')
            print(meta['id'], 'PASS' if row['valid'] else 'FAIL',
                  round(row['runtime_sec'], 3), row.get('matches'), row.get('error', ''), flush=True)
            if not row['valid'] and args.stop_on_failure:
                break
    print('PASS' if report['valid'] else 'FAIL', report['cases_passed'], '/', len(cases),
          'max', round(report['max_runtime_sec'], 3), 'seconds', flush=True)
    return 0 if report['valid'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
