import random
import unittest
from tools.test_solver import ROOT,load_solver
from tools.simulate import Instance,simulate


class BinarySearchTests(unittest.TestCase):
    def test_transition_encoding_and_involution(self):
        solver=load_solver(ROOT/'solvers/experiments/binary_bfs_fragment.py')
        expand=solver.binary_transitions()
        rng=random.Random(842263)
        for _ in range(80):
            a,s=[[rng.randrange(2) for _ in range(size)] for size in (16,9)]
            state=sum(v<<i for i,v in enumerate(a+s))
            case=Instance(4,3,2,1,a,[0]*16,s)
            for aid,child in expand(state):
                op=(aid//8,(aid//4)%2,aid%4)
                final,stamp=simulate(case,[op])
                self.assertEqual(child,sum(v<<i for i,v in enumerate(final+stamp)))
                self.assertEqual(dict(expand(child))[aid],state)

    def test_reachable_goals_with_short_budget(self):
        solver=load_solver(ROOT/'solvers/experiments/binary_bfs_fragment.py')
        rng=random.Random(842264)
        for k in range(1,6):
            for _ in range(5):
                a,s=[[rng.randrange(2) for _ in range(size)] for size in (16,9)]
                original=Instance(4,3,2,k,a,[0]*16,s)
                path=[(rng.randrange(2),rng.randrange(2),rng.randrange(4)) for _ in range(k)]
                target,_=simulate(original,path)
                result=solver.binary_bfs(a,target,s,k)
                self.assertIsNotNone(result)
                case=Instance(4,3,2,k,a,target,s)
                final,_=simulate(case,[(x//8,(x//4)%2,x%4) for x in result])
                self.assertEqual(final,target)


if __name__=='__main__':
    unittest.main()
