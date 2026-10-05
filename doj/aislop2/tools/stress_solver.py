"""Sequential max-size runtime holdout, separate from the frozen scoring suite.

Usage: python tools/stress_solver.py solvers/current.py --timeout 5 \
    --output results/stress_current.json

All 36 cases have N=30 and K=180. Random cases cover both D values, every C,
and two fixed seeds; four structured families cover both D and extreme C.
Timings include process startup, output capture, and wait overhead. The p95
uses the nearest-rank definition. Run without other solver workers for useful
wall-time comparisons; this tool intentionally has no parallel-worker option.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import statistics
import sys
import tempfile
import time

if __package__:
    from . import check_submission
    from .simulate import format_instance
else:
    import check_submission
    from simulate import format_instance


VERSION = 1
BASE_SEED = 916273451


def configurations() -> list[dict]:
    """Return deterministic holdout recipes; do not select using solver results."""
    configs = []
    for d in (2, 3):
        for c in range(2, 7):
            for replicate in range(2):
                configs.append(dict(id=f'random_d{d}_c{c}_s{replicate}', n=30,
                                    d=d, c=c, k=180, family='random',
                                    seed=BASE_SEED+d*10000+c*100+replicate))
    for family_index, family in enumerate(('pattern', 'close', 'uniform', 'reachable')):
        for d in (2, 3):
            for c in (2, 6):
                configs.append(dict(id=f'{family}_d{d}_c{c}', n=30, d=d, c=c,
                                    k=180, family=family,
                                    seed=BASE_SEED+100000+family_index*10000+d*100+c))
    return configs


def summarize(rows: list[dict]) -> dict:
    times = sorted(row['runtime_sec'] for row in rows)
    return {
        'cases_total': len(rows),
        'cases_passed': sum(row['valid'] for row in rows),
        'invalid': sum(not row['valid'] for row in rows),
        'total_runtime_sec': sum(times),
        'avg_runtime_sec': statistics.mean(times) if times else 0.0,
        'p95_runtime_sec': times[math.ceil(len(times)*0.95)-1] if times else 0.0,
        'max_runtime_sec': times[-1] if times else 0.0,
        'total_score': sum(row.get('score', 0) for row in rows),
    }


def stress_solver(path: Path, timeout: float = 5.0) -> dict:
    """Run one immutable solver snapshot sequentially using bounded capture."""
    started = time.perf_counter()
    path = path.resolve()
    solver_data = path.read_bytes()
    generator_path = Path(check_submission.__file__).resolve()
    configs = configurations()
    cases = []
    for config in configs:
        instance = check_submission.make_case(config['n'], config['d'], config['c'],
                                              config['k'], config['seed'], config['family'])
        data = format_instance(instance).encode('ascii')
        metadata = dict(config, input_sha256=hashlib.sha256(data).hexdigest())
        cases.append((metadata, instance))
    manifest = [metadata for metadata, _ in cases]
    report = {
        'kind': 'sequential_maximum_size_runtime_holdout', 'version': VERSION,
        'solver': str(path), 'solver_sha256': hashlib.sha256(solver_data).hexdigest(),
        'python': sys.version, 'timeout_sec': timeout, 'jobs': 1,
        'generator': str(generator_path),
        'generator_sha256': hashlib.sha256(generator_path.read_bytes()).hexdigest(),
        'stress_tool_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'suite_sha256': hashlib.sha256(json.dumps(manifest, sort_keys=True,
                                                 separators=(',', ':')).encode('ascii')).hexdigest(),
        'percentile_method': 'nearest rank',
        'timing_scope': 'isolated sequential subprocess wall time, including startup and capture',
        'cases': [],
    }
    with tempfile.TemporaryDirectory(prefix='stamp-runtime-holdout-') as isolated_cwd:
        snapshot = Path(isolated_cwd) / path.name
        snapshot.write_bytes(solver_data)
        report['static'] = check_submission.inspect_source(snapshot)
        if report['static']['valid']:
            for metadata, instance in cases:
                row, output = check_submission.run_solver(snapshot, instance, timeout, isolated_cwd)
                row.update(metadata)
                row['output_sha256'] = hashlib.sha256(output).hexdigest()
                report['cases'].append(row)
    report.update(summarize(report['cases']))
    report['expected_cases'] = len(cases)
    report['valid'] = (report['static']['valid'] and report['cases_total'] == len(cases)
                       and report['invalid'] == 0)
    report['passed'] = report['valid']
    report['wall_runtime_sec'] = time.perf_counter() - started
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('solver', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--timeout', type=float, default=5.0)
    args = parser.parse_args()
    if not math.isfinite(args.timeout) or args.timeout <= 0:
        parser.error('--timeout must be a positive finite number')
    try:
        report = stress_solver(args.solver, args.timeout)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    except (OSError, ValueError) as exc:
        parser.exit(2, f'error: {exc}\n')
    print(f"{'PASS' if report['valid'] else 'FAIL'}: {report['cases_passed']}/{report['expected_cases']} "
          f"max-size cases; max {report['max_runtime_sec']:.3f}s; "
          f"p95 {report['p95_runtime_sec']:.3f}s; avg {report['avg_runtime_sec']:.3f}s")
    for error in report['static']['errors'] + report['static']['review_flags']:
        print(f'  {error}')
    for row in report['cases']:
        if not row['valid']:
            print(f"  {row['id']}: {row['error']}")
    print(f'Saved {args.output}')
    return 0 if report['valid'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
