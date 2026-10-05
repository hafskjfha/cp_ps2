"""Canonical tests for weighting isolated remaining errors."""
import random
import unittest

from tools.test_solver import ROOT, load_solver
from tools.simulate import Instance, simulate, match_count, rotation_offsets


class IsolatedWeightedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.solver = load_solver(ROOT/'solvers/experiments/forward_isolated_034.py')

    def test_mask_matches_independent_cardinal_definition(self):
        rng = random.Random(772045)
        for n in range(3,12):
            for _ in range(15):
                target = [rng.randrange(3) for _ in range(n*n)]
                final = [rng.randrange(3) for _ in target]
                wrong = {divmod(p,n) for p,(a,b) in enumerate(zip(final,target)) if a!=b}
                expected = []
                for x in range(n):
                    for y in range(n):
                        count = sum((x+dx,y+dy) in wrong for dx,dy in ((-1,0),(1,0),(0,-1),(0,1)))
                        expected.append(1+((x,y) in wrong and count<=1))
                self.assertEqual(self.solver.isolated_weights(n,final,target),expected)

    def test_isolated_weighted_optimizer_matches_canonical_actions(self):
        solver = self.solver
        rng = random.Random(798561)
        def apply(values,op,n,d):
            x,y,r = op
            for j,(p,q) in enumerate(rotation_offsets(d,r)):
                pos = (x+p)*n+y+q
                values[pos],values[n*n+j] = values[n*n+j],values[pos]
        for _ in range(35):
            n,d,c = rng.randint(3,7),rng.choice((2,3)),rng.randint(2,6)
            nn,dd = n*n,d*d
            initial = [rng.randrange(c) for _ in range(nn+dd)]
            target = [rng.randrange(c) for _ in range(nn)]
            weights = solver.isolated_weights(n,initial,target)
            indices,_,operations,_,_ = solver.build(n,d,target)
            actions = list(zip(indices,operations))
            order = list(range(len(actions)))
            rng.shuffle(order)
            state = solver.WeightedRefineState(n,d,initial,target,weights,actions,order)
            actual,wishes,importance = initial[:],target+[6]*dd,weights+[0]*dd
            for step in range(12):
                old = sum(w*(a==b) for w,a,b in zip(importance,actual,wishes))
                expected = (-1,0)
                for aid in order:
                    changed = actual[:]
                    apply(changed,operations[aid],n,d)
                    gain = sum(w*(a==b) for w,a,b in zip(importance,changed,wishes))-old
                    if gain>expected[1] or (expected[0]<0 and gain==expected[1]):
                        expected = (aid,gain)
                self.assertEqual(state.best(),expected)
                aid = rng.randrange(len(actions))
                if rng.randrange(2):
                    state.apply(aid,wishes=True)
                    apply(wishes,operations[aid],n,d)
                    apply(importance,operations[aid],n,d)
                else:
                    state.apply(aid)
                    apply(actual,operations[aid],n,d)
                self.assertEqual(state.grid+state.stamp,actual)
                self.assertEqual(state.wishes+state.wstamp,wishes)
                self.assertEqual(state.weights+state.wstamp_weights,importance)

    def test_isolated_weighted_sweep_preserves_weighted_objective(self):
        solver = self.solver
        rng = random.Random(291784)
        for _ in range(50):
            n,d,c,k = rng.randint(3,8),rng.choice((2,3)),rng.randint(2,6),rng.randint(3,25)
            a,t,s = [[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
            indices,_,ops,_,_ = solver.build(n,d,t)
            sequence = [rng.randrange(len(ops)) for _ in range(rng.randint(1,k))]
            case = Instance(n,d,c,k,a,t,s)
            before,_ = simulate(case,[ops[i] for i in sequence])
            weights = solver.isolated_weights(n,before,t)
            result = solver.weighted_refine(n,d,k,a+s,t,weights,list(zip(indices,ops)),sequence)
            after,_ = simulate(case,[ops[i] for i in result])
            self.assertLessEqual(len(result),k)
            self.assertGreaterEqual(sum(w*(x==y) for w,x,y in zip(weights,after,t)),
                                    sum(w*(x==y) for w,x,y in zip(weights,before,t)))

    def test_wrapper_retains_true_parent_score_and_input(self):
        solver = self.solver
        rng = random.Random(243178)
        parent = solver.solve_isolated_parent
        try:
            for _ in range(40):
                n,d,c,k = rng.randint(3,8),rng.choice((2,3)),rng.randint(2,6),rng.randint(3,25)
                a,t,s = [[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
                _,_,ops,_,_ = solver.build(n,d,t)
                reference = [rng.choice(ops) for _ in range(k)]
                solver.solve_isolated_parent = lambda *args: reference[:]
                case = Instance(n,d,c,k,a[:],t[:],s[:])
                result = solver.solve(n,d,c,k,a,t,s)
                self.assertEqual((a,t,s),(case.a,case.t,case.s))
                self.assertLessEqual(len(result),k)
                self.assertGreaterEqual(match_count(case,simulate(case,result)[0]),
                                        match_count(case,simulate(case,reference)[0]))
        finally:
            solver.solve_isolated_parent = parent


if __name__=='__main__':
    unittest.main()
