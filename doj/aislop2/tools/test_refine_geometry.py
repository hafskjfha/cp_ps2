import random
import unittest
from tools.test_solver import ROOT,load_solver


class RefineGeometryTests(unittest.TestCase):
    def test_exact_actions_after_mixed_transitions(self):
        old=load_solver(ROOT/'solvers/experiments/pool_sa_fast.py')
        new=load_solver(ROOT/'solvers/experiments/refine_cached.py')
        rng=random.Random(612277)
        for _ in range(70):
            n,d,c=rng.randint(3,14),rng.choice((2,3)),rng.randint(2,6)
            initial,target=[[rng.randrange(c) for _ in range(size)] for size in (n*n+d*d,n*n)]
            indices,_,ops,_,_=old.build(n,d,target)
            actions=list(zip(indices,ops))
            order=list(range(len(ops)));rng.shuffle(order)
            a=old.RefineState(n,d,initial,target,actions,order)
            b=new.RefineState(n,d,initial,target,actions,order)
            for _ in range(25):
                self.assertEqual(a.best(),b.best())
                aid=rng.randrange(len(ops));wish=bool(rng.randrange(2))
                a.apply(aid,wishes=wish);b.apply(aid,wishes=wish)
                for field in ('grid','stamp','wishes','wstamp','counts'):
                    self.assertEqual(getattr(a,field),getattr(b,field))

    def test_complete_sweep_sequence_parity(self):
        old=load_solver(ROOT/'solvers/experiments/pool_sa_fast.py')
        new=load_solver(ROOT/'solvers/experiments/refine_cached.py')
        rng=random.Random(413779)
        for _ in range(45):
            n,d,c,k=rng.randint(3,15),rng.choice((2,3)),rng.randint(2,6),rng.randint(1,40)
            initial,target=[[rng.randrange(c) for _ in range(size)] for size in (n*n+d*d,n*n)]
            indices,_,ops,_,_=old.build(n,d,target)
            actions=list(zip(indices,ops))
            sequence=[rng.randrange(len(ops)) for _ in range(rng.randrange(k+1))]
            self.assertEqual(old.refine(n,d,k,initial,target,actions,sequence,passes=3),
                             new.refine(n,d,k,initial,target,actions,sequence,passes=3))


if __name__=='__main__':
    unittest.main()
