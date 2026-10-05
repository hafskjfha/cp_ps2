import random
import unittest
from tools.test_solver import ROOT,load_solver
from tools.simulate import Instance,simulate,match_count


class SmallBeamTests(unittest.TestCase):
    def test_novel_beam_agrees_with_exhaustive_two_moves(self):
        solver=load_solver(ROOT/'solvers/experiments/small_beam_novel.py')
        rng=random.Random(123771)
        for _ in range(24):
            n,d,c=rng.randint(3,4),rng.choice((2,3)),rng.randint(2,6)
            a,t,s=[[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
            case=Instance(n,d,c,2,a,t,s)
            beam=solver.novel_small_beam(n,d,c,2,a,t,s,width=128)
            exact=solver.exact_two(n,d,c,2,a,t,s)
            self.assertEqual(match_count(case,simulate(case,beam)[0]),
                             match_count(case,simulate(case,exact)[0]))


if __name__=='__main__':
    unittest.main()
