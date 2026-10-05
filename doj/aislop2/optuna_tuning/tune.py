"""Continuous Optuna search; run --help for options. Ctrl+C stops, rerun resumes."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from optuna_tuning.evaluation import evaluate_source, export_source, load_cases, qualify
from optuna_tuning.sa_solver import DEFAULT_PARAMS, normalize_params


def atomic_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    temporary.replace(path)


@contextmanager
def run_lock(directory):
    """OS lock is released even after a crash. Do not delete this lock file."""
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / '.tuner.lock').open('a+b') as stream:
        stream.seek(0, 2)
        if stream.tell() == 0:
            stream.write(b'0')
            stream.flush()
        stream.seek(0)
        try:
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise ValueError('Another tuner is using this output directory.') from exc
        try:
            yield
        finally:
            stream.seek(0)
            if os.name == 'nt':
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=HERE / 'runs/default')
    parser.add_argument('--study', default='stamp-sa-v1')
    parser.add_argument('--manifest', type=Path, default=ROOT / 'cases/manifest.json')
    parser.add_argument('--suite', choices=('smoke', 'dev', 'stable'), default='dev')
    parser.add_argument('--limit', type=int, help='debug only; use all cases for real tuning')
    parser.add_argument('--trials', type=int, default=0, help='additional trials; 0 = keep running')
    parser.add_argument('--hours', type=float, default=0, help='stop starting trials after this many hours; 0 = unlimited')
    parser.add_argument('--seeds', default='0', help='fixed solver seeds, comma separated; e.g. 0,1,2')
    parser.add_argument('--sampler-seed', type=int, default=20260930)
    parser.add_argument('--iterations-min', type=int, default=500)
    parser.add_argument('--iterations-max', type=int, default=8000)
    parser.add_argument('--case-timeout', type=float, default=4.5, help='per-process seconds, <= official 5 seconds')
    parser.add_argument('--validate-every', type=int, default=10, help='qualify pending training best every N completed trials and on finite exit; 0 disables')
    parser.add_argument('--validate-only', action='store_true', help='qualify saved training best without new trials')
    parser.add_argument('--revalidate', action='store_true', help='repeat validation even when successful evidence exists')
    parser.add_argument('--no-prune', action='store_true', help='disable median pruning')
    args = parser.parse_args(argv)
    try:
        args.seeds = [int(value) for value in args.seeds.split(',')]
    except ValueError:
        parser.error('--seeds must be comma-separated integers')
    if len(set(args.seeds)) != len(args.seeds) or not args.seeds:
        parser.error('--seeds must be nonempty and distinct')
    if any(not 0 <= seed < 2**63 for seed in args.seeds):
        parser.error('--seeds must be in [0, 2**63)')
    if not 0 <= args.iterations_min <= args.iterations_max <= 20000:
        parser.error('need 0 <= iterations-min <= iterations-max <= 20000')
    if args.trials < 0 or not math.isfinite(args.hours) or args.hours < 0 or args.validate_every < 0:
        parser.error('trials, hours, and validate-every must be nonnegative')
    if not math.isfinite(args.case_timeout) or not 0 < args.case_timeout <= 5:
        parser.error('--case-timeout must be in (0, 5]')
    if args.limit is not None and args.limit < 1:
        parser.error('--limit must be positive')
    if not 0 <= args.sampler_seed < 2**32:
        parser.error('--sampler-seed must be in [0, 2**32)')
    args.output_dir = args.output_dir.resolve()
    args.manifest = args.manifest.resolve()
    return args


def configuration(args, cases, optuna_version):
    # Any change that could alter measured objectives starts a separate study.
    source_files = [HERE / name for name in ('sa_solver.py', 'evaluation.py', 'tune.py')]
    source_files += [ROOT / 'tools' / name for name in ('simulate.py', 'validate_output.py', 'benchmark.py',
                                                      'check_submission.py', 'compact_submission.py')]
    return {
        'version': 1, 'study': args.study, 'suite': args.suite,
        'manifest_sha256': hashlib.sha256(args.manifest.read_bytes()).hexdigest(),
        'cases': [(case['id'], case['sha256']) for case in cases],
        'sources': {path.relative_to(ROOT).as_posix(): hashlib.sha256(
                        args.solver_source if path == HERE / 'sa_solver.py' else path.read_bytes()).hexdigest()
                    for path in source_files},
        'seeds': args.seeds, 'sampler_seed': args.sampler_seed,
        'iterations_min': args.iterations_min, 'iterations_max': args.iterations_max,
        'case_timeout': args.case_timeout, 'pruning': not args.no_prune,
        'python': sys.version, 'python_executable': sys.executable,
        'platform': platform.platform(), 'optuna': optuna_version,
    }


def sample_params(trial, args):
    start = trial.suggest_float('start_temp', 0.15, 8.0, log=True)
    ratio = trial.suggest_float('cooling_ratio', 0.002, 0.5, log=True)
    return normalize_params({
        'iterations': trial.suggest_int('iterations', args.iterations_min, args.iterations_max),
        'start_temp': start, 'end_temp': start * ratio,
        # One weight is fixed: scaling all weights equally has no effect.
        'replace_weight': 4.0,
        'insert_weight': trial.suggest_float('insert_weight', 0.1, 8.0, log=True),
        'delete_weight': trial.suggest_float('delete_weight', 0.1, 8.0, log=True),
        'swap_weight': trial.suggest_float('swap_weight', 0.1, 8.0, log=True),
        'local_probability': trial.suggest_float('local_probability', 0.0, 1.0),
        'local_radius': trial.suggest_int('local_radius', 1, 5),
        'tail_bias': trial.suggest_float('tail_bias', 0.5, 5.0),
    })


class InvalidTrial(Exception):
    """An illegal answer or timeout disqualifies the whole parameter trial."""


def objective_function(args, cases, optuna):
    def objective(trial):
        params = sample_params(trial, args)
        trial.set_user_attr('solver_params', params)
        rows = []
        source_hashes = {}
        path = args.output_dir / 'trials' / f'trial_{trial.number:06d}.json'
        started = time.perf_counter()
        state = 'FAILED'
        error = None
        try:
            for seed in args.seeds:
                def on_case(row, index):
                    rows.append(dict(row, solver_seed=seed))
                    if not row['valid']:
                        raise InvalidTrial(f"{row['id']}: {row.get('error', 'invalid answer')}")
                    trial.report(sum(item['score'] for item in rows) / len(rows), len(rows)-1)
                    if not args.no_prune and trial.should_prune():
                        raise optuna.TrialPruned('unpromising partial mean')
                source = export_source(params, seed, template_source=args.solver_source)
                source_hashes[str(seed)] = hashlib.sha256(source).hexdigest()
                evaluate_source(source, cases, args.case_timeout, on_case=on_case)
            state = 'COMPLETE'
            value = sum(row['score'] for row in rows) / len(rows)
            trial.set_user_attr('max_runtime_sec', max(row['runtime_sec'] for row in rows))
            trial.set_user_attr('total_score', sum(row['score'] for row in rows))
            trial.set_user_attr('evaluations', len(rows))
            return value
        except optuna.TrialPruned:
            state = 'PRUNED'
            raise
        except (InvalidTrial, KeyboardInterrupt) as exc:
            error = str(exc) or 'interrupted'
            raise
        finally:
            atomic_json(path, {
                'trial': trial.number, 'state': state, 'params': params,
                'source_sha256_by_seed': source_hashes,
                'seeds': args.seeds, 'suite': args.suite,
                'evaluations': len(rows), 'total_score': sum(row['score'] for row in rows),
                'avg_score': sum(row['score'] for row in rows)/len(rows) if rows else None,
                'invalid': sum(not row['valid'] for row in rows), 'error': error,
                'wall_runtime_sec': time.perf_counter()-started, 'results': rows,
            })
    return objective


def export_best(study, args):
    try:
        trial = study.best_trial
    except ValueError:
        return None
    path = args.output_dir / 'best_params.json'
    previous = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    if previous.get('trial') == trial.number:
        return previous
    params = trial.user_attrs['solver_params']
    source = export_source(params, args.seeds[0], template_source=args.solver_source)
    temporary = args.output_dir / 'best_candidate.py.tmp'
    temporary.write_bytes(source)
    temporary.replace(args.output_dir / 'best_candidate.py')
    record = {
        'trial': trial.number, 'training_avg_score': trial.value,
        'training_total_score': trial.user_attrs['total_score'],
        'training_evaluations': trial.user_attrs['evaluations'],
        'suite': args.suite, 'solver_params': params, 'seeds': args.seeds,
        'export_seed': args.seeds[0], 'solver_sha256': hashlib.sha256(source).hexdigest(),
        'validation_status': 'training_only', 'candidate': 'best_candidate.py',
    }
    atomic_json(path, record)
    print(f"Training best #{trial.number}: mean={trial.value:.2f}; exported best_candidate.py", flush=True)
    return record


def validate_best(args, best):
    if best is None:
        raise ValueError('No completed trials to validate.')
    verified = args.output_dir / 'verified'
    baseline = normalize_params({'iterations': 0})

    def progress(row, index):
        if (index+1) % 40 == 0:
            print(f"  stable/repeat: {index+1} cases", flush=True)

    if not (verified / 'best.json').exists():
        print('Qualifying greedy baseline on stable320 before SA candidates...', flush=True)
        result = qualify(export_source(baseline, args.seeds[0], template_source=args.solver_source), args.manifest,
                         verified, 'Initial greedy baseline (SA iterations=0)',
                         timeout=args.case_timeout, on_progress=progress)
        if not result['passed']:
            raise ValueError('Greedy baseline qualification failed: ' + str(result.get('reason')))
    source = (args.output_dir / 'best_candidate.py').read_bytes()
    if hashlib.sha256(source).hexdigest() != best['solver_sha256']:
        raise ValueError('best_candidate.py changed after training; rerun export from the study')
    state_path = args.output_dir / 'last_validation.json'
    previous = json.loads(state_path.read_text(encoding='utf-8')) if state_path.exists() else {}
    if (previous.get('solver_sha256') == best['solver_sha256'] and previous.get('passed')
            and not args.revalidate):
        best['validation_status'] = 'passed'
        best['stable_evidence'] = 'last_validation.json'
        atomic_json(args.output_dir / 'best_params.json', best)
        print('This training best already has stable validation evidence.', flush=True)
        return previous
    print(f"Qualifying trial #{best['trial']} on stable320...", flush=True)
    result = qualify(source, args.manifest, verified, f"Optuna trial {best['trial']}",
                     timeout=args.case_timeout, on_progress=progress)
    record = {'trial': best['trial'], 'solver_sha256': best['solver_sha256'], **result}
    atomic_json(state_path, record)
    best['validation_status'] = 'passed' if result['passed'] else 'failed'
    best['stable_evidence'] = 'last_validation.json'
    atomic_json(args.output_dir / 'best_params.json', best)
    print(f"Stable validation: passed={result['passed']}, promoted={result['promoted']}", flush=True)
    return record


def run(args, optuna):
    cases = load_cases(args.manifest, args.suite, args.limit)
    args.solver_source = (HERE / 'sa_solver.py').read_bytes()
    signature = configuration(args, cases, optuna.__version__)
    # JSON converts tuples to lists; canonicalize before comparing stored data.
    signature = json.loads(json.dumps(signature))
    config_path = args.output_dir / 'configuration.json'
    if config_path.exists():
        if json.loads(config_path.read_text(encoding='utf-8')) != signature:
            raise ValueError('Study configuration changed (code/cases/seeds/runtime/search space). Use a NEW --output-dir.')
    elif (args.output_dir / 'study.db').exists():
        raise ValueError('Existing study.db has no configuration evidence. Use a NEW --output-dir.')
    else:
        atomic_json(config_path, signature)

    storage = optuna.storages.RDBStorage(
        url='sqlite:///' + (args.output_dir / 'study.db').as_posix(),
        engine_kwargs={'connect_args': {'timeout': 60}})
    pruner = (optuna.pruners.NopPruner() if args.no_prune else
              optuna.pruners.MedianPruner(n_startup_trials=8, n_warmup_steps=9, interval_steps=5))
    study = optuna.create_study(study_name=args.study, storage=storage,
                                direction='maximize', load_if_exists=True, pruner=pruner)
    digest = hashlib.sha256(json.dumps(signature, sort_keys=True).encode()).hexdigest()
    recorded = study.user_attrs.get('configuration_sha256')
    if recorded is not None and recorded != digest:
        raise ValueError('Database configuration does not match configuration.json.')
    study.set_user_attr('configuration_sha256', digest)
    # The directory lock proves no live owner is using this local SQLite study.
    for trial in study.get_trials(deepcopy=False):
        if trial.state == optuna.trial.TrialState.RUNNING:
            study.tell(trial.number, state=optuna.trial.TrialState.FAIL)
            print(f'Recovered interrupted trial #{trial.number} as FAIL.', flush=True)
    if not study.trials:
        defaults = DEFAULT_PARAMS.copy()
        defaults['iterations'] = min(args.iterations_max, max(args.iterations_min, defaults['iterations']))
        defaults['cooling_ratio'] = defaults.pop('end_temp')/defaults['start_temp']
        defaults.pop('replace_weight')
        study.enqueue_trial(defaults)

    best = export_best(study, args)
    if args.validate_only:
        result = validate_best(args, best)
        return 0 if result['passed'] else 1

    objective = objective_function(args, cases, optuna)
    deadline = time.monotonic() + args.hours*3600 if args.hours else math.inf
    attempts = 0
    interrupted = False
    print(f'{len(cases)} {args.suite} cases x {len(args.seeds)} seed(s); Ctrl+C stops and preserves completed trials.', flush=True)
    try:
        while (not args.trials or attempts < args.trials) and time.monotonic() < deadline:
            history = study.get_trials(deepcopy=False)
            waiting = [trial.number for trial in history if trial.state == optuna.trial.TrialState.WAITING]
            number = min(waiting) if waiting else max((trial.number for trial in history), default=-1)+1
            # A fresh deterministic sampler per trial avoids losing sampler RNG
            # state on restart. The completed database history still drives TPE.
            study.sampler = optuna.samplers.TPESampler(seed=(args.sampler_seed + number*104729) % 2**32)
            study.optimize(objective, n_trials=1, n_jobs=1, catch=(InvalidTrial,))
            attempts += 1
            trial = study.get_trials(deepcopy=False)[-1]
            print(f'Trial #{trial.number}: {trial.state.name}, mean={trial.value}', flush=True)
            csv_path = args.output_dir / 'trials.csv'
            new_file = not csv_path.exists()
            with csv_path.open('a', newline='', encoding='utf-8') as stream:
                writer = csv.writer(stream)
                if new_file:
                    writer.writerow(['trial', 'state', 'avg_score', 'max_runtime_sec', 'params'])
                writer.writerow([trial.number, trial.state.name, trial.value,
                                 trial.user_attrs.get('max_runtime_sec'), json.dumps(trial.params, sort_keys=True)])
            best = export_best(study, args)
            completed = sum(trial.state == optuna.trial.TrialState.COMPLETE for trial in study.get_trials(deepcopy=False))
            if args.validate_every and trial.state == optuna.trial.TrialState.COMPLETE and completed % args.validate_every == 0:
                validate_best(args, best)
    except KeyboardInterrupt:
        interrupted = True
        print('\nStopped. Rerun the same command to resume.', flush=True)
    if not interrupted and args.validate_every and best is not None:
        validate_best(args, best)
    if best:
        print(f"Best training mean: {best['training_avg_score']:.2f}; {args.output_dir / 'best_params.json'}", flush=True)
    else:
        print('No completed valid trials yet.', flush=True)
    return 0 if best is not None or interrupted else 1


def main(argv=None):
    args = parse_args(argv)
    try:
        import optuna
    except ImportError:
        print('Install dependencies: python -m pip install -r optuna_tuning/requirements.txt', file=sys.stderr)
        return 2
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    try:
        with run_lock(args.output_dir):
            return run(args, optuna)
    except (ValueError, OSError) as exc:
        print(f'error: {exc}', file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print('\nStopped; completed trials and checkpoints are preserved.', flush=True)
        return 0


if __name__ == '__main__':
    raise SystemExit(main())
