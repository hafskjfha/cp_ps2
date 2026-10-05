"""Tiny fixed-suffix cases where a complete-state beam escapes width-one search."""
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.simulate import Instance, simulate

SPEC = importlib.util.spec_from_file_location(
    "i1_beam_advantage_solver", ROOT / "solvers/experiments/i1_block_fragment.py")
SOLVER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SOLVER)


def advance(n, d, colors, operations):
    instance = Instance(n, d, 6, 180, colors[:n*n], [0]*(n*n), colors[n*n:])
    grid, stamp = simulate(instance, operations)
    return grid + stamp


class BeamAdvantageTests(unittest.TestCase):
    def test_live_suffix_targets_benefit_from_multiple_states(self):
        examples = [
            (3, 2,
             [2, 0, 0, 1, 0, 2, 0, 0, 0, 0, 0, 2, 0],
             [1, 2, 2, 1, 0, 2, 1, 1, 0],
             [(1, 1, 3), (0, 1, 0), (1, 1, 2)], (5, 6)),
            (4, 3,
             [2, 1, 1, 1, 0, 0, 2, 0, 1, 2, 2, 0, 1, 2, 2, 0,
              0, 2, 2, 1, 1, 2, 0, 0, 0],
             [1, 0, 2, 2, 1, 1, 0, 2, 2, 1, 2, 2, 2, 1, 1, 2],
             [(1, 0, 0), (1, 0, 1), (0, 0, 2)], (9, 12)),
        ]
        for n, d, initial, target, suffix, expected in examples:
            with self.subTest(n=n, d=d):
                operations = [(x, y, r) for x in range(n-d+1)
                              for y in range(n-d+1) for r in range(4)]
                wanted = advance(n, d, target+[6]*(d*d), list(reversed(suffix)))
                self.assertIn(6, wanted[:n*n])
                self.assertTrue(any(v != 6 for v in wanted[n*n:]))
                scores = []
                for width in (1, 8):
                    path, score, used = SOLVER.i1_search_block(
                        n, d, initial, wanted, 4, width=width,
                        node_budget=10000, seed=11)
                    final = advance(n, d, initial, [operations[i] for i in path]+suffix)
                    canonical_score = sum(a == b for a, b in zip(final, target))
                    self.assertEqual(score, canonical_score)
                    self.assertLessEqual(len(path), 4)
                    self.assertLessEqual(used, 10000)
                    scores.append(score)
                self.assertEqual(tuple(scores), expected)
                self.assertGreater(scores[1], scores[0])


if __name__ == "__main__":
    unittest.main()
