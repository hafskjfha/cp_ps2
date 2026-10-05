import random
import unittest
from tools.test_solver import ROOT,load_solver
from tools.simulate import Instance,simulate,match_count


class GapAnnealingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.solver=load_solver(ROOT/'solvers/experiments/gap_informed.py')

    def test_exact_companion_and_incremental_boundaries(self):
        rng=random.Random(335894)
        solver=self.solver
        for _ in range(35):
            n,d,c,k=rng.randint(3,6),rng.choice((2,3)),rng.randint(2,6),rng.randint(4,15)
            a,t,s=[[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
            indices,_,ops,_,_=solver.build(n,d,t)
            actions=list(zip(indices,ops))
            sequence=[rng.randrange(-1,len(ops)) for _ in range(k)]
            order=list(range(len(ops)))
            rng.shuffle(order)
            gap=rng.randrange(2,k)
            walker=solver.GapWalker(n,d,a+s,t,actions,sequence,order,gap)
            case=Instance(n,d,c,k,a,t,s)
            def score(path):
                return match_count(case,simulate(case,[ops[x] for x in path if x>=0])[0])
            for turn in range(12):
                position=rng.randrange(k-gap)
                walker.move(position)
                fixed,side=rng.randrange(-1,len(ops)),rng.randrange(2)
                pair,delta=walker.propose(fixed,side)
                expected=-1
                for other in range(-1,len(ops)):
                    candidate=walker.sequence[:]
                    candidate[position]=other if side else fixed
                    candidate[position+gap]=fixed if side else other
                    expected=max(expected,score(candidate))
                walker.accept(pair,delta)
                self.assertEqual(walker.score,expected)
                self.assertEqual(walker.score,score(walker.sequence))

    def test_annealed_floor_and_determinism(self):
        rng=random.Random(991354)
        solver=self.solver
        for _ in range(20):
            n,d,c,k=rng.randint(3,9),rng.choice((2,3)),rng.randint(2,6),rng.randint(4,25)
            a,t,s=[[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
            indices,_,ops,_,_=solver.build(n,d,t)
            actions=list(zip(indices,ops))
            sequence=[rng.randrange(len(ops)) for _ in range(rng.randrange(k+1))]
            candidate=solver.gap_anneal(n,d,k,a+s,t,actions,sequence,100)
            case=Instance(n,d,c,k,a,t,s)
            before=match_count(case,simulate(case,[ops[x] for x in sequence])[0])
            after=match_count(case,simulate(case,[ops[x] for x in candidate])[0])
            self.assertGreaterEqual(after,before)
            self.assertEqual(candidate,solver.gap_anneal(n,d,k,a+s,t,actions,sequence,100))


if __name__=='__main__':
    unittest.main()
