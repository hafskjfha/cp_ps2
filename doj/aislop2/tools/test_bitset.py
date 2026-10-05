"""Exact tie-order and canonical transition checks for bit-sliced evaluation."""
import json
import random
import unittest
from pathlib import Path

from solvers.experiments import bitset_lookahead as fast
from solvers.experiments import bitset_lookahead8 as wider
from solvers.experiments import lookahead_multi4 as reference
from tools.simulate import Instance, parse_instance, simulate


class BitsetTests(unittest.TestCase):
    def test_randomized_best_and_canonical_transitions(self):
        rng = random.Random(671991)
        for trial in range(48):
            n, d, c = (3, 7, 14, 30)[trial % 4], rng.choice((2, 3)), rng.randrange(2, 7)
            grid = [rng.randrange(c) for _ in range(n*n)]
            target = [rng.randrange(c) for _ in grid]
            stamp = [rng.randrange(c) for _ in range(d*d)]
            order = list(range(4*(n-d+1)**2))
            rng.shuffle(order)
            a = reference.State(n, d, c, grid[:], target, stamp[:])
            a.order = order[:]
            b = fast.State(n, d, c, grid[:], target, stamp[:], order[:])
            widened = wider.State(n, d, c, grid[:], target, stamp[:], order[:])
            operations = []
            for step in range(50):
                with self.subTest(trial=trial, step=step):
                    self.assertEqual(b.best(), a.best())
                    self.assertEqual(widened.best(), a.best())
                    chosen = a.best()[1] if step % 2 else rng.randrange(len(order))
                    a.apply(chosen)
                    b.apply(chosen)
                    widened.apply(chosen)
                    operations.append(b.actions[chosen][1])
                    self.assertEqual(b.grid, a.grid)
                    self.assertEqual(b.stamp, a.stamp)
                    self.assertEqual(b.counts, a.counts)
            expected = simulate(Instance(n, d, c, 180, grid, target, stamp), operations)
            self.assertEqual((b.grid, b.stamp), expected)
            self.assertEqual((widened.grid, widened.stamp), expected)

    def test_full_sequences_match_baseline_exactly(self):
        root = Path(__file__).resolve().parents[1]
        manifest = json.loads((root / 'cases/manifest.json').read_text())
        for meta in manifest['cases'][:24]:
            case = parse_instance((root / meta['path']).read_text())
            args = (case.n, case.d, case.c, case.k, case.a, case.t, case.s)
            with self.subTest(case=meta['id']):
                self.assertEqual(fast.solve(*args), reference.solve(*args))


if __name__ == '__main__':
    unittest.main()
