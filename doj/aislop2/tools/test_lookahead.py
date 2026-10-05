"""Differential checks for packed lookahead evaluation and transitions."""
import importlib.util
from pathlib import Path
import random
import unittest

from tools.simulate import Instance, simulate


PATH = Path(__file__).resolve().parents[1] / 'solvers/experiments/lookahead.py'


class PackedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = getattr(cls, 'candidate_path', PATH)
        spec = importlib.util.spec_from_file_location('lookahead', path)
        cls.solver = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.solver)

    def test_packed_gain_and_transition_against_canonical(self):
        rng = random.Random(31971)
        for trial in range(80):
            n, d, c = rng.randint(3, 12), rng.choice((2, 3)), rng.randint(2, 6)
            a = [rng.randrange(c) for _ in range(n*n)]
            t = [rng.randrange(c) for _ in range(n*n)]
            s = [rng.randrange(c) for _ in range(d*d)]
            instance = Instance(n, d, c, 180, a, t, s)
            state = self.solver.State(n, d, c, a.copy(), t, s.copy())
            operations = []
            old_matches = sum(x == y for x,y in zip(a,t))
            for step in range(25):
                action = rng.randrange(len(state.actions))
                indices, op = state.actions[action]
                expected_gain = sum((state.stamp[j] == t[p]) - (state.grid[p] == t[p])
                                    for j,p in enumerate(indices))
                self.assertEqual(state.gain(action), expected_gain)
                state.apply(action)
                operations.append(op)
                expected_grid, expected_stamp = simulate(instance, operations)
                self.assertEqual(state.grid, expected_grid)
                self.assertEqual(state.stamp, expected_stamp)
                new_matches = sum(x == y for x,y in zip(expected_grid,t))
                self.assertEqual(new_matches - old_matches, expected_gain)
                old_matches = new_matches
                for j in range(0, len(state.actions), 13):
                    indices, _ = state.actions[j]
                    self.assertEqual(state.gain(j), sum((state.stamp[u] == t[p]) -
                                                       (state.grid[p] == t[p])
                                                       for u,p in enumerate(indices)))

    def test_pair_choice_is_actual_positive_gain(self):
        rng = random.Random(2291)
        for _ in range(30):
            n, d, c = rng.randint(3, 8), rng.choice((2, 3)), rng.randint(2, 6)
            a = [rng.randrange(c) for _ in range(n*n)]
            t = [rng.randrange(c) for _ in range(n*n)]
            s = [rng.randrange(c) for _ in range(d*d)]
            instance = Instance(n, d, c, 50, a, t, s)
            output = self.solver.solve(n, d, c, 50, a.copy(), t, s.copy())
            final, _ = simulate(instance, output)
            self.assertGreaterEqual(sum(x == y for x,y in zip(final,t)),
                                    sum(x == y for x,y in zip(a,t)))


class WidePackedTests(PackedTests):
    candidate_path = PATH.with_name('lookahead_w128.py')


class MultiPackedTests(PackedTests):
    candidate_path = PATH.with_name('lookahead_multi4.py')


class ProductivePackedTests(PackedTests):
    candidate_path = PATH.with_name('lookahead_productive.py')


if __name__ == '__main__':
    unittest.main()
