import random
import unittest
from collections import Counter
from tools.test_solver import ROOT,load_solver
from tools.simulate import Instance,simulate,match_count


class ReorderTests(unittest.TestCase):
    def test_multiset_preserved_and_canonical_score_floor(self):
        solver=load_solver(ROOT/'solvers/experiments/reorder_guided.py')
        rng=random.Random(878332)
        for _ in range(70):
            n,d,c,k=rng.randint(3,9),rng.choice((2,3)),rng.randint(2,6),rng.randint(1,35)
            a,t,s=[[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
            indices,_,ops,_,_=solver.build(n,d,t)
            actions=list(zip(indices,ops))
            sequence=[rng.randrange(len(ops)) for _ in range(rng.randrange(k+1))]
            result=solver.reorder_sequence(n,d,k,a+s,t,actions,sequence)
            self.assertEqual(Counter(sequence),Counter(result))
            case=Instance(n,d,c,k,a,t,s)
            old,_=simulate(case,[ops[x] for x in sequence])
            final,_=simulate(case,[ops[x] for x in result])
            self.assertGreaterEqual(match_count(case,final),match_count(case,old))


if __name__=='__main__':
    unittest.main()
