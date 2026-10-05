import random
import unittest
from tools.test_solver import ROOT,load_solver
from tools.simulate import Instance,simulate,match_count


class PruningTests(unittest.TestCase):
    def test_pruned_subsequence_score_floor(self):
        solver=load_solver(ROOT/'solvers/experiments/prune_cached.py')
        rng=random.Random(119859)
        for _ in range(150):
            n,d,c,k=rng.randint(3,12),rng.choice((2,3)),rng.randint(2,6),rng.randint(1,80)
            a,t,s=[[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
            indices,_,ops,_,_=solver.build(n,d,t)
            sequence=[rng.randrange(len(ops)) for _ in range(k)]
            result=solver.prune_sequence(n*n,a+s,t,list(zip(indices,ops)),sequence)
            it=iter(sequence)
            self.assertTrue(all(any(x==aid for x in it) for aid in result))
            case=Instance(n,d,c,k,a,t,s)
            before,_=simulate(case,[ops[x] for x in sequence])
            after,_=simulate(case,[ops[x] for x in result])
            self.assertGreaterEqual(match_count(case,after),match_count(case,before))


if __name__=='__main__':
    unittest.main()
