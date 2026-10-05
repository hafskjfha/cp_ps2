"""Exact-equivalence checks for consolidation of the 028 solver core."""
import importlib.util
from pathlib import Path
import random
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SlimTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old=load('route_old028','submissions/best_028_251305191.py')
        cls.new=load('route_slim028','solvers/experiments/route_core028_slim.py')

    def test_refine_state_all_fields_and_best(self):
        rng=random.Random(25839101)
        for trial in range(35):
            n,d,c=rng.randint(3,10),rng.choice((2,3)),rng.randint(2,6)
            a,t,s=[[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
            indices,_,ops,_,_=self.old.build(n,d,t)
            actions=list(zip(indices,ops));order=list(range(len(ops)));rng.shuffle(order)
            for weighted in (False,True):
                if weighted:
                    weights=[rng.randrange(1,3) for _ in t]
                    args=(n,d,a+s,t,weights,actions,order)
                    old,new=self.old.WeightedRefineState(*args),self.new.WeightedRefineState(*args)
                else:
                    args=(n,d,a+s,t,actions,order)
                    old,new=self.old.RefineState(*args),self.new.RefineState(*args)
                self.assertEqual(old.__dict__,new.__dict__)
                for _ in range(20):
                    self.assertEqual(old.best(),new.best())
                    aid,wishes=rng.randrange(len(ops)),bool(rng.randrange(2))
                    old.apply(aid,wishes);new.apply(aid,wishes)
                    self.assertEqual(old.__dict__,new.__dict__)

    def test_productive_and_base_escape_equivalence(self):
        rng=random.Random(815616)
        for trial in range(20):
            n,d,c=rng.randint(3,8),rng.choice((2,3)),rng.randint(2,6)
            a,t,s=[[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
            for name in ('State','ProductiveState'):
                old,new=getattr(self.old,name)(n,d,c,a[:],t,s[:]),getattr(self.new,name)(n,d,c,a[:],t,s[:])
                kwargs=dict(width=12)
                if name=='ProductiveState':kwargs['min_gain']=rng.randrange(-4,2)
                self.assertEqual(old.escape(random.Random(trial),**kwargs),new.escape(random.Random(trial),**kwargs))
                self.assertEqual(old.__dict__,new.__dict__)

    def test_small_complete_solver_equivalence(self):
        rng=random.Random(38774)
        for _ in range(8):
            n,d,c,k=3,rng.choice((2,3)),rng.randint(2,6),rng.randint(1,8)
            a,t,s=[[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
            self.assertEqual(self.old.solve(n,d,c,k,a[:],t,s[:]),self.new.solve(n,d,c,k,a[:],t,s[:]))


if __name__=='__main__':unittest.main()
