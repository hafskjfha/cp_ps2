"""Canonical tests of exact four-window state, proposals, and retention."""
import copy
import random
import unittest

from tools.test_solver import ROOT, load_solver
from tools.simulate import Instance, simulate, match_count, rotation_offsets


class FourWindowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.solver = load_solver(ROOT/'solvers/experiments/forward_four_window_035.py')

    def test_walker_boundaries_deltas_and_nested_restoration(self):
        solver = self.solver
        rng = random.Random(874221)
        for trial in range(35):
            n,d,c,k = rng.randint(3,8),rng.choice((2,3)),rng.randint(2,6),rng.randint(4,18)
            a,t,s = [[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
            indices,_,ops,_,_ = solver.build(n,d,t)
            actions = list(zip(indices,ops))
            order = list(range(len(actions)))
            rng.shuffle(order)
            sequence = [rng.randrange(-1,len(actions)) for _ in range(k)]
            case = Instance(n,d,c,k,a,t,s)
            walker = solver.FourWindowWalker(n,d,a+s,t,actions,sequence,order)
            for step in range(12):
                pos = rng.randrange(k-3)
                walker.move(pos)
                prefix_grid,prefix_stamp = simulate(case,[ops[aid] for aid in walker.sequence[:pos] if aid>=0])
                wishes = t+[6]*(d*d)
                for aid in reversed(walker.sequence[pos+4:]):
                    if aid>=0:
                        x,y,r = ops[aid]
                        for j,(u,v) in enumerate(rotation_offsets(d,r)):
                            p = (x+u)*n+y+v
                            wishes[p],wishes[n*n+j] = wishes[n*n+j],wishes[p]
                self.assertEqual(walker.state.grid+walker.state.stamp,prefix_grid+prefix_stamp)
                self.assertEqual(walker.state.wishes+walker.state.wstamp,wishes)
                self.assertEqual(walker.boundary_score,sum(x==y for x,y in zip(prefix_grid+prefix_stamp,wishes)))
                before = copy.deepcopy(walker.state.__dict__)
                first,last = rng.randrange(-1,len(actions)),rng.randrange(-1,len(actions))
                candidates = [(walker.sequence[pos+1],0),(walker.sequence[pos+2],1),(-1,0),(-1,1),
                              (rng.randrange(len(actions)),rng.randrange(2))]
                proposed,delta = walker.propose(first,last,candidates)
                self.assertEqual(walker.state.__dict__,before)
                old_score = match_count(case,simulate(case,[ops[x] for x in walker.sequence if x>=0])[0])
                changed = walker.sequence[:pos]+list(proposed)+walker.sequence[pos+4:]
                new_score = match_count(case,simulate(case,[ops[x] for x in changed if x>=0])[0])
                self.assertEqual(walker.score,old_score)
                self.assertEqual(delta,new_score-old_score)
                if rng.randrange(2):
                    walker.accept(proposed,delta)
                    self.assertEqual(walker.score,new_score)

    def test_middle_pair_choice_matches_exhaustive_allowed_search(self):
        solver = self.solver
        rng = random.Random(458277)
        for _ in range(25):
            n,d,c,k = rng.randint(3,5),rng.choice((2,3)),rng.randint(2,6),6
            a,t,s = [[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
            indices,_,ops,_,_ = solver.build(n,d,t)
            actions = list(zip(indices,ops))
            sequence = [rng.randrange(-1,len(actions)) for _ in range(k)]
            walker = solver.FourWindowWalker(n,d,a+s,t,actions,sequence,list(range(len(actions))))
            walker.move(1)
            first,last = rng.randrange(-1,len(actions)),rng.randrange(-1,len(actions))
            candidates = [(rng.randrange(-1,len(actions)),rng.randrange(2)) for _ in range(4)]
            result,delta = walker.propose(first,last,candidates)
            case = Instance(n,d,c,k,a,t,s)
            def score(middle):
                path=sequence[:1]+[first]+list(middle)+[last]+sequence[5:]
                return match_count(case,simulate(case,[ops[x] for x in path if x>=0])[0])
            expected = max(score(sequence[2:4]),score((-1,-1)))
            for fixed,side in candidates:
                for other in range(-1,len(actions)):
                    expected = max(expected,score((other,fixed) if side else (fixed,other)))
            self.assertEqual(score(result[1:3]),expected)

    def test_search_and_wrapper_keep_parent_floor_and_budget(self):
        solver = self.solver
        rng = random.Random(638981)
        parent = solver.solve_four_parent
        try:
            for _ in range(15):
                n,d,c,k = rng.randint(3,7),rng.choice((2,3)),rng.randint(2,6),rng.randint(4,14)
                a,t,s = [[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
                indices,_,ops,_,_ = solver.build(n,d,t)
                actions = list(zip(indices,ops))
                sequence = [rng.randrange(len(actions)) for _ in range(rng.randint(1,k))]
                case = Instance(n,d,c,k,a[:],t[:],s[:])
                reference = [ops[aid] for aid in sequence]
                before = match_count(case,simulate(case,reference)[0])
                result = solver.repair_four_windows(n,d,k,a+s,t,actions,sequence,proposals=30)
                self.assertLessEqual(len(result),k)
                self.assertGreaterEqual(match_count(case,simulate(case,[ops[x] for x in result])[0]),before)
                solver.solve_four_parent = lambda *args: reference[:]
                candidate = solver.solve(n,d,c,k,a,t,s)
                self.assertLessEqual(len(candidate),k)
                self.assertEqual((a,t,s),(case.a,case.t,case.s))
                self.assertGreaterEqual(match_count(case,simulate(case,candidate)[0]),before)
        finally:
            solver.solve_four_parent = parent


if __name__=='__main__':
    unittest.main()
