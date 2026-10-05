"""Checkpoint promotion must refuse stale, invalid, or incomparable evidence."""

import contextlib
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools import benchmark, checkpoint
from tools.check_submission import check_submission


class CheckpointTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="checkpoint-test-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        (self.root / "results").mkdir()
        self.solver = self.root / "solver.py"
        self.solver.write_text("import sys\nsys.stdin.read()\nprint(0)\n")
        self.digest = hashlib.sha256(self.solver.read_bytes()).hexdigest()
        self.benchmark_path = self.root / "benchmark.json"
        self.readiness_path = self.root / "readiness.json"
        self.benchmark = {
            "solver_sha256": self.digest, "manifest_sha256": "frozen-manifest", "suite": "stable",
            "timeout_sec": 5.0, "cases": 320, "invalid": 0,
            "total_score": 320 * 333333, "avg_score": 333333.0,
            "runtime_sec": 32.0, "max_runtime_sec": 0.1,
            "results": [dict(id=f"case_{i}", input_sha256=hashlib.sha256(str(i).encode()).hexdigest(),
                             output_sha256="fixed-output", valid=True, score=333333, runtime_sec=0.1,
                             matches=3, total_cells=9) for i in range(320)],
        }
        self.readiness = dict(passed=True, solver_sha256=self.digest, timeout_sec=5.0, max_runtime_sec=0.1)

    def promote(self):
        self.benchmark_path.write_text(json.dumps(self.benchmark))
        self.readiness_path.write_text(json.dumps(self.readiness))
        args = ["checkpoint.py", str(self.solver), str(self.benchmark_path), str(self.readiness_path),
                "--description", "regression fixture"]
        with patch.object(checkpoint, "ROOT", self.root), patch("sys.argv", args), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            checkpoint.main()

    def improve(self):
        self.benchmark["total_score"] = 320 * 444444
        self.benchmark["avg_score"] = 444444.0
        for row in self.benchmark["results"]:
            row.update(score=444444, matches=4)

    def assert_rejected(self):
        before = sorted(p.name for p in (self.root / "submissions").glob("*.py")) if (self.root / "submissions").exists() else []
        with self.assertRaises(SystemExit) as error:
            self.promote()
        self.assertNotEqual(error.exception.code, 0)
        after = sorted(p.name for p in (self.root / "submissions").glob("*.py")) if (self.root / "submissions").exists() else []
        self.assertEqual(after, before)

    def test_initial_and_strict_improvement_preserve_prior_bytes(self):
        self.promote()
        initial = self.root / "submissions/best_000_initial.py"
        before = initial.read_bytes()
        self.improve()
        self.promote()
        self.assertEqual(initial.read_bytes(), before)
        self.assertEqual(len(list((self.root / "submissions").glob("*.py"))), 2)
        best = json.loads((self.root / "results/best.json").read_text())
        self.assertTrue((self.root / best["benchmark"]).exists())
        self.assertNotEqual(Path(best["benchmark"]), self.benchmark_path)

    def test_tie_and_regression_refused(self):
        self.promote()
        self.assert_rejected()
        self.benchmark["total_score"] -= 1
        self.assert_rejected()

    def test_official_source_size_is_checked_at_promotion(self):
        self.solver.write_text('input()\nprint(0)\n#'+'x'*100000)
        digest=hashlib.sha256(self.solver.read_bytes()).hexdigest()
        self.benchmark['solver_sha256']=digest
        self.readiness['solver_sha256']=digest
        self.assert_rejected()

    def test_stale_solver_or_readiness_refused(self):
        self.benchmark["solver_sha256"] = "old-solver"
        self.assert_rejected()
        self.benchmark["solver_sha256"] = self.digest
        self.readiness["solver_sha256"] = "old-solver"
        self.assert_rejected()

    def test_changed_manifest_or_case_hash_refused(self):
        self.promote()
        self.improve()
        self.benchmark["manifest_sha256"] = "different-manifest"
        self.assert_rejected()
        self.benchmark["manifest_sha256"] = "frozen-manifest"
        self.benchmark["results"][0]["input_sha256"] = "different-case"
        self.assert_rejected()

    def test_duplicates_invalid_or_partial_results_refused(self):
        original = json.loads(json.dumps(self.benchmark))
        for mutation in (
            lambda data: data["results"].pop(),
            lambda data: data["results"][0].update(valid=False),
            lambda data: data["results"][0].update(id="case_1"),
            lambda data: data.update(total_score=data["total_score"] + 1),
        ):
            self.benchmark = json.loads(json.dumps(original))
            mutation(self.benchmark)
            self.assert_rejected()

    def test_official_runtime_limit_enforced(self):
        for evidence in (self.benchmark, self.readiness):
            for field in ("timeout_sec", "max_runtime_sec"):
                original = evidence[field]
                evidence[field] = 6.0
                self.assert_rejected()
                evidence[field] = original

    def test_existing_checkpoint_never_overwritten(self):
        (self.root / "submissions").mkdir()
        existing = self.root / "submissions/best_000_initial.py"
        existing.write_bytes(b"keep these bytes")
        with self.assertRaises((SystemExit, FileExistsError)):
            self.promote()
        self.assertEqual(existing.read_bytes(), b"keep these bytes")


class SnapshotTests(unittest.TestCase):
    def test_benchmark_uses_one_solver_snapshot_despite_concurrent_edits(self):
        with tempfile.TemporaryDirectory(prefix="snapshot-test-") as directory:
            root = Path(directory)
            (root / "results").mkdir()
            solver = root / "solver.py"
            initial = b"import sys\nsys.stdin.read()\nprint(0)\n"
            solver.write_bytes(initial)
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps({"cases": [dict(id=str(i), suites=["smoke"]) for i in range(2)]}))
            output = root / "results/report.json"

            def evaluate(snapshot, meta, timeout):
                solver.write_text("edited during benchmark")
                self.assertNotEqual(Path(snapshot), solver)
                self.assertEqual(Path(snapshot).read_bytes(), initial)
                return dict(id=meta["id"], n=3, d=2, c=2, k=1, family="test", valid=True,
                            score=1000000, matches=9, total_cells=9, runtime_sec=0.1,
                            input_sha256="same-input", output_sha256="same-output")

            args = ["benchmark.py", str(solver), "--manifest", str(manifest), "--output", str(output)]
            with patch.object(benchmark, "ROOT", root), patch.object(benchmark, "evaluate_case", side_effect=evaluate), patch("sys.argv", args), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(benchmark.main(), 0)
            report = json.loads(output.read_text())
            self.assertEqual(report["solver_sha256"], hashlib.sha256(initial).hexdigest())
            self.assertEqual(report["solver"], str(solver))
            self.assertEqual(len(report["result_sha256"]), 64)

    def test_readiness_uses_same_snapshot_for_every_case(self):
        with tempfile.TemporaryDirectory(prefix="readiness-snapshot-") as directory:
            solver = Path(directory) / "solver.py"
            initial = b"import sys\nsys.stdin.read()\nprint(0)\n"
            solver.write_bytes(initial)

            def run(snapshot, instance, timeout, cwd):
                solver.write_text("edited during readiness")
                self.assertEqual(Path(snapshot).read_bytes(), initial)
                return dict(valid=True, n=instance.n, runtime_sec=0.1), b"0\n"

            with patch("tools.check_submission.run_solver", side_effect=run):
                report = check_submission(solver, random_count=0)
            self.assertTrue(report["passed"])
            self.assertEqual(report["solver_sha256"], hashlib.sha256(initial).hexdigest())

    def test_benchmark_refuses_changed_frozen_case(self):
        with tempfile.TemporaryDirectory(prefix="frozen-case-") as directory:
            root = Path(directory)
            case = root / "case.in"
            case.write_text("3 2 2 1\n" + "0 " * 22)
            meta = dict(path=str(case), sha256="different-hash")
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                benchmark.evaluate_case(root / "unused.py", meta, 5, root)


if __name__ == "__main__":
    unittest.main()
