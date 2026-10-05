"""Reuse exact four-window oracles and check best retention through losses."""
import random

from tools import test_forward_four_window as core
from tools.test_solver import ROOT, load_solver
from tools.simulate import Instance, simulate, match_count


class AnnealedFourWindowTests(core.FourWindowTests):
    @classmethod
    def setUpClass(cls):
        cls.solver = load_solver(ROOT/'solvers/experiments/forward_four_window_anneal035.py')

    def test_negative_exploration_preserves_best_visited_score(self):
        solver = self.solver
        original = solver.FourWindowWalker
        accepted = []
        class TrackedWalker(original):
            def accept(self,window,delta):
                super().accept(window,delta)
                accepted.append((delta,self.score))
        solver.FourWindowWalker = TrackedWalker
        negative_count = 0
        rng = random.Random(712384)
        try:
            for trial in range(10):
                n,d,c,k = 5,2+trial%2,3,12
                a,t,s = [[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
                indices,_,ops,_,_ = solver.build(n,d,t)
                actions = list(zip(indices,ops))
                sequence = [rng.randrange(len(actions)) for _ in range(k)]
                case = Instance(n,d,c,k,a,t,s)
                initial_score = match_count(case,simulate(case,[ops[x] for x in sequence])[0])
                accepted.clear()
                result = solver.repair_four_windows(n,d,k,a+s,t,actions,sequence,proposals=120)
                final_score = match_count(case,simulate(case,[ops[x] for x in result])[0])
                expected = max([initial_score]+[score for _,score in accepted])
                self.assertEqual(final_score,expected)
                negative_count += sum(delta<0 for delta,_ in accepted)
        finally:
            solver.FourWindowWalker = original
        self.assertGreater(negative_count,0)


if __name__=='__main__':
    import unittest
    unittest.main()
