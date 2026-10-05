"""Independent canonical exhaustive checks for parallel routing scores."""
import json
from pathlib import Path
import random
import sys
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from solvers.experiments import route_bits_fragment as parallel
from solvers.experiments import route_sparse_fragment as scalar
from tools.simulate import Instance, match_count, simulate

parallel.route_patterns = scalar.route_patterns
MEASUREMENTS = {}


def word(pattern, x, y):
    dx, dy, r, s, backward, count, _ = pattern
    left, right = (x, y, r), (x + dx, y + dy, s)
    return ([right, left] if backward else [left, right]) * count


def best_canonical(case, repeats):
    initial = match_count(case, case.a)
    best_gain, best, considered = 0, [], 0
    width = case.n - case.d + 1
    for pattern in scalar.route_patterns(case.n, case.d, repeats):
        dx, dy, _, _, _, count, _ = pattern
        if 2 * count > case.k:
            continue
        for x in range(max(0, width - dx)):
            for y in range(max(0, -dy), min(width, width - dy)):
                operations = word(pattern, x, y)
                final, _ = simulate(case, operations)
                gain = match_count(case, final) - initial
                if gain > best_gain:
                    best_gain, best = gain, operations
                considered += 1
    return best_gain, best, considered


class ParallelRoutingReview(unittest.TestCase):
    def test_all_anchor_argmax_and_ties_match_canonical(self):
        rng = random.Random(314093)
        configurations = [(3, 2, 2, (3,)), (3, 3, 6, (3,)), (4, 3, 6, (3,)),
                          (4, 2, 2, (5,)), (5, 3, 2, (6,)), (5, 2, 6, (9,)),
                          (4, 3, 6, (3, 5)), (5, 3, 6, (3, 3))]
        considered = 0
        for n, d, c, repeats in configurations:
            for variant in range(2):
                grid, target, stamp = [[rng.randrange(c) for _ in range(size)] for size in (n * n, n * n, d * d)]
                if variant:
                    target = grid[:]
                    for _ in range(max(1, n * n // 8)):
                        target[rng.randrange(n * n)] = rng.randrange(c)
                case = Instance(n, d, c, 2 * max(repeats), grid, target, stamp)
                expected_gain, expected_path, count = best_canonical(case, repeats)
                actual = parallel.route_tail_bits(n, d, grid, target, stamp, case.k, repeats, 1)
                self.assertEqual(actual, expected_path, (n, d, c, repeats, variant))
                final, _ = simulate(case, actual)
                self.assertEqual(match_count(case, final) - match_count(case, grid), expected_gain)
                considered += count
        MEASUREMENTS["canonical_argmax"] = dict(fixtures=16, complete_permutation_sequences=considered)

    def test_full_accumulator_carry_and_negative_offsets(self):
        rng = random.Random(145789)
        patterns = scalar.route_patterns(6, 3, (3, 5, 6))
        chosen = [max(patterns, key=lambda item: len(item[-1])),
                  max((item for item in patterns if item[1] < 0), key=lambda item: len(item[-1]))]
        for pattern in chosen:
            count, mapping = pattern[5], pattern[-1]
            x, y = 0, max(0, -pattern[1])
            operations = word(pattern, x, y)
            for _ in range(1000):
                grid, stamp = [[rng.randrange(6) for _ in range(size)] for size in (36, 9)]
                fixture = Instance(6, 3, 6, 2 * count, grid, grid, stamp)
                target, _ = simulate(fixture, operations)
                if sum(a != b for a, b in zip(grid, target)) == len(mapping):
                    break
            else:
                self.fail("Could not produce a full-carry witness.")
            case = Instance(6, 3, 6, 2 * count, grid, target, stamp)
            with patch.object(parallel, "route_patterns", return_value=[pattern]), patch.object(scalar, "route_patterns", return_value=[pattern]):
                answer = parallel.route_tail_bits(6, 3, grid, target, stamp, case.k, (count,), 1)
                expected = scalar.route_tail(6, 3, grid, target, stamp, case.k, (count,), 1)
            self.assertEqual(answer, expected)
            self.assertEqual(simulate(case, answer)[0], target)
        MEASUREMENTS["full_carry"] = dict(fixtures=len(chosen), mapping_lengths=[len(item[-1]) for item in chosen], negative_offset_exercised=True)

    def test_short_budget_scalar_contract(self):
        grid = [1, 0, 1, 0, 1, 1, 0, 1, 0]
        target = [0, 1, 1, 1, 0, 0, 0, 1, 1]
        stamp = [1, 1, 0, 1]
        for k, powers in ((0, (3,)), (1, (3,)), (4, (2,)), (5, (2,)), (5, (3,))):
            self.assertEqual(parallel.route_tail_bits(3, 2, grid, target, stamp, k, powers, 1),
                             scalar.route_tail(3, 2, grid, target, stamp, k, powers, 1))
        self.assertEqual(parallel.route_tail_bits(3, 2, grid, target, stamp, 6, (5,), 1), [])


if __name__ == "__main__":
    started = time.perf_counter()
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    report = dict(passed=result.wasSuccessful(), tests_run=result.testsRun, runtime_sec=time.perf_counter() - started,
                  failures=[dict(test=str(test), traceback=trace) for test, trace in result.failures + result.errors], measurements=MEASUREMENTS)
    (ROOT / "results/route_bits_review.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf8")
    raise SystemExit(not result.wasSuccessful())
