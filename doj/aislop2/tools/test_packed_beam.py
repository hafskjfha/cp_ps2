import random
import unittest
from tools.test_solver import ROOT,load_solver
from tools.simulate import Instance,simulate,match_count


class PackedBeamTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.solver=load_solver(ROOT/'solvers/experiments/packed_late_weighted.py')

    def test_all_rotations_against_canonical(self):
        rng=random.Random(793839)
        expand=self.solver.packed_transitions()
        for _ in range(80):
            c=rng.randint(2,6)
            values=[rng.randrange(c) for _ in range(25)]
            packed=sum(v<<(3*i) for i,v in enumerate(values))
            case=Instance(4,3,c,1,values[:16],values[:16],values[16:])
            for aid,child in expand(packed):
                a,s=simulate(case,[(aid//8,(aid//4)%2,aid%4)])
                self.assertEqual(a+s,[(child>>(3*i))&7 for i in range(25)])
                self.assertEqual(dict(expand(child))[aid],packed)

    def test_complete_one_and_two_move_search(self):
        rng=random.Random(45882)
        for _ in range(20):
            c=rng.randint(2,6)
            a,t,s=[[rng.randrange(c) for _ in range(n)] for n in (16,16,9)]
            case=Instance(4,3,c,2,a,t,s)
            paths=[()]+[(i,) for i in range(16)]+[(i,j) for i in range(16) for j in range(16)]
            def score(path):
                ops=[(i//8,(i//4)%2,i%4) for i in path]
                return match_count(case,simulate(case,ops)[0])
            result=self.solver.packed_late_beam(a,t,s,2,width=512)
            self.assertEqual(score(result),max(map(score,paths)))


if __name__=='__main__':
    unittest.main()
