"""Regression checks for readiness failures that must block checkpoints."""

import tempfile
import unittest
from pathlib import Path

from tools.check_submission import check_submission, inspect_source, make_case, run_solver


class ReadinessTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="readiness-test-")
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "solver.py"
        self.instance = make_case(3, 2, 2, 1, 123)

    def solver(self, source):
        self.path.write_text(source, encoding="utf-8")
        return self.path

    def test_valid_report_has_checkpoint_metadata(self):
        self.solver("import sys\nsys.stdin.buffer.read()\nprint(0)\n")
        report = check_submission(self.path, random_count=2, timeout=2)
        self.assertTrue(report["passed"])
        self.assertEqual(report["cases_total"], 10)
        self.assertEqual(report["cases_passed"], 10)
        self.assertEqual(len(report["solver_sha256"]), 64)
        self.assertTrue(report["determinism"]["valid"])
        self.assertGreater(report["max_runtime_sec"], 0)
        self.assertEqual(report["transition_differential"]["status"], "not_run")

    def test_nonstandard_import_rejected_without_execution(self):
        self.solver("import unavailable_helper\ninput()\nprint(0)\n")
        report = check_submission(self.path, random_count=0)
        self.assertFalse(report["passed"])
        self.assertEqual(report["cases_total"], 0)
        self.assertTrue(report["static"]["errors"])

    def test_syntax_and_missing_stdin_rejected(self):
        for source in ("this is not valid Python!", "print(0)"):
            with self.subTest(source=source):
                self.assertFalse(inspect_source(self.solver(source))["valid"])

    def test_filesystem_access_flagged(self):
        result = inspect_source(self.solver("input()\nopen('data.txt').read()\nprint(0)\n"))
        self.assertFalse(result["valid"])
        self.assertTrue(result["review_flags"])

    def test_stdin_alias_allowed(self):
        result = inspect_source(self.solver("from sys import stdin as stream\nstream.read()\nprint(0)\n"))
        self.assertTrue(result["valid"])

    def test_bad_output_and_stderr_fail(self):
        bodies = [
            "print('0 extra')", "print('1 0 0 4')", "print('2 0 0 0 0 0 0')",
            "print('1 5 0 0')", "print(0); print('debug', file=sys.stderr)",
            "print('0 ' + ' ' * 100001)", "raise RuntimeError('crashed')",
        ]
        for body in bodies:
            with self.subTest(body=body):
                self.solver("import sys\nsys.stdin.read()\n" + body + "\n")
                row, _ = run_solver(self.path, self.instance, 2, self.directory.name)
                self.assertFalse(row["valid"])
                self.assertIn("error", row)

    def test_timeout_rejected(self):
        self.solver("import sys, time\nsys.stdin.read()\ntime.sleep(10)\nprint(0)\n")
        row, _ = run_solver(self.path, self.instance, 0.1, self.directory.name)
        self.assertFalse(row["valid"])
        self.assertIn("timeout", row["error"])

    def test_official_source_size_limit(self):
        result=inspect_source(self.solver("input()\nprint(0)\n#"+"x"*100000))
        self.assertFalse(result['valid'])
        self.assertTrue(any('100,000' in error for error in result['errors']))
        self.assertTrue(inspect_source(self.solver("input()\nprint(0)\n#"+"x"*99000))['valid'])

    def test_literal_wrapper_is_decoded_and_inspected(self):
        from tools.compact_submission import pack_source
        result=inspect_source(self.solver(pack_source('import sys\nsys.stdin.read()\nprint(0)\n')))
        self.assertTrue(result['valid'])
        self.assertTrue(result['packed_source']['decoded_sha256'])
        for body in ("import helper\ninput()\nprint(0)","input()\nopen('local.txt')\nprint(0)",
                     "input()\nexec('print(0)')"):
            self.assertFalse(inspect_source(self.solver(pack_source(body)))['valid'])
        modified=pack_source('input()\nprint(0)\n')+'print(123)\n'
        self.assertFalse(inspect_source(self.solver(modified))['valid'])


if __name__ == "__main__":
    unittest.main()
