import random
import unittest
from tools.test_solver import ROOT,load_solver


class ColorBoundTests(unittest.TestCase):
    def test_conservation_bound_and_incremental_matches(self):
        solver=load_solver(ROOT/'solvers/experiments/color_bound_pair.py')
        rng=random.Random(782199)
        for _ in range(80):
            n,d,c=rng.randint(3,12),rng.choice((2,3)),rng.randint(2,6)
            a,t,s=[[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
            state=solver.State(n,d,c,a[:],t,s[:])
            upper=solver.color_bound(a+s,t)
            self.assertLessEqual(upper,n*n)
            for _ in range(30):
                action=rng.randrange(len(state.actions))
                state.apply(action)
                actual=sum(x==y for x,y in zip(state.grid,t))
                self.assertEqual(state.matches,actual)
                self.assertLessEqual(actual,upper)
                self.assertEqual(upper,solver.color_bound(state.grid+state.stamp,t))

    def test_initial_color_optimum_needs_no_operations(self):
        solver=load_solver(ROOT/'solvers/experiments/color_bound_pair.py')
        for n,d in ((3,2),(3,3),(30,2),(30,3)):
            target=[i%3 for i in range(n*n)]
            self.assertEqual(solver.solve(n,d,3,180,[0]*(n*n),target,[0]*(d*d)),[])


if __name__ == '__main__':
    unittest.main()
