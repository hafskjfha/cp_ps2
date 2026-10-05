"""Exact old/new state checks for parallel region count-plane arithmetic."""
import random
import unittest

from tools.test_solver import ROOT, load_solver


class ParallelCountTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = load_solver(ROOT / 'solvers/experiments/late_beam_four_fast.py')
        cls.new = load_solver(ROOT / 'solvers/experiments/refine_parallel_counts.py')

    def test_mixed_actual_and_wish_transitions(self):
        rng = random.Random(921731)
        checks = 0
        for n in (3, 4, 7, 16, 30):
            for d in (2, 3):
                for c in (2, 6):
                    initial = [rng.randrange(c) for _ in range(n*n+d*d)]
                    target = [rng.randrange(c) for _ in range(n*n)]
                    indices, _, ops, _, _ = self.old.build(n, d, target)
                    actions = list(zip(indices, ops))
                    order = list(range(len(actions)))
                    rng.shuffle(order)
                    states = [m.RefineState(n, d, initial, target, actions, order)
                              for m in (self.old, self.new)]
                    for step in range(60):
                        aid, wishes = rng.randrange(len(actions)), bool(rng.randrange(2))
                        for s in states:
                            s.apply(aid, wishes)
                        for field in ('grid', 'stamp', 'wishes', 'wstamp',
                                      'old_planes', 'values', 'goals'):
                            self.assertEqual(getattr(states[0], field),
                                             getattr(states[1], field), (n, d, c, step, field))
                        self.assertEqual(states[0].best(), states[1].best())
                        expected = [sum(states[1].grid[p] == states[1].wishes[p] for p in patch)
                                    for patch in states[1].regions]
                        self.assertEqual(states[0].counts, expected)
                        if states[1].counts is not None:
                            self.assertEqual(states[1].counts, expected)
                        checks += 1
        self.assertEqual(checks, 1200)

    def test_complete_sweeps_preserve_sequences(self):
        rng = random.Random(189921)
        for _ in range(24):
            n, d, c, k = rng.randint(3, 14), rng.choice((2, 3)), rng.randint(2, 6), 30
            initial = [rng.randrange(c) for _ in range(n*n+d*d)]
            target = [rng.randrange(c) for _ in range(n*n)]
            indices, _, ops, _, _ = self.old.build(n, d, target)
            actions = list(zip(indices, ops))
            sequence = [rng.randrange(len(ops)) for _ in range(rng.randrange(k+1))]
            self.assertEqual(self.old.refine(n, d, k, initial, target, actions, sequence, passes=3),
                             self.new.refine(n, d, k, initial, target, actions, sequence, passes=3))

    def test_nested_trial_restore_parity(self):
        rng = random.Random(736811)
        for n, d in ((3, 2), (3, 3), (9, 2), (9, 3), (30, 2), (30, 3)):
            initial = [rng.randrange(6) for _ in range(n*n+d*d)]
            target = [rng.randrange(6) for _ in range(n*n)]
            indices, _, ops, _, _ = self.old.build(n, d, target)
            actions = list(zip(indices, ops))
            order = list(range(len(ops)))
            rng.shuffle(order)
            states = [m.RefineState(n, d, initial, target, actions, order)
                      for m in (self.old, self.new)]
            stacks = [[], []]
            for _ in range(100):
                if stacks[0] and (len(stacks[0]) == 5 or rng.randrange(3) == 0):
                    for m, state, stack in zip((self.old, self.new), states, stacks):
                        m.refine_restore(state, stack.pop())
                else:
                    aid, wishes = rng.randrange(-1, len(ops)), bool(rng.randrange(2))
                    for m, state, stack in zip((self.old, self.new), states, stacks):
                        stack.append(m.refine_trial(state, aid, wishes))
                for field in ('grid', 'stamp', 'wishes', 'wstamp', 'old_planes', 'values', 'goals'):
                    self.assertEqual(getattr(states[0], field), getattr(states[1], field))
                self.assertEqual(states[0].best(), states[1].best())


class PlanesOnlyTests(ParallelCountTests):
    @classmethod
    def setUpClass(cls):
        cls.old = load_solver(ROOT / 'solvers/experiments/late_beam_four_fast.py')
        cls.new = load_solver(ROOT / 'solvers/experiments/refine_planes_only.py')


if __name__ == '__main__':
    unittest.main()
