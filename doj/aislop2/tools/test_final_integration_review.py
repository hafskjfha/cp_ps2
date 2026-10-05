"""Lightweight independent checks of the four ordinary-Python final variants."""
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

PARENT = ROOT / "submissions/best_039_251862073.py"
VARIANTS = ("b3", "b12", "b30", "cycles")
NEW_NAMES = {"route_patterns", "route_tail", "cancel_inverse_pairs", "best_insertion", "deletion_deltas", "temporal_repair"}
MEASUREMENTS = {}


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class IntegrationReview(unittest.TestCase):
    def test_exact_parent_preservation_and_dense_ast_mapping(self):
        parent_tree = ast.parse(PARENT.read_text())
        parent_names = {node.name for node in parent_tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
        self.assertFalse(NEW_NAMES & parent_names)
        rows = []
        for variant in VARIANTS:
            source_path = ROOT / f"solvers/experiments/algebra39_{variant}_source.py"
            submitted_path = ROOT / f"solvers/experiments/algebra39_{variant}.py"
            source = ast.parse(source_path.read_text())
            submitted = ast.parse(submitted_path.read_text())
            self.assertEqual(ast.dump(source), ast.dump(submitted), variant)
            names = [node.name for node in source.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))]
            self.assertEqual(len(names), len(set(names)), variant)
            self.assertEqual(set(names), parent_names | NEW_NAMES | {"solve_route_parent"}, variant)
            restored = copy.deepcopy(source)
            restored.body = [node for node in restored.body
                             if not (isinstance(node, ast.FunctionDef) and node.name in NEW_NAMES | {"solve"})]
            # The appended routing fragment contains one documentation expression.
            restored.body = [node for node in restored.body
                             if not (isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant)
                                     and node.value.value == "Exact parallel scoring of sparse routing permutations at every legal anchor.")]
            for node in restored.body:
                if isinstance(node, ast.FunctionDef) and node.name == "solve_route_parent":
                    node.name = "solve"
            self.assertEqual(ast.dump(restored), ast.dump(parent_tree), variant)
            main = next(node for node in source.body if isinstance(node, ast.FunctionDef) and node.name == "main")
            self.assertEqual(sum(isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "solve"
                                 for node in ast.walk(main)), 1)
            checked = inspect_source(submitted_path)
            self.assertTrue(checked["valid"], checked)
            self.assertLessEqual(checked["source_bytes"], 100000)
            self.assertNotIn("packed_source", checked)
            rows.append(dict(variant=variant, source_sha256=hashlib.sha256(source_path.read_bytes()).hexdigest(), **checked))
        MEASUREMENTS["artifacts"] = rows

    def test_integration_replays_each_stage_preserving_budget_and_score_floor(self):
        rng = random.Random(580462)
        rows = []
        for variant in VARIANTS:
            module = load(ROOT / f"solvers/experiments/algebra39_{variant}_source.py", "final_review_" + variant)
            original_temporal = module.temporal_repair
            original_tail = module.route_tail
            for n, d, c, k in ((3, 2, 2, 1), (3, 3, 6, 2), (4, 3, 6, 15), (4, 2, 3, 24)):
                grid, target, stamp = [[rng.randrange(c) for _ in range(size)] for size in (n * n, n * n, d * d)]
                operations = [(x, y, r) for x in range(n - d + 1) for y in range(n - d + 1) for r in range(4)]
                reference = [rng.choice(operations) for _ in range(min(k, 9))]
                if k >= 15:
                    reference[3:3] = [reference[0], reference[0]]
                case = Instance(n, d, c, k, grid, target, stamp)
                parent_state = simulate(case, reference)
                parent_score = match_count(case, parent_state[0])
                tracked = dict(sequence=reference[:], state=parent_state, calls=[])

                def temporal(*args, **kwargs):
                    self.assertEqual(args[0:3], (n, d, k))
                    self.assertEqual(args[3], grid + stamp)
                    result = original_temporal(*args, **kwargs)
                    replay = [operations[index] for index in result]
                    tracked["sequence"] = replay
                    tracked["state"] = simulate(case, replay)
                    self.assertGreaterEqual(match_count(case, tracked["state"][0]), parent_score)
                    return result

                def tail(nn, dd, board, wanted, buffer, remaining, powers, cap):
                    self.assertEqual((nn, dd), (n, d))
                    self.assertEqual((board, buffer), tracked["state"])
                    self.assertEqual(remaining, k - len(tracked["sequence"]))
                    self.assertGreaterEqual(remaining, 0)
                    previous_score = match_count(case, board)
                    result = original_tail(nn, dd, board, wanted, buffer, remaining, powers, cap)
                    if remaining < 2 * min(powers):
                        self.assertEqual(result, [])
                    tracked["sequence"].extend(result)
                    tracked["state"] = simulate(case, tracked["sequence"])
                    self.assertLessEqual(len(tracked["sequence"]), k)
                    self.assertGreaterEqual(match_count(case, tracked["state"][0]), previous_score)
                    tracked["calls"].append(dict(powers=powers, cap=cap, remaining=remaining, added=len(result)))
                    return result

                with patch.object(module, "solve_route_parent", return_value=reference), \
                     patch.object(module, "temporal_repair", side_effect=temporal), \
                     patch.object(module, "route_tail", side_effect=tail):
                    answer = module.solve(n, d, c, k, grid, target, stamp)
                self.assertEqual(answer, tracked["sequence"])
                final_grid, _ = simulate(case, answer)
                self.assertGreaterEqual(match_count(case, final_grid), parent_score)
                self.assertLessEqual(len(answer), k)
                rows.append(dict(variant=variant, n=n, d=d, c=c, k=k, parent_score=parent_score,
                                 final_score=match_count(case, final_grid), operations=len(answer), route_calls=tracked["calls"]))
        MEASUREMENTS["instrumented_wrapper_cases"] = rows


if __name__ == "__main__":
    started = time.perf_counter()
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__]))
    report = dict(passed=result.wasSuccessful(), tests_run=result.testsRun, runtime_sec=time.perf_counter() - started,
                  failures=[dict(test=str(test), traceback=trace) for test, trace in result.failures + result.errors], measurements=MEASUREMENTS)
    (ROOT / "results/final_integration_review.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf8")
    raise SystemExit(not result.wasSuccessful())
