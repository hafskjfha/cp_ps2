import random
import unittest
from tools.test_solver import ROOT,load_solver
from tools.simulate import Instance,simulate,match_count


class WildcardPartialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.solver=load_solver(ROOT/'solvers/experiments/wildcard_small.py')

    def test_all_generic_rotations(self):
        rng=random.Random(784435)
        for n in (5,6):
            expand=self.solver.packed3_transitions(n)
            for _ in range(25):
                c=rng.randint(2,6)
                values=[rng.randrange(c) for _ in range(n*n+9)]
                packed=sum(v<<(3*i) for i,v in enumerate(values))
                case=Instance(n,3,c,1,values[:n*n],values[:n*n],values[n*n:])
                for aid,child in expand(packed):
                    op=(aid//4//(n-2),aid//4%(n-2),aid%4)
                    a,s=simulate(case,[op])
                    self.assertEqual(a+s,[(child>>(3*i))&7 for i in range(n*n+9)])
                    self.assertEqual(dict(expand(child))[aid],packed)

    def test_partial_goal_strict_floor(self):
        rng=random.Random(891366)
        for _ in range(8):
            n,c=5,rng.randint(2,6)
            a,s=[[rng.randrange(c) for _ in range(size)] for size in (n*n,9)]
            case=Instance(n,3,c,2,a,a,s)
            moves=[(rng.randrange(n-2),rng.randrange(n-2),rng.randrange(4)) for _ in range(2)]
            target,_=simulate(case,moves)
            result=self.solver.wildcard_partial(n,a,target,s,2)
            if a==target:
                continue
            self.assertIsNotNone(result)
            case.t=target
            final,_=simulate(case,[(aid//4//(n-2),aid//4%(n-2),aid%4) for aid in result])
            self.assertGreater(match_count(case,final),match_count(case,a))
            self.assertTrue(all(final[p]==target[p] for p in range(n*n) if a[p]==target[p]))


if __name__=='__main__':
    unittest.main()
