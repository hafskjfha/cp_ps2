import random
import unittest
from tools.test_solver import ROOT,load_solver
from tools.simulate import Instance,simulate,match_count


class WildcardBeamTests(unittest.TestCase):
    def test_canonical_score_floor_and_two_move_completeness(self):
        solver=load_solver(ROOT/'solvers/experiments/wildcard_beam_small.py')
        rng=random.Random(813984)
        for trial in range(16):
            n,c=rng.choice((5,6)),rng.randint(2,6)
            k=2 if trial<8 else rng.randint(3,6)
            a,s=[[rng.randrange(c) for _ in range(size)] for size in (n*n,9)]
            case=Instance(n,3,c,k,a,a,s)
            known=[(rng.randrange(n-2),rng.randrange(n-2),rng.randrange(4)) for _ in range(k)]
            target,_=simulate(case,known)
            case.t=target
            path=solver.wildcard_partial(n,a,target,s,k)
            if trial<8 and a!=target:
                self.assertIsNotNone(path)
            if path is not None:
                final,_=simulate(case,[(i//4//(n-2),i//4%(n-2),i%4) for i in path])
                self.assertGreater(match_count(case,final),match_count(case,a))


if __name__=='__main__':
    unittest.main()
