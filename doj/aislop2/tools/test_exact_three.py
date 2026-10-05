import itertools
import random
import unittest
from tools.test_solver import ROOT,load_solver
from tools.simulate import Instance,simulate,match_count,parse_instance


class ExactThreeTests(unittest.TestCase):
    def test_exhaustive_canonical_optimum(self):
        solver=load_solver(ROOT/'solvers/experiments/exact_three_cached.py')
        rng=random.Random(911331)
        for _ in range(12):
            n,d,c=rng.choice(((3,2,2),(3,3,4),(4,3,3)))
            a,t,s=[[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
            case=Instance(n,d,c,3,a,t,s)
            _,_,ops,_,_=solver.build(n,d,t)
            best=match_count(case,a)
            for length in (1,2,3):
                for path in itertools.product(ops,repeat=length):
                    best=max(best,match_count(case,simulate(case,path)[0]))
            result=solver.exact_three(n,d,c,a,t,s)
            self.assertEqual(best,match_count(case,simulate(case,result)[0]))


if __name__=='__main__':
    unittest.main()
