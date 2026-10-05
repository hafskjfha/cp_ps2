import random
import unittest
from tools.test_solver import ROOT,load_solver
from tools.simulate import Instance,simulate,match_count


class IteratedRefinementTests(unittest.TestCase):
    def test_deterministic_legal_score_floor(self):
        solver=load_solver(ROOT/'solvers/experiments/iterated_hybrid.py')
        rng=random.Random(436822)
        for _ in range(30):
            n,d,c,k=rng.randint(3,8),rng.choice((2,3)),rng.randint(2,6),rng.randint(1,30)
            a,t,s=[[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
            indices,_,ops,_,_=solver.build(n,d,t)
            actions=list(zip(indices,ops))
            sequence=[rng.randrange(len(ops)) for _ in range(rng.randrange(k+1))]
            candidate=solver.iterated_refine(n,d,k,a+s,t,actions,sequence)
            self.assertEqual(candidate,solver.iterated_refine(n,d,k,a+s,t,actions,sequence))
            case=Instance(n,d,c,k,a,t,s)
            before,_=simulate(case,[ops[x] for x in sequence])
            after,_=simulate(case,[ops[x] for x in candidate])
            self.assertGreaterEqual(match_count(case,after),match_count(case,before))


if __name__=='__main__':
    unittest.main()
