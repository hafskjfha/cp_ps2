"""Tests for frozen evaluation and immutable local checkpoint promotion."""

import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from tools.simulate import Instance, format_instance


ZERO = b"import sys\nsys.stdin.buffer.read()\nprint(0)\n"


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        from optuna_tuning import evaluation
        self.evaluation = evaluation
        self.temp = tempfile.TemporaryDirectory(prefix="optuna-evaluation-test-")
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.instance = Instance(3, 2, 2, 1, [0] * 9, [0] * 9, [1] * 4)
        case = self.directory / "case.in"
        case.write_text(format_instance(self.instance), encoding="ascii")
        self.meta = dict(id="one", family="uniform", n=3, d=2, c=2, k=1,
                         path=str(case), suites=["smoke", "dev", "stable"],
                         sha256=hashlib.sha256(case.read_bytes()).hexdigest())
        self.manifest = self.directory / "manifest.json"
        self.write_manifest([self.meta])

    def write_manifest(self, cases):
        self.manifest.write_text(json.dumps({"cases": cases,
                                            "suite_counts": {"stable": len(cases)}}), encoding="utf-8")

    def test_manifest_rejects_modified_case_even_outside_limited_prefix(self):
        bad = dict(self.meta, id="two", sha256="0" * 64)
        self.write_manifest([self.meta, bad])
        with self.assertRaisesRegex(ValueError, "hash"):
            self.evaluation.load_cases(self.manifest, "stable", limit=1)

    def test_manifest_rejects_duplicates_empty_and_nonpositive_limit(self):
        self.write_manifest([self.meta, self.meta])
        with self.assertRaisesRegex(ValueError, "[Dd]uplicate"):
            self.evaluation.load_cases(self.manifest, "stable")
        self.write_manifest([self.meta])
        with self.assertRaises(ValueError):
            self.evaluation.load_cases(self.manifest, "missing")
        with self.assertRaises(ValueError):
            self.evaluation.load_cases(self.manifest, "stable", limit=0)

    def test_manifest_checks_dimensions_against_instance(self):
        self.write_manifest([dict(self.meta, n=30)])
        with self.assertRaisesRegex(ValueError, "metadata"):
            self.evaluation.load_cases(self.manifest, "stable")

    def test_real_subprocess_scores_valid_output_without_global_artifacts(self):
        rows_seen = []
        latest = self.evaluation.ROOT / "results/latest.json"
        before = latest.read_bytes() if latest.exists() else None
        report = self.evaluation.evaluate_source(
            ZERO, self.evaluation.load_cases(self.manifest, "stable"),
            on_case=lambda row, index: rows_seen.append((row["score"], index)))
        self.assertEqual(report["total_score"], 1_000_000)
        self.assertEqual(report["invalid"], 0)
        self.assertEqual(report["solver_sha256"], hashlib.sha256(ZERO).hexdigest())
        self.assertEqual(rows_seen, [(1_000_000, 0)])
        self.assertEqual(latest.read_bytes() if latest.exists() else None, before)

    def test_invalid_output_and_timeout_are_not_valid_scores(self):
        cases = self.evaluation.load_cases(self.manifest, "stable")
        for source, timeout in [(b"print('0 extra')\n", 2.0),
                                (b"import time\ntime.sleep(2)\nprint(0)\n", 0.05)]:
            with self.subTest(source=source):
                report = self.evaluation.evaluate_source(source, cases, timeout=timeout)
                self.assertEqual(report["invalid"], 1)
                self.assertEqual(report["total_score"], 0)
                self.assertIn("error", report["results"][0])

    def test_debug_output_is_rejected(self):
        source = ZERO + b"sys.stderr.write('debug')\n"
        report = self.evaluation.evaluate_source(source, [self.meta])
        self.assertEqual(report["invalid"], 1)

    def test_callback_can_abort_and_temporary_snapshot_is_cleaned(self):
        class Abort(Exception):
            pass
        def abort(row, index):
            raise Abort()
        with self.assertRaises(Abort):
            self.evaluation.evaluate_source(ZERO, [self.meta], on_case=abort)

    def test_export_only_changes_top_level_configuration(self):
        template = self.directory / "template.py"
        template.write_text("import sys\nDEFAULT_PARAMS = {'iterations': 7}\nDEFAULT_SEED = 0\n"
                            "def local():\n    DEFAULT_SEED = 99\n    return DEFAULT_SEED\n"
                            "sys.stdin.buffer.read()\nprint(0)\n", encoding="utf-8")
        with patch.object(self.evaluation, "SOLVER_PATH", template):
            source = self.evaluation.export_source({"iterations": 0}, seed=17)
        tree = ast.parse(source)
        values = {node.targets[0].id: ast.literal_eval(node.value)
                  for node in tree.body if isinstance(node, ast.Assign)}
        self.assertEqual(values["DEFAULT_PARAMS"]["iterations"], 0)
        self.assertEqual(values["DEFAULT_SEED"], 17)
        local = next(node for node in tree.body if isinstance(node, ast.FunctionDef))
        self.assertEqual(ast.literal_eval(local.body[0].value), 99)
        self.assertEqual(self.evaluation.evaluate_source(source, [self.meta])["invalid"], 0)

    def test_export_rejects_missing_or_ambiguous_defaults(self):
        template = self.directory / "template.py"
        for text in ["DEFAULT_PARAMS = {}\n", "DEFAULT_PARAMS = {}\nDEFAULT_SEED = 0\nDEFAULT_SEED = 1\n"]:
            template.write_text(text, encoding="utf-8")
            with patch.object(self.evaluation, "SOLVER_PATH", template):
                with self.assertRaises(ValueError):
                    self.evaluation.export_source({})

    def test_frozen_template_survives_edits_during_a_run(self):
        frozen = self.evaluation.SOLVER_PATH.read_bytes()
        first = self.evaluation.export_source({'iterations': 10}, template_source=frozen)
        changed = self.directory / 'changed.py'
        changed.write_text('raise RuntimeError("edited during tuning")\n', encoding='utf-8')
        with patch.object(self.evaluation, 'SOLVER_PATH', changed):
            second = self.evaluation.export_source({'iterations': 10}, template_source=frozen)
        self.assertEqual(first, second)
        self.assertEqual(self.evaluation.evaluate_source(second, [self.meta])['invalid'], 0)

    def test_real_export_is_self_contained_and_reproducible(self):
        source = self.evaluation.export_source({"iterations": 20}, seed=19)
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.Import):
                self.assertNotIn("optuna", [item.name for item in node.names])
            if isinstance(node, ast.ImportFrom):
                self.assertEqual(node.level, 0)
                self.assertFalse((node.module or "").startswith(("tools", "optuna_tuning")))
        one = self.evaluation.evaluate_source(source, [self.meta])
        two = self.evaluation.evaluate_source(source, [self.meta])
        self.assertEqual(one["invalid"], 0)
        self.assertEqual(one["result_sha256"], two["result_sha256"])

    def test_strict_improvement_preserves_initial_checkpoint(self):
        self.instance.t[:2] = [1, 1]
        self.instance.t[3:5] = [1, 1]
        case = Path(self.meta["path"])
        case.write_text(format_instance(self.instance), encoding="ascii")
        self.meta["sha256"] = hashlib.sha256(case.read_bytes()).hexdigest()
        self.write_manifest([self.meta])
        out = self.directory / "improving"
        initial = self.evaluation.qualify(ZERO, self.manifest, out, readiness_random_count=0)
        initial_path = Path(initial["checkpoint"])
        better = b"import sys\nsys.stdin.buffer.read()\nprint('1\\n0 0 0')\n"
        improved = self.evaluation.qualify(better, self.manifest, out, readiness_random_count=0)
        self.assertTrue(improved["promoted"])
        self.assertEqual(improved["benchmark"]["total_score"], 1_000_000)
        self.assertEqual(improved["reproduction"]["total_score"], 1_000_000)
        self.assertEqual(initial_path.read_bytes(), ZERO)
        self.assertNotEqual(initial_path, Path(improved["checkpoint"]))
        self.assertEqual(len((out / "history.csv").read_text().splitlines()), 3)

    def test_qualification_saves_initial_once_then_keeps_score_ties(self):
        out = self.directory / "run"
        first = self.evaluation.qualify(ZERO, self.manifest, out, "initial", readiness_random_count=0)
        self.assertTrue(first["passed"])
        self.assertTrue(first["promoted"])
        checkpoint = Path(first["checkpoint"])
        self.assertEqual(checkpoint.read_bytes(), ZERO)
        self.assertTrue((out / "history.csv").is_file())
        second = self.evaluation.qualify(ZERO, self.manifest, out, readiness_random_count=0)
        self.assertTrue(second["passed"])
        self.assertFalse(second["promoted"])
        self.assertEqual(len(list((out / "checkpoints").glob("*.py"))), 1)
        self.assertEqual(checkpoint.read_bytes(), ZERO)
        self.write_manifest([dict(self.meta, family="renamed")])
        with self.assertRaisesRegex(ValueError, "manifest"):
            self.evaluation.qualify(ZERO, self.manifest, out, readiness_random_count=0)

    def test_qualification_lock_rejects_contention_then_allows_reacquisition(self):
        with self.evaluation._qualification_lock(self.directory):
            with self.assertRaisesRegex(ValueError, "already running"):
                with self.evaluation._qualification_lock(self.directory):
                    self.fail("Two qualifications acquired one lock")
        self.assertTrue((self.directory / ".qualification.lock").is_file())
        with self.evaluation._qualification_lock(self.directory):
            pass

    def test_killed_qualification_worker_releases_lock(self):
        child = ("from pathlib import Path\nimport sys, time\n"
                 "from optuna_tuning.evaluation import _qualification_lock\n"
                 "with _qualification_lock(Path(sys.argv[1])):\n"
                 "    print('ready', flush=True)\n    time.sleep(60)\n")
        process = subprocess.Popen([sys.executable, "-c", child, str(self.directory)],
                                   cwd=self.evaluation.ROOT, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, text=True)
        try:
            self.assertEqual(process.stdout.readline().strip(), "ready")
            with self.assertRaises(ValueError):
                with self.evaluation._qualification_lock(self.directory):
                    self.fail("Concurrent process acquired held lock")
        finally:
            process.kill()
            process.communicate(timeout=5)
        with self.evaluation._qualification_lock(self.directory):
            pass

    def test_qualification_rejects_oversized_source_before_evaluation(self):
        observed = []
        with self.assertRaisesRegex(ValueError, "100,000"):
            self.evaluation.qualify(ZERO + b"#" * 100_000, self.manifest,
                                    self.directory / "oversized",
                                    on_progress=lambda row, index: observed.append(row))
        self.assertEqual(observed, [])


if __name__ == "__main__":
    unittest.main()
