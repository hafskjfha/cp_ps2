"""Regression checks for integrated bitset search and monotonic refinement."""
import random
import unittest

from tools.test_solver import ROOT, load_solver
from tools.simulate import Instance, simulate, match_count


class FinalSolverTests(unittest.TestCase):
    def test_plateau_preserves_scalar_actions(self):
        scalar = load_solver(ROOT/'solvers/experiments/sequence_bitset_strong.py')
        fast = load_solver(ROOT/'solvers/experiments/sequence_bitset_final.py')
        rng = random.Random(9313811)
        for _ in range(100):
            n,d,c,k = rng.randint(3,10),rng.choice((2,3)),rng.randint(2,6),rng.randint(1,60)
            a,t,s = [[rng.randrange(c) for _ in range(count)] for count in (n*n,n*n,d*d)]
            self.assertEqual(scalar.solve_plateau(n,d,c,k,a,t,s),fast.solve_plateau(n,d,c,k,a,t,s))

    def test_refinement_monotonic_and_canonical_score(self):
        fast = load_solver(ROOT/'solvers/experiments/sequence_bitset_final.py')
        rng = random.Random(72163)
        for _ in range(24):
            n,d,c,k = rng.randint(3,8),rng.choice((2,3)),rng.randint(2,6),rng.randint(1,30)
            a,t,s = [[rng.randrange(c) for _ in range(count)] for count in (n*n,n*n,d*d)]
            case = Instance(n,d,c,k,a,t,s)
            ops = fast.construct(n,d,c,k,a[:],t,s[:])
            indices,_,actions,_,_ = fast.build(n,d,t)
            width = n-d+1
            sequence = [(x*width+y)*4+r for x,y,r in ops]
            scores = []
            for passes in (0,6,8):
                refined = fast.refine(n,d,k,a+s,t,list(zip(indices,actions)),sequence[:],passes=passes)
                result = [actions[aid] for aid in refined]
                final,_ = simulate(case,result)
                scores.append(match_count(case,final))
            self.assertLessEqual(scores[0],scores[1])
            self.assertLessEqual(scores[1],scores[2])
            final,_ = simulate(case,fast.solve(n,d,c,k,a[:],t,s[:]))
            self.assertEqual(scores[-1],match_count(case,final))


if __name__ == '__main__':
    unittest.main()
