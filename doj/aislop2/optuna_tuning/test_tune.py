"""Integration checks for durable tuning, using real Optuna and subprocesses."""
import importlib.util
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'optuna_tuning/tune.py'


@contextmanager
def opened_study(directory):
    import optuna
    storage = optuna.storages.RDBStorage(
        'sqlite:///' + (Path(directory) / 'study.db').as_posix())
    try:
        yield optuna.load_study(study_name='stamp-sa-v1', storage=storage)
    finally:
        storage.remove_session()
        storage.engine.dispose()


@unittest.skipUnless(importlib.util.find_spec('optuna'), 'install optuna_tuning/requirements.txt')
class TuningIntegrationTests(unittest.TestCase):
    def run_tuner(self, directory, *extra):
        return subprocess.run(
            [sys.executable, str(SCRIPT), '--output-dir', str(directory),
             '--suite', 'smoke', '--limit', '1', '--iterations-min', '10',
             '--iterations-max', '10', '--trials', '1', '--validate-every', '0',
             *extra], capture_output=True, text=True, timeout=60, cwd=ROOT)

    def test_resume_retains_trials_and_exports_standalone_candidate(self):
        with tempfile.TemporaryDirectory() as directory:
            first = self.run_tuner(directory)
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            second = self.run_tuner(directory)
            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
            import optuna
            with opened_study(directory) as study:
                completed = [t for t in study.trials if t.state == optuna.trial.TrialState.COMPLETE]
                self.assertEqual(len(completed), 2)
            best = json.loads((Path(directory) / 'best_params.json').read_text())
            self.assertEqual(best['validation_status'], 'training_only')
            source = Path(directory) / 'best_candidate.py'
            self.assertTrue(source.is_file())
            from tools.simulate import parse_instance
            from tools.validate_output import validate_output
            data = (ROOT / 'cases/generated/case_000.in').read_bytes()
            run = subprocess.run([sys.executable, '-I', str(source)], input=data,
                                 capture_output=True, timeout=5, cwd=directory)
            self.assertEqual(run.returncode, 0, run.stderr)
            validate_output(parse_instance(data.decode()), run.stdout)
            self.assertFalse((Path(directory) / 'verified/best.json').exists())

    def test_resume_rejects_changed_evaluation_conditions(self):
        with tempfile.TemporaryDirectory() as directory:
            first = self.run_tuner(directory)
            self.assertEqual(first.returncode, 0, first.stderr)
            changed = self.run_tuner(directory, '--seeds', '99')
            self.assertNotEqual(changed.returncode, 0)
            self.assertIn('configuration', changed.stderr.lower())

    def test_bad_ranges_are_rejected_before_creating_a_study(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_tuner(directory, '--iterations-min', '20')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('iterations-min', result.stderr)
            self.assertFalse((Path(directory) / 'study.db').exists())

    def test_sampler_reproduces_across_resume(self):
        import optuna
        with tempfile.TemporaryDirectory() as whole, tempfile.TemporaryDirectory() as split:
            continuous = self.run_tuner(whole, '--trials', '3')
            self.assertEqual(continuous.returncode, 0, continuous.stderr)
            for _ in range(3):
                resumed = self.run_tuner(split)
                self.assertEqual(resumed.returncode, 0, resumed.stderr)
            def trials(directory):
                with opened_study(directory) as study:
                    return [(t.params, t.value) for t in study.trials]
            self.assertEqual(trials(whole), trials(split))

    def test_crashed_trial_is_failed_and_tuning_continues(self):
        import optuna
        with tempfile.TemporaryDirectory() as directory:
            first = self.run_tuner(directory)
            self.assertEqual(first.returncode, 0, first.stderr)
            with opened_study(directory) as study:
                abandoned = study.ask()
            resumed = self.run_tuner(directory)
            self.assertEqual(resumed.returncode, 0, resumed.stderr)
            with opened_study(directory) as study:
                self.assertEqual(study.trials[abandoned.number].state, optuna.trial.TrialState.FAIL)
                self.assertEqual(study.trials[-1].state, optuna.trial.TrialState.COMPLETE)


class ValidationRecoveryTests(unittest.TestCase):
    def fixture(self, directory, passed):
        from optuna_tuning import tune
        args = tune.parse_args(['--output-dir', directory])
        args.solver_source = (ROOT / 'optuna_tuning/sa_solver.py').read_bytes()
        source = b'import sys\nsys.stdin.read()\nprint(0)\n'
        best = {'trial': 1, 'solver_sha256': hashlib.sha256(source).hexdigest(),
                'validation_status': 'training_only'}
        (args.output_dir / 'best_candidate.py').write_bytes(source)
        verified = args.output_dir / 'verified'
        verified.mkdir()
        (verified / 'best.json').write_text('{}')
        tune.atomic_json(args.output_dir / 'best_params.json', best)
        tune.atomic_json(args.output_dir / 'last_validation.json',
                         {'solver_sha256': best['solver_sha256'], 'passed': passed})
        return tune, args, best

    def test_cached_validation_recovers_metadata_after_interruption(self):
        with tempfile.TemporaryDirectory() as directory:
            tune, args, best = self.fixture(directory, True)
            tune.validate_best(args, best)
            record = json.loads((args.output_dir / 'best_params.json').read_text())
            self.assertEqual(record['validation_status'], 'passed')

    def test_transient_validation_failure_can_retry(self):
        with tempfile.TemporaryDirectory() as directory:
            tune, args, best = self.fixture(directory, False)
            # Expensive full qualification is exercised by test_evaluation.
            # Here its success verifies recovery instead of cached failure.
            with patch.object(tune, 'qualify', return_value={'passed': True, 'promoted': False}):
                result = tune.validate_best(args, best)
            self.assertTrue(result['passed'])
            self.assertEqual(json.loads((args.output_dir / 'best_params.json').read_text())[
                'validation_status'], 'passed')


if __name__ == '__main__':
    unittest.main()
