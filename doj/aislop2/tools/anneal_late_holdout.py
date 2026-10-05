"""Fixed-recipe small-board timing and late-beam coverage holdout.

Official timings use the unchanged candidate in a fresh subprocess. A second,
untimed diagnostic process wraps two functions without changing their results;
its output must exactly match the official run. It records attempted and
successful final repairs, including whether the third/fourth repair is used.
"""

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import statistics
import subprocess
import sys
import tempfile
import time

if __package__:
    from . import check_submission
    from .simulate import Instance, format_instance, match_count, parse_instance, simulate
else:
    import check_submission
    from simulate import Instance, format_instance, match_count, parse_instance, simulate


SEED = 925731041


def configurations():
    rows = []
    for n in range(5, 10):
        for variant, family in enumerate(('reachable', 'near_target')):
            rows.append(dict(id=f'{family}_n{n}', n=n, d=3,
                             c=3 if (n+variant)%2 else 6,
                             k=120 if (n+variant)%2 else 180,
                             family=family, seed=SEED+n*100+variant,
                             swaps=8*n+7 if variant == 0 else 0,
                             mutations=max(3, n*n//6) if variant else 0,
                             reserve=False))
    for n in (7, 8, 9):
        rows.append(dict(id=f'reserve_reachable_n{n}', n=n, d=3, c=6, k=180,
                         family='reachable', seed=SEED+10000+n,
                         swaps=120, mutations=0, reserve=True))
    return rows


def make_case(recipe):
    rng = random.Random(recipe['seed'])
    n, d, c, k = (recipe[key] for key in ('n', 'd', 'c', 'k'))
    a = [rng.randrange(c) for _ in range(n*n)]
    s = [rng.randrange(c) for _ in range(d*d)]
    t = a[:]
    inst = Instance(n, d, c, k, a, t, s)
    if recipe['family'] == 'reachable':
        operations = [(rng.randrange(n-d+1), rng.randrange(n-d+1), rng.randrange(4))
                      for _ in range(recipe['swaps'])]
        t, _ = simulate(inst, operations)
    else:
        for position in rng.sample(range(n*n), recipe['mutations']):
            t[position] = (a[position]+rng.randrange(1, c)) % c
    return Instance(n, d, c, k, a, t, s)


def probe(solver_path, instance):
    spec = importlib.util.spec_from_file_location('holdout_candidate', solver_path)
    solver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(solver)
    evidence = {'calls': [], 'reference': None}
    original_reference = solver.solve_without_late_beam
    original_finish = solver.late_beam_finish

    def reference(n, d, c, k, grid, target, stamp):
        operations = original_reference(n, d, c, k, grid, target, stamp)
        final, _ = simulate(Instance(n, d, c, k, grid[:], target, stamp[:]), operations)
        missing = n*n-sum(a == b for a, b in zip(final, target))
        evidence['reference'] = {'operations': len(operations), 'missing': missing,
                                 'spare_operations': k-len(operations),
                                 'eligible': 5 <= n <= 9 and d == 3 and
                                             len(operations) < k and 1 <= missing <= 8}
        return operations

    def finish(n, grid, target, stamp, k):
        before = sum(a == b for a, b in zip(grid, target))
        row = {'remaining_operations': k, 'initial_matches': before,
               'missing': n*n-before,
               'color_bound': solver.color_bound(grid+stamp, target)}
        started = time.perf_counter()
        tail = original_finish(n, grid, target, stamp, k)
        row['diagnostic_runtime_sec'] = time.perf_counter()-started
        row['returned_operations'] = None if tail is None else len(tail)
        row['successful_repair'] = tail is not None
        if tail is not None:
            width = n-2
            operations = [(aid//4//width, aid//4%width, aid%4) for aid in tail]
            final, _ = simulate(Instance(n, 3, instance.c, k, grid[:], target, stamp[:]), operations)
            row['final_matches'] = sum(a == b for a, b in zip(final, target))
            assert row['final_matches'] > before
        evidence['calls'].append(row)
        return tail

    solver.solve_without_late_beam = reference
    solver.late_beam_finish = finish
    operations = solver.solve(instance.n, instance.d, instance.c, instance.k,
                              instance.a[:], instance.t, instance.s[:])
    output = str(len(operations))+'\n'+''.join(f'{x} {y} {r}\n' for x, y, r in operations)
    evidence.update(normalized_output_sha256=hashlib.sha256(output.encode('ascii')).hexdigest(),
                    attempted_repairs=len(evidence['calls']),
                    successful_repairs=sum(row['successful_repair'] for row in evidence['calls']))
    return evidence


def run(path, output_path, timeout):
    source = path.resolve().read_bytes()
    recipes = configurations()
    inputs = [(recipe, make_case(recipe)) for recipe in recipes]
    manifest = [dict(recipe, input_sha256=hashlib.sha256(format_instance(inst).encode('ascii')).hexdigest())
                for recipe, inst in inputs]
    report = dict(kind='small_board_late_beam_runtime_holdout', version=1, seed=SEED,
                  solver=str(path.resolve()), solver_sha256=hashlib.sha256(source).hexdigest(),
                  generator=str(Path(__file__).resolve()),
                  generator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  python=sys.version, jobs=1, timeout_sec=timeout,
                  timing_scope='unchanged fresh subprocess; shared machine load, not isolated stress',
                  recipe_manifest=manifest,
                  extension_rule='Run the three predeclared reserve recipes only if no initial case has two successful late repairs.',
                  cases=[])
    with tempfile.TemporaryDirectory(prefix='stamp-late-holdout-') as cwd:
        snapshot = Path(cwd)/path.name
        snapshot.write_bytes(source)
        report['static'] = check_submission.inspect_source(snapshot)
        assert report['static']['valid'], report['static']
        run_reserves = None
        for index, (recipe, inst) in enumerate(inputs):
            if index == 10:
                run_reserves = not any(row.get('diagnostic', {}).get('successful_repairs', 0) >= 2
                                       for row in report['cases'])
            if recipe['reserve'] and not run_reserves:
                continue
            row, output = check_submission.run_solver(snapshot, inst, timeout, cwd)
            row.update(manifest[index])
            row['canonical_valid'] = row['valid']
            row['output_sha256'] = hashlib.sha256(output).hexdigest()
            row['normalized_output_sha256'] = hashlib.sha256(output.replace(b'\r\n', b'\n')).hexdigest()
            try:
                result = subprocess.run([sys.executable, str(Path(__file__).resolve()),
                                         str(snapshot), '--probe'],
                                        input=format_instance(inst).encode('ascii'), capture_output=True,
                                        timeout=max(10, 2*timeout), cwd=cwd, check=True)
                diagnostic = json.loads(result.stdout)
                row['diagnostic'] = diagnostic
                row['diagnostic_output_parity'] = diagnostic['normalized_output_sha256'] == row['normalized_output_sha256']
                if not row['diagnostic_output_parity']:
                    row['valid'] = False
                    row['error'] = 'Diagnostic wrapper changed solver output.'
            except (subprocess.SubprocessError, ValueError) as exc:
                row['diagnostic_error'] = str(exc)
                row['valid'] = False
            report['cases'].append(row)
            print(f"{recipe['id']}: valid={row['valid']} time={row['runtime_sec']:.3f}s "
                  f"repairs={row.get('diagnostic', {}).get('successful_repairs', '?')}", flush=True)
            output_path.write_text(json.dumps(report, indent=2)+'\n')
    rows = report['cases']
    report.update(valid=all(row['valid'] for row in rows), cases_total=len(rows),
                  cases_passed=sum(row['valid'] for row in rows),
                  total_score=sum(row.get('score', 0) for row in rows),
                  max_runtime_sec=max(row['runtime_sec'] for row in rows),
                  avg_runtime_sec=statistics.mean(row['runtime_sec'] for row in rows),
                  branch_executed_cases=sum(row.get('diagnostic', {}).get('attempted_repairs', 0) > 0 for row in rows),
                  multiple_repair_cases=sum(row.get('diagnostic', {}).get('successful_repairs', 0) >= 2 for row in rows),
                  beyond_old_cap_cases=sum(row.get('diagnostic', {}).get('successful_repairs', 0) >= 3 for row in rows))
    output_path.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: report[key] for key in ('valid', 'cases_total', 'cases_passed',
          'max_runtime_sec', 'avg_runtime_sec', 'branch_executed_cases', 'multiple_repair_cases',
          'beyond_old_cap_cases')}))
    return report['valid']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('solver', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--timeout', type=float, default=5)
    parser.add_argument('--probe', action='store_true')
    args = parser.parse_args()
    if args.probe:
        print(json.dumps(probe(args.solver, parse_instance(sys.stdin.read()))))
        return 0
    if args.output is None:
        parser.error('--output is required')
    return 0 if run(args.solver, args.output, args.timeout) else 1


if __name__ == '__main__':
    raise SystemExit(main())
