"""Four-window oracles on the composed fast parent and its late-beam floor."""
import copy
import random

from tools import test_forward_four_window_anneal as core
from tools.test_solver import ROOT, load_solver
from tools.simulate import Instance, simulate


class AllRepairsTests(core.AnnealedFourWindowTests):
    @classmethod
    def setUpClass(cls):
        cls.solver = load_solver(ROOT/'solvers/experiments/forward_all_repairs.py')

    def test_four_window_proposals_restore_none_counts(self):
        solver = self.solver
        rng = random.Random(564183)
        n,d,c,k = 6,3,6,10
        a,t,s = [[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
        indices,_,ops,_,_ = solver.build(n,d,t)
        actions = list(zip(indices,ops))
        sequence = [rng.randrange(len(actions)) for _ in range(k)]
        walker = solver.FourWindowWalker(n,d,a+s,t,actions,sequence,list(range(len(actions))))
        self.assertIsNone(walker.state.counts)
        for _ in range(25):
            walker.move(rng.randrange(k-3))
            before = copy.deepcopy(walker.state.__dict__)
            candidates = [(rng.randrange(-1,len(actions)),rng.randrange(2)) for _ in range(5)]
            window,delta = walker.propose(rng.randrange(-1,len(actions)),rng.randrange(-1,len(actions)),candidates)
            self.assertEqual(walker.state.__dict__,before)
            self.assertIsNone(walker.state.counts)
            walker.accept(window,delta)

    def test_final_deeper_layer_rejects_worse_tail(self):
        solver = self.solver
        parent,helper = solver.solve_without_deeper_beam,solver.deeper_beam_finish
        try:
            n,d,k = 5,3,4
            a,s = [0]*(n*n),[1]*(d*d)
            case = Instance(n,d,2,k,a,a[:],s)
            t,_ = simulate(case,[(n-d,n-d,0)])
            # Eight wrong cells satisfy the deeper wrapper's eligibility.
            t[-1] = 0
            solver.solve_without_deeper_beam = lambda *args: []
            solver.deeper_beam_finish = lambda *args: [0]
            self.assertEqual(solver.solve(n,d,2,k,a,t,s),[])
        finally:
            solver.solve_without_deeper_beam,solver.deeper_beam_finish = parent,helper


if __name__=='__main__':
    import unittest
    unittest.main()
