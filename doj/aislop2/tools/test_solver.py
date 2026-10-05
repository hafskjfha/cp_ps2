"""Differential checks for solver transition implementations."""
import importlib.util
import random
import unittest
from pathlib import Path

from tools.simulate import Instance, simulate

ROOT = Path(__file__).resolve().parents[1]


def load_solver(path):
    spec = importlib.util.spec_from_file_location('candidate_solver', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SolverTests(unittest.TestCase):
    def test_greedy_transition_and_single_best(self):
        solver = load_solver(ROOT/'solvers/greedy.py')
        rng = random.Random(123779)
        for _ in range(120):
            n, d, c = rng.randint(3, 10), rng.choice((2, 3)), rng.randint(2, 6)
            a = [rng.randrange(c) for _ in range(n*n)]
            t = [rng.randrange(c) for _ in range(n*n)]
            s = [rng.randrange(c) for _ in range(d*d)]
            instance = Instance(n,d,c,180,a,t,s)
            actions = solver.build_actions(n, d)
            grid, stamp, ops = a[:], s[:], []
            for _ in range(15):
                indices, op = rng.choice(actions)
                solver.transition(grid, stamp, indices)
                ops.append(op)
                self.assertEqual((grid, stamp), simulate(instance, ops))
            best = sum(x == y for x,y in zip(a,t))
            for _, op in actions:
                final, _ = simulate(instance, [op])
                best = max(best, sum(x == y for x,y in zip(final,t)))
            found = solver.solve(n,d,c,1,a[:],t,s[:])
            final, _ = simulate(instance, found)
            self.assertEqual(best, sum(x == y for x,y in zip(final,t)))


if __name__ == '__main__':
    unittest.main()
