"""Canonical checks for larger packed-board beam repairs."""
import random
import unittest

from tools.test_solver import ROOT, load_solver
from tools.simulate import Instance, simulate, match_count


class WideBeamTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.solver = load_solver(ROOT/'solvers/experiments/forward_wide_beam_four.py')

    def test_all_large_board_rotations_match_canonical_swaps(self):
        rng = random.Random(391582)
        for n in (10,11,12):
            for c in (2,6):
                a,t,s = [[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,9)]
                case = Instance(n,3,c,1,a,t,s)
                packed = sum(v<<(3*i) for i,v in enumerate(a+s))
                seen = []
                for aid,child in self.solver.packed3_transitions(n)(packed):
                    width = n-2
                    op = (aid//(4*width),(aid//4)%width,aid%4)
                    grid,stamp = simulate(case,[op])
                    expected = sum(v<<(3*i) for i,v in enumerate(grid+stamp))
                    self.assertEqual(child,expected)
                    seen.append(aid)
                self.assertEqual(seen,list(range(4*(n-2)**2)))

    def test_two_byte_paths_return_legal_improving_high_ids(self):
        for n in (10,11,12):
            a,s = [0]*(n*n),[1]*9
            case = Instance(n,3,2,1,a,a[:],s)
            target,_ = simulate(case,[(n-3,n-3,0)])
            case.t = target
            tail = self.solver.wide_beam_finish(n,a,target,s,1)
            self.assertIsNotNone(tail)
            self.assertEqual(len(tail),1)
            if n>=11:
                self.assertGreater(tail[0],255)
            width = n-2
            ops = [(aid//(4*width),(aid//4)%width,aid%4) for aid in tail]
            after,_ = simulate(case,ops)
            self.assertGreater(match_count(case,after),match_count(case,a))

    def test_wrapper_preserves_parent_score_budget_and_inputs(self):
        solver = self.solver
        parent = solver.solve_wide_parent
        try:
            for n in (10,11,12):
                for k in (1,2,7):
                    a,s = [0]*(n*n),[1]*9
                    case = Instance(n,3,2,k,a,a[:],s)
                    target,_ = simulate(case,[(n-3,n-3,1)])
                    case.t = target
                    solver.solve_wide_parent = lambda *args: []
                    original = (a[:],target[:],s[:])
                    result = solver.solve(n,3,2,k,a,target,s)
                    self.assertEqual((a,target,s),original)
                    self.assertLessEqual(len(result),k)
                    self.assertGreaterEqual(match_count(case,simulate(case,result)[0]),match_count(case,a))
        finally:
            solver.solve_wide_parent = parent

    def test_wrapper_rejects_nonimproving_proposals(self):
        solver = self.solver
        parent,helper = solver.solve_wide_parent,solver.wide_beam_finish
        try:
            n = 11
            a,s = [0]*(n*n),[1]*9
            case = Instance(n,3,2,4,a,a[:],s)
            target,_ = simulate(case,[(n-3,n-3,0)])
            solver.solve_wide_parent = lambda *args: []
            solver.wide_beam_finish = lambda *args: [0]
            self.assertEqual(solver.solve(n,3,2,4,a,target,s),[])
        finally:
            solver.solve_wide_parent,solver.wide_beam_finish = parent,helper


if __name__=='__main__':
    unittest.main()
