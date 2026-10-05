import random
import unittest
from tools.test_solver import ROOT,load_solver
from tools.simulate import Instance,simulate,match_count,parse_instance


class RetainedIteratedTests(unittest.TestCase):
    def test_retains_both_final_parent_scores(self):
        solver=load_solver(ROOT/'solvers/experiments/retained_small_beam.py')
        old=load_solver(ROOT/'submissions/best_017_249880999.py')
        new=load_solver(ROOT/'submissions/best_018_250064691.py')
        rng=random.Random(356922)
        cases=[]
        for _ in range(8):
            n,d,c,k=rng.randint(3,8),rng.choice((2,3)),rng.randint(2,6),rng.randint(5,32)
            a,t,s=[[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
            cases.append(Instance(n,d,c,k,a,t,s))
        for case_id in ('case_072','case_125'):
            cases.append(parse_instance((ROOT/'cases/generated'/f'{case_id}.in').read_text()))
        for case in cases:
            args=(case.n,case.d,case.c,case.k,case.a,case.t,case.s)
            result=solver.solve_retained_iterated(*args)
            score=match_count(case,simulate(case,result)[0])
            for parent in (old,new):
                parent_score=match_count(case,simulate(case,parent.solve(*args))[0])
                self.assertGreaterEqual(score,parent_score)


if __name__=='__main__':
    unittest.main()
