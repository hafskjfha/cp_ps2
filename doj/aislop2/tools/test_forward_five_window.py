"""Canonical five-operation boundary, optimization, and retention checks."""
import copy
import random
import unittest

from tools.test_solver import ROOT, load_solver
from tools.simulate import Instance, simulate, match_count, rotation_offsets


class FiveWindowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.solver = load_solver(ROOT/'solvers/experiments/forward_five_window_039.py')

    def test_boundaries_delta_restoration_and_none_counts(self):
        solver = self.solver
        rng = random.Random(814293)
        for _ in range(35):
            n,d,c,k = rng.randint(3,8),rng.choice((2,3)),rng.randint(2,6),rng.randint(5,18)
            a,t,s = [[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
            indices,_,ops,_,_ = solver.build(n,d,t)
            actions = list(zip(indices,ops))
            sequence = [rng.randrange(-1,len(actions)) for _ in range(k)]
            order = list(range(len(actions))); rng.shuffle(order)
            walker = solver.FiveWindowWalker(n,d,a+s,t,actions,sequence,order)
            case = Instance(n,d,c,k,a,t,s)
            for step in range(12):
                pos = rng.randrange(k-4)
                walker.move(pos)
                grid,stamp = simulate(case,[ops[x] for x in walker.sequence[:pos] if x>=0])
                wishes = t+[6]*(d*d)
                for aid in reversed(walker.sequence[pos+5:]):
                    if aid>=0:
                        x,y,r = ops[aid]
                        for j,(u,v) in enumerate(rotation_offsets(d,r)):
                            p = (x+u)*n+y+v
                            wishes[p],wishes[n*n+j] = wishes[n*n+j],wishes[p]
                self.assertEqual(walker.state.grid+walker.state.stamp,grid+stamp)
                self.assertEqual(walker.state.wishes+walker.state.wstamp,wishes)
                self.assertEqual(walker.boundary_score,sum(x==y for x,y in zip(grid+stamp,wishes)))
                self.assertIsNone(walker.state.counts)
                before = copy.deepcopy(walker.state.__dict__)
                first,last = rng.randrange(-1,len(actions)),rng.randrange(-1,len(actions))
                left = [walker.sequence[pos+1],rng.randrange(-1,len(actions))]
                right = [walker.sequence[pos+3],rng.randrange(-1,len(actions))]
                window,delta = walker.propose(first,last,left,right)
                self.assertEqual(walker.state.__dict__,before)
                old = match_count(case,simulate(case,[ops[x] for x in walker.sequence if x>=0])[0])
                candidate = walker.sequence[:pos]+list(window)+walker.sequence[pos+5:]
                new = match_count(case,simulate(case,[ops[x] for x in candidate if x>=0])[0])
                self.assertEqual(walker.score,old)
                self.assertEqual(delta,new-old)
                if rng.randrange(2):
                    walker.accept(window,delta)
                    self.assertEqual(walker.score,new)

    def test_central_triple_matches_constrained_exhaustive_search(self):
        solver = self.solver
        rng = random.Random(738421)
        for _ in range(25):
            n,d,c,k = rng.randint(3,5),rng.choice((2,3)),rng.randint(2,6),7
            a,t,s = [[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
            indices,_,ops,_,_ = solver.build(n,d,t)
            actions = list(zip(indices,ops))
            sequence = [rng.randrange(-1,len(actions)) for _ in range(k)]
            walker = solver.FiveWindowWalker(n,d,a+s,t,actions,sequence,list(range(len(actions))))
            walker.move(1)
            first,last = rng.randrange(-1,len(actions)),rng.randrange(-1,len(actions))
            left = [sequence[2],rng.randrange(-1,len(actions))]
            right = [sequence[4],rng.randrange(-1,len(actions))]
            result,delta = walker.propose(first,last,left,right)
            case = Instance(n,d,c,k,a,t,s)
            def score(middle):
                path=sequence[:1]+[first]+list(middle)+[last]+sequence[6:]
                return match_count(case,simulate(case,[ops[x] for x in path if x>=0])[0])
            expected = score(sequence[2:5])
            for second in left:
                for fourth in right:
                    for third in range(-1,len(actions)):
                        expected = max(expected,score((second,third,fourth)))
            self.assertEqual(score(result[1:4]),expected)

    def test_annealing_returns_best_visited_true_score(self):
        solver = self.solver
        original = solver.FiveWindowWalker
        accepted = []
        class TrackingWalker(original):
            def accept(self,window,delta):
                super().accept(window,delta)
                accepted.append((delta,self.score))
        solver.FiveWindowWalker = TrackingWalker
        rng = random.Random(517824)
        negative = 0
        try:
            for trial in range(10):
                n,d,c,k = 5,2+trial%2,3,12
                a,t,s = [[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
                indices,_,ops,_,_ = solver.build(n,d,t)
                actions = list(zip(indices,ops))
                sequence = [rng.randrange(len(actions)) for _ in range(k)]
                case = Instance(n,d,c,k,a,t,s)
                baseline = match_count(case,simulate(case,[ops[x] for x in sequence])[0])
                accepted.clear()
                result = solver.repair_five_windows(n,d,k,a+s,t,actions,sequence,proposals=120)
                final = match_count(case,simulate(case,[ops[x] for x in result])[0])
                self.assertEqual(final,max([baseline]+[score for _,score in accepted]))
                self.assertLessEqual(len(result),k)
                negative += sum(delta<0 for delta,_ in accepted)
        finally:
            solver.FiveWindowWalker = original
        self.assertGreater(negative,0)

    def test_complete_wrapper_preserves_parent_inputs_floor_and_budget(self):
        solver = self.solver
        parent = solver.solve_five_parent
        rng = random.Random(826547)
        try:
            for _ in range(15):
                n,d,c,k = rng.randint(3,7),rng.choice((2,3)),rng.randint(2,6),rng.randint(5,15)
                a,t,s = [[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
                _,_,ops,_,_ = solver.build(n,d,t)
                reference = [rng.choice(ops) for _ in range(rng.randint(1,k))]
                solver.solve_five_parent = lambda *args: reference[:]
                case = Instance(n,d,c,k,a[:],t[:],s[:])
                result = solver.solve(n,d,c,k,a,t,s)
                self.assertLessEqual(len(result),k)
                self.assertEqual((a,t,s),(case.a,case.t,case.s))
                self.assertGreaterEqual(match_count(case,simulate(case,result)[0]),
                                        match_count(case,simulate(case,reference)[0]))
        finally:
            solver.solve_five_parent = parent


if __name__=='__main__':
    unittest.main()
