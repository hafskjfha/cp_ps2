"""Canonical packed D2 transitions and retained late repair tests."""
import random
import unittest

from tools.test_solver import ROOT, load_solver
from tools.simulate import Instance, simulate, match_count


class D2BeamTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.solver = load_solver(ROOT/'solvers/experiments/forward_d2_beam_four.py')

    def test_all_rotations_and_large_ids_match_canonical(self):
        rng = random.Random(491287)
        for n in (3,5,8,10,12):
            for c in (2,6):
                a,t,s = [[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,4)]
                case = Instance(n,2,c,1,a,t,s)
                initial = sum(v<<(3*i) for i,v in enumerate(a+s))
                children = list(self.solver.packed2_transitions(n)(initial))
                self.assertEqual([aid for aid,_ in children],list(range(4*(n-1)**2)))
                for aid,child in children:
                    width = n-1
                    op = (aid//(4*width),(aid//4)%width,aid%4)
                    grid,stamp = simulate(case,[op])
                    self.assertEqual(child,sum(v<<(3*i) for i,v in enumerate(grid+stamp)))

    def test_random_packed_sequences_match_full_canonical_states(self):
        rng = random.Random(843119)
        for n in (3,5,10,12):
            c = 6
            a,t,s = [[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,4)]
            case = Instance(n,2,c,20,a,t,s)
            state = sum(v<<(3*i) for i,v in enumerate(a+s))
            expand = self.solver.packed2_transitions(n)
            operations = []
            for _ in range(20):
                aid = rng.randrange(4*(n-1)**2)
                state = dict(expand(state))[aid]
                width = n-1
                operations.append((aid//(4*width),(aid//4)%width,aid%4))
                grid,stamp = simulate(case,operations)
                self.assertEqual(state,sum(v<<(3*i) for i,v in enumerate(grid+stamp)))

    def test_simple_high_id_repairs_improve_true_score(self):
        for n in (5,10,12):
            a,s = [0]*(n*n),[1]*4
            case = Instance(n,2,2,1,a,a[:],s)
            target,_ = simulate(case,[(n-2,n-2,3)])
            case.t = target
            tail = self.solver.d2_beam_finish(n,a,target,s,1)
            self.assertIsNotNone(tail)
            self.assertEqual(len(tail),1)
            if n>=10:
                self.assertGreater(tail[0],255)
            width = n-1
            operations = [(aid//(4*width),(aid//4)%width,aid%4) for aid in tail]
            self.assertGreater(match_count(case,simulate(case,operations)[0]),match_count(case,a))

    def test_wrapper_budget_floor_and_harmful_tail_rejection(self):
        solver = self.solver
        parent,helper = solver.solve_d2_parent,solver.d2_beam_finish
        try:
            for n in (5,10,12):
                a,s = [0]*(n*n),[1]*4
                case = Instance(n,2,2,4,a,a[:],s)
                target,_ = simulate(case,[(n-2,n-2,0)])
                case.t = target
                solver.solve_d2_parent = lambda *args: []
                original = (a[:],target[:],s[:])
                result = solver.solve(n,2,2,4,a,target,s)
                self.assertEqual((a,target,s),original)
                self.assertLessEqual(len(result),4)
                self.assertGreaterEqual(match_count(case,simulate(case,result)[0]),match_count(case,a))
                solver.d2_beam_finish = lambda *args: [0]
                self.assertEqual(solver.solve(n,2,2,4,a,target,s),[])
                solver.d2_beam_finish = helper
        finally:
            solver.solve_d2_parent,solver.d2_beam_finish = parent,helper


if __name__=='__main__':
    unittest.main()
