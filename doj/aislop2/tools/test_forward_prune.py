"""Canonical pruning and parent-floor tests for the modern sequence wrapper."""
import random
import unittest

from tools.test_solver import ROOT, load_solver
from tools.simulate import Instance, simulate, match_count


class ForwardPruningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.solver = load_solver(ROOT/'solvers/experiments/forward_prune_late.py')

    def test_pruned_subsequence_score_floor(self):
        solver = self.solver
        rng = random.Random(119859)
        for _ in range(150):
            n,d,c,k = rng.randint(3,12),rng.choice((2,3)),rng.randint(2,6),rng.randint(1,80)
            a,t,s = [[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
            indices,_,ops,_,_ = solver.build(n,d,t)
            sequence = [rng.randrange(len(ops)) for _ in range(k)]
            result = solver.prune_sequence(n*n,a+s,t,list(zip(indices,ops)),sequence)
            it = iter(sequence)
            self.assertTrue(all(any(x==aid for x in it) for aid in result))
            case = Instance(n,d,c,k,a,t,s)
            before,_ = simulate(case,[ops[x] for x in sequence])
            after,_ = simulate(case,[ops[x] for x in result])
            self.assertGreaterEqual(match_count(case,after),match_count(case,before))

    def test_pruning_decisions_match_canonical_removal_oracle(self):
        solver = self.solver
        rng = random.Random(185923)
        for _ in range(75):
            n,d,c,k = rng.randint(3,7),rng.choice((2,3)),rng.randint(2,6),rng.randint(1,20)
            a,t,s = [[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
            indices,_,ops,_,_ = solver.build(n,d,t)
            sequence = [rng.randrange(len(ops)) for _ in range(k)]
            case = Instance(n,d,c,k,a,t,s)
            def score(path):
                return match_count(case,simulate(case,[ops[x] for x in path])[0])
            expected = sequence[:]
            for i in range(k-1,-1,-1):
                without = expected[:i]+expected[i+1:]
                if score(without)>=score(expected):
                    expected = without
            actual = solver.prune_sequence(n*n,a+s,t,list(zip(indices,ops)),sequence)
            self.assertEqual(actual,expected)

    def test_wrapper_preserves_parent_floor_and_input(self):
        solver = self.solver
        rng = random.Random(293148)
        parent = solver.solve_prune_parent
        try:
            for _ in range(30):
                n,d,c,k = rng.randint(3,7),rng.choice((2,3)),rng.randint(2,6),rng.randint(3,20)
                a,t,s = [[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
                _,_,ops,_,_ = solver.build(n,d,t)
                reference = [rng.choice(ops) for _ in range(k)]
                solver.solve_prune_parent = lambda *args: reference[:]
                case = Instance(n,d,c,k,a[:],t[:],s[:])
                result = solver.solve(n,d,c,k,a,t,s)
                self.assertEqual((a,t,s),(case.a,case.t,case.s))
                self.assertLessEqual(len(result),k)
                self.assertGreaterEqual(match_count(case,simulate(case,result)[0]),
                                        match_count(case,simulate(case,reference)[0]))
        finally:
            solver.solve_prune_parent = parent

    def test_wrapper_rejects_worse_cleanup_and_preserves_ties(self):
        solver = self.solver
        parent,prune,refine = solver.solve_prune_parent,solver.prune_sequence,solver.refine
        try:
            rng = random.Random(824312)
            for _ in range(30):
                n,d,c,k = 5,2,3,8
                a,t,s = [[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
                _,_,ops,_,_ = solver.build(n,d,t)
                reference = [rng.choice(ops) for _ in range(k)]
                solver.solve_prune_parent = lambda *args: reference[:]
                solver.prune_sequence = lambda nn,initial,target,actions,sequence: sequence[:-1]
                solver.refine = lambda *args,**kwargs: []
                case = Instance(n,d,c,k,a,t,s)
                result = solver.solve(n,d,c,k,a,t,s)
                baseline = match_count(case,simulate(case,reference)[0])
                if match_count(case,a)<=baseline:
                    self.assertEqual(result,reference)
                else:
                    self.assertEqual(result,[])
        finally:
            solver.solve_prune_parent,solver.prune_sequence,solver.refine = parent,prune,refine


if __name__=='__main__':
    unittest.main()
