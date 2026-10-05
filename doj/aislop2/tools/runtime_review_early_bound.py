"""Independent proof-oriented checks of the early global-optimum shortcut."""
import ast
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import sys
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.check_submission import inspect_source
from tools.simulate import Instance, match_count, simulate

PATH = ROOT / "solvers/experiments/runtime_route_early_bound.py"
BASE = ROOT / "submissions/best_049_252862932.py"
MEASUREMENTS = {}


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class EarlyBoundReview(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.new = load(PATH, "review_early_bound_new")
        cls.old = load(BASE, "review_early_bound_old")

    def test_only_proven_early_guard_changes_original_ast(self):
        old = ast.parse(BASE.read_text())
        new = ast.parse(PATH.read_text())
        helper = next(node for node in new.body if isinstance(node, ast.FunctionDef) and node.name == "runtime_early_bound")
        new.body.remove(helper)
        changed = next(node for node in new.body if isinstance(node, ast.FunctionDef) and node.name == "solve_without_hot_restart")
        added_guard = changed.body.pop(1)
        self.assertIsInstance(added_guard, ast.If)
        self.assertIn("runtime_early_bound", ast.unparse(added_guard))
        self.assertEqual(ast.dump(new), ast.dump(old))
        MEASUREMENTS["source_sha256"] = hashlib.sha256(PATH.read_bytes()).hexdigest()
        MEASUREMENTS["static"] = inspect_source(PATH)
        self.assertTrue(MEASUREMENTS["static"]["valid"])

    def test_actual_early_success_is_legal_and_reaches_conserved_inventory_bound(self):
        rng = random.Random(104245)
        successful = 0
        for n in range(5, 10):
            patterns = self.new.route_patterns(n, 3, (3,))
            for _ in range(3):
                pattern = rng.choice(patterns)
                dx, dy, r, s, backward, count, _ = pattern
                x, y = 0, max(0, -dy)
                left, right = (x, y, r), (x + dx, y + dy, s)
                operations = ([right, left] if backward else [left, right]) * count
                grid = [rng.randrange(6) for _ in range(n * n)]
                stamp = [rng.randrange(6) for _ in range(9)]
                initial = Instance(n, 3, 6, 12, grid, grid, stamp)
                target = simulate(initial, operations)[0]
                reference = [(0, 0, 0), (0, 0, 0)]
                saved = (grid[:], target[:], stamp[:], reference[:])
                answer = self.new.runtime_early_bound(n, 3, 12, grid, target, stamp, reference)
                self.assertIsNotNone(answer)
                case = Instance(n, 3, 6, 12, grid, target, stamp)
                final, _ = simulate(case, answer)
                self.assertEqual(match_count(case, final), self.new.color_bound(grid + stamp, target))
                self.assertEqual((grid, target, stamp, reference), saved)
                successful += 1
        # Exact optimum can be below N^2 because missing target colors cannot be
        # created by swaps. Such a certificate must still allow early return.
        n = 9
        grid, stamp, target = [0] * 81, [0] * 9, [0] * 78 + [1] * 3
        result = self.new.runtime_early_bound(n, 3, 20, grid, target, stamp, [])
        self.assertEqual(result, [])
        self.assertEqual(self.new.color_bound(grid + stamp, target), 78)
        MEASUREMENTS["canonical_early_success"] = dict(reachable_targets=successful, deficient_inventory_score=78)

    def test_failure_and_budget_guards_preserve_inputs_and_random_state(self):
        rng = random.Random(757611)
        failed = 0
        for n in (5, 7, 9):
            for k in (1, 5, 6, 18):
                grid = [rng.randrange(6) for _ in range(n * n)]
                target = [rng.randrange(6) for _ in range(n * n)]
                stamp = [rng.randrange(6) for _ in range(9)]
                reference = []
                saved = (grid[:], target[:], stamp[:], reference[:])
                random_state = random.getstate()
                answer = self.new.runtime_early_bound(n, 3, k, grid, target, stamp, reference)
                self.assertEqual((grid, target, stamp, reference), saved)
                self.assertEqual(random.getstate(), random_state)
                if answer is None:
                    failed += 1
                else:
                    case = Instance(n, 3, 6, k, grid, target, stamp)
                    self.assertEqual(match_count(case, simulate(case, answer)[0]), self.new.color_bound(grid + stamp, target))
        self.assertGreater(failed, 0)
        MEASUREMENTS["failed_probe_purity"] = dict(cases=12, failed_probes=failed)

    def test_failed_probe_resumes_exact_old_branch_and_success_skips_beam(self):
        rng = random.Random(771862)
        for n, d in ((4, 3), (5, 3), (9, 3), (10, 3), (7, 2)):
            grid = [rng.randrange(3) for _ in range(n * n)]
            target = grid[:]
            target[-1] = (target[-1] + 1) % 3
            stamp = [rng.randrange(3) for _ in range(d * d)]
            reference = []
            outputs = []
            for solver in (self.old, self.new):
                with patch.object(solver, "solve_without_late_beam", return_value=reference), \
                     patch.object(solver, "late_beam_finish", return_value=None) as beam:
                    if solver is self.new:
                        with patch.object(solver, "runtime_early_bound", return_value=None) as shortcut:
                            outputs.append(solver.solve_without_hot_restart(n, d, 3, 12, grid, target, stamp))
                            self.assertEqual(shortcut.call_count, int(5 <= n <= 9 and d == 3))
                    else:
                        outputs.append(solver.solve_without_hot_restart(n, d, 3, 12, grid, target, stamp))
            self.assertEqual(outputs[0], outputs[1])
        grid, stamp, target = [0] * 81, [0] * 9, [0] * 78 + [1] * 3
        with patch.object(self.new, "solve_without_late_beam", return_value=[]), \
             patch.object(self.new, "late_beam_finish", side_effect=AssertionError("Beam ran after proved optimum")):
            self.assertEqual(self.new.solve_without_hot_restart(9, 3, 2, 90, grid, target, stamp), [])
        MEASUREMENTS["guard_integration"] = dict(fallback_parity_fixtures=5, exact_optimum_skips_beam=True)


if __name__ == "__main__":
    started = time.perf_counter()
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__]))
    report = dict(passed=result.wasSuccessful(), tests_run=result.testsRun, runtime_sec=time.perf_counter() - started,
                  failures=[dict(test=str(test), traceback=trace) for test, trace in result.failures + result.errors], measurements=MEASUREMENTS)
    (ROOT / "results/runtime_review_early_bound.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf8")
    raise SystemExit(not result.wasSuccessful())
