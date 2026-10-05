import random
import unittest
from tools.test_solver import ROOT,load_solver
from tools.simulate import Instance,simulate


class WildcardFinishTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.solver=load_solver(ROOT/'solvers/experiments/wildcard_weighted.py')

    def test_reachable_targets_with_free_final_stamp(self):
        rng=random.Random(883192)
        for depth in range(1,6):
            for _ in range(3):
                c=rng.randint(2,6)
                a,s=[[rng.randrange(c) for _ in range(n)] for n in (16,9)]
                case=Instance(4,3,c,depth,a,a,s)
                path=[(rng.randrange(2),rng.randrange(2),rng.randrange(4)) for _ in range(depth)]
                target,_=simulate(case,path)
                result=self.solver.wildcard_finish(a,target,s,depth)
                self.assertIsNotNone(result)
                self.assertLessEqual(len(result),depth)
                result=[(i//8,(i//4)%2,i%4) for i in result]
                self.assertEqual(simulate(case,result)[0],target)

    def test_impossible_inventory_rejected(self):
        self.assertIsNone(self.solver.wildcard_finish([0]*16,[1]*16,[1]*9,8))

    def test_deeper_wildcard_join(self):
        rng=random.Random(239876)
        for depth in (6,7,8):
            a,s=[[rng.randrange(6) for _ in range(n)] for n in (16,9)]
            case=Instance(4,3,6,depth,a,a,s)
            path=[(rng.randrange(2),rng.randrange(2),rng.randrange(4)) for _ in range(depth)]
            target,_=simulate(case,path)
            result=self.solver.wildcard_finish(a,target,s,depth)
            self.assertIsNotNone(result)
            self.assertLessEqual(len(result),depth)
            self.assertEqual(simulate(case,[(i//8,(i//4)%2,i%4) for i in result])[0],target)


if __name__=='__main__':
    unittest.main()
