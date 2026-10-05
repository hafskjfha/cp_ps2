"""Independent canonical oracles for the final wildcard-join submission."""
import ast
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import random
import sys
import time
import tokenize
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.check_submission import inspect_source
from tools.compact_submission import compact_source, decode_literal_wrapper
from tools.simulate import Instance, match_count, rotation_offsets, simulate

FINAL = ROOT / "solvers/experiments/regret_wildcard_final_source.py"
SOURCE = FINAL if FINAL.exists() else ROOT / "solvers/experiments/regret_wildcard_modern_source.py"
PACKED = SOURCE.with_name(SOURCE.stem.removesuffix("_source") + ".py")
MEASUREMENTS = {"source": str(SOURCE)}


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical_operations():
    return [(x, y, r) for x in range(2) for y in range(2) for r in range(4)]


class WildcardReview(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.solver = load(SOURCE, "review_wildcard")
        cls.operations = canonical_operations()

    @staticmethod
    def pack(values):
        return sum(value << (3 * index) for index, value in enumerate(values))

    def oracle(self, grid, target, stamp, k):
        """Tuple-state BFS using canonical rotation offsets, no packed helper."""
        if grid == target:
            return True
        initial = tuple(grid + stamp)
        visited, frontier = {initial}, [initial]
        contacts = [[(x + p) * 4 + y + q for p, q in rotation_offsets(3, r)]
                    for x, y, r in self.operations]
        for _ in range(k):
            next_layer = []
            for state in frontier:
                for action in contacts:
                    child = list(state)
                    for j, position in enumerate(action):
                        child[16 + j], child[position] = child[position], child[16 + j]
                    child = tuple(child)
                    if child in visited:
                        continue
                    if list(child[:16]) == target:
                        return True
                    visited.add(child)
                    next_layer.append(child)
            frontier = next_layer
        return False

    def test_generic_small_budgets_match_independent_exhaustive_bfs(self):
        rng = random.Random(933772)
        cases = 0
        for c in range(2, 7):
            for k in range(4):
                for reachable in (False, True):
                    grid = [rng.randrange(c) for _ in range(16)]
                    stamp = [rng.randrange(c) for _ in range(9)]
                    target = [rng.randrange(c) for _ in range(16)]
                    if reachable:
                        fixture = Instance(4, 3, c, max(1, k), grid, grid, stamp)
                        target = simulate(fixture, [rng.choice(self.operations) for _ in range(k)])[0]
                    expected = self.oracle(grid, target, stamp, k)
                    answer = self.solver.wildcard_finish(grid, target, stamp, k)
                    self.assertEqual(answer is not None, expected, (c, k, reachable))
                    if answer is not None:
                        self.assertLessEqual(len(answer), k)
                        case = Instance(4, 3, c, max(1, k), grid, target, stamp)
                        self.assertEqual(simulate(case, [self.operations[i] for i in answer])[0], target)
                    cases += 1
        MEASUREMENTS["independent_bfs"] = dict(cases=cases, colors=[2, 3, 4, 5, 6], budgets=[0, 1, 2, 3])

    def test_backward_wildcards_trace_canonical_constraints(self):
        rng = random.Random(747201)
        target = [rng.randrange(6) for _ in range(16)]
        symbolic = Instance(4, 3, 8, 180, target, target, [7] * 9)
        records = self.solver.wildcard_backward_records(self.solver.packed_transitions(), self.pack(target))
        count = 0
        for depth, path, encoded in itertools.islice(records, 240):
            wishes_grid, wishes_stamp = simulate(symbolic, [self.operations[i] for i in path])
            wishes = wishes_grid + wishes_stamp
            self.assertEqual(depth, len(path))
            self.assertEqual(list(encoded), [position * 6 + value for position, value in enumerate(wishes) if value != 7])
            self.assertEqual(len(encoded), 16)
            values = [rng.randrange(6) if value == 7 else value for value in wishes]
            fixture = Instance(4, 3, 6, 180, values[:16], target, values[16:])
            reversed_operations = [self.operations[i] for i in path[::-1]]
            self.assertEqual(simulate(fixture, reversed_operations)[0], target)
            constrained = encoded[count % len(encoded)] // 6
            values[constrained] = (values[constrained] + 1) % 6
            wrong = Instance(4, 3, 6, 180, values[:16], target, values[16:])
            self.assertNotEqual(simulate(wrong, reversed_operations)[0], target)
            count += 1
        self.assertEqual(count, 240)
        MEASUREMENTS["backward_constraints"] = dict(records=count, successful_and_violated_witnesses=2 * count)

    def test_meeting_depths_and_cache_reuse_keep_budget_and_target(self):
        rng = random.Random(893004)
        cases = 0
        for budget in (5, 6, 7, 8):
            c = 2 if budget % 2 else 6
            grid = [rng.randrange(c) for _ in range(16)]
            stamp = [rng.randrange(c) for _ in range(9)]
            base = Instance(4, 3, c, budget, grid, grid, stamp)
            witness = [rng.choice(self.operations) for _ in range(budget)]
            target = simulate(base, witness)[0]
            answer = self.solver.wildcard_finish(grid, target, stamp, budget)
            self.assertIsNotNone(answer)
            self.assertLessEqual(len(answer), budget)
            self.assertEqual(simulate(base, [self.operations[i] for i in answer])[0], target)
            # Reusing a partially populated target cache must remain safe with a
            # shorter cap, and later restoration of the full cap.
            small = self.solver.wildcard_finish(grid, target, stamp, 1, depth=1)
            if small is not None:
                self.assertLessEqual(len(small), 1)
                self.assertEqual(simulate(base, [self.operations[i] for i in small])[0], target)
            self.assertEqual(self.solver.wildcard_finish(grid, target, stamp, budget), answer)
            cases += 1
        self.assertIsNone(self.solver.wildcard_finish([0] * 16, [5] * 16, [5] * 9, 180))
        self.assertEqual(self.solver.wildcard_finish([0] * 16, [0] * 16, [5] * 9, 0), [])
        MEASUREMENTS["meeting_cache_inventory"] = dict(reachable_budgets=[5, 6, 7, 8], fixtures=cases, inventory_rejected=True)

    def test_suffix_trials_use_available_budget_and_preserve_parent_floor(self):
        rng = random.Random(731588)
        grid = [rng.randrange(6) for _ in range(16)]
        stamp = [rng.randrange(6) for _ in range(9)]
        reference = [rng.choice(self.operations) for _ in range(10)]
        true_tail = [rng.choice(self.operations) for _ in range(3)]
        baseline = Instance(4, 3, 6, 12, grid, grid, stamp)
        target = simulate(baseline, reference[:6] + true_tail)[0]
        case = Instance(4, 3, 6, 12, grid, target, stamp)
        lengths = list(dict.fromkeys(max(0, len(reference) - remove) for remove in (0, 2, 4, 8, 12)))
        calls = []

        def none_tail(board, wanted, buffer, remaining):
            length = lengths[len(calls)]
            expected = simulate(case, reference[:length])
            self.assertEqual((board, buffer), expected)
            self.assertEqual(remaining, 12 - length)
            calls.append((length, remaining))
            return None

        with patch.object(self.solver, "solve_without_regret_wildcard", return_value=reference), \
             patch.object(self.solver, "wildcard_finish", side_effect=none_tail):
            answer = self.solver.solve(4, 3, 6, 12, grid, target, stamp)
        self.assertEqual(answer, reference)
        self.assertEqual([length for length, _ in calls], lengths)
        calls.clear()

        def successful_tail(board, wanted, buffer, remaining):
            none_tail(board, wanted, buffer, remaining)
            return [self.operations.index(op) for op in true_tail] if len(calls) == 3 else None

        with patch.object(self.solver, "solve_without_regret_wildcard", return_value=reference), \
             patch.object(self.solver, "wildcard_finish", side_effect=successful_tail):
            answer = self.solver.solve(4, 3, 6, 12, grid, target, stamp)
        self.assertEqual(answer, reference[:6] + true_tail)
        self.assertLessEqual(len(answer), 12)
        self.assertEqual(simulate(case, answer)[0], target)
        self.assertGreaterEqual(match_count(case, simulate(case, answer)[0]), match_count(case, simulate(case, reference)[0]))
        MEASUREMENTS["suffix_budget"] = dict(tried_lengths=lengths, later_cut_success_length=len(answer), parent_floor_preserved=True)

    def test_apply_and_escape_consolidation_preserve_core_fields(self):
        old = load(ROOT / "submissions/best_027_251280679.py", "review_old27")
        rng = random.Random(945700)
        transitions = 0
        for n, d, c in ((3, 2, 2), (3, 3, 6), (5, 2, 6), (7, 3, 2), (9, 3, 6)):
            grid = [rng.randrange(c) for _ in range(n * n)]
            target = [rng.randrange(c) for _ in range(n * n)]
            stamp = [rng.randrange(c) for _ in range(d * d)]
            for name in ("State", "WeightedState"):
                before = getattr(old, name)(n, d, c, grid[:], target, stamp[:])
                after = getattr(self.solver, name)(n, d, c, grid[:], target, stamp[:])
                self.assertEqual(before.__dict__, after.__dict__)
                for _ in range(40):
                    action = rng.randrange(len(before.actions))
                    self.assertEqual(before.gain(action), after.gain(action))
                    self.assertEqual(before.best(), after.best())
                    before.apply(action)
                    after.apply(action)
                    self.assertEqual(before.__dict__, after.__dict__)
                    transitions += 1
            before = old.ProductiveState(n, d, c, grid[:], target, stamp[:])
            after = self.solver.State(n, d, c, grid[:], target, stamp[:])
            for threshold in (-2, 0, 1):
                self.assertEqual(before.escape(random.Random(127), width=16, min_gain=threshold),
                                 after.escape(random.Random(127), width=16, min_gain=threshold))
                self.assertEqual(before.__dict__, after.__dict__)
        MEASUREMENTS["core_equivalence"] = dict(state_and_weighted_transitions=transitions, productive_escape_trials=15)

    def test_final_file_mapping_and_size_gate(self):
        with tokenize.open(PACKED) as stream:
            decoded = decode_literal_wrapper(stream.read())
        self.assertEqual(decoded, compact_source(SOURCE.read_text()))
        checked = inspect_source(PACKED)
        self.assertTrue(checked["valid"], checked)
        self.assertLessEqual(checked["source_bytes"], 100000)
        MEASUREMENTS["artifact"] = checked
        MEASUREMENTS["source_sha256"] = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
        # Save concrete final call ordering for independent inspection.
        tree = ast.parse(SOURCE.read_text())
        wrapper = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "solve_without_regret_wildcard")
        MEASUREMENTS["wrapper_source"] = ast.unparse(wrapper)


if __name__ == "__main__":
    started = time.perf_counter()
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    report = dict(passed=result.wasSuccessful(), tests_run=result.testsRun, runtime_sec=time.perf_counter() - started,
                  failures=[dict(test=str(test), traceback=trace) for test, trace in result.failures + result.errors], measurements=MEASUREMENTS)
    (ROOT / "results/regret_review.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf8")
    raise SystemExit(not result.wasSuccessful())
