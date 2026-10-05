import random
import unittest
from tools.test_solver import ROOT,load_solver
from tools.simulate import Instance,simulate,match_count


class MacroTests(unittest.TestCase):
    def test_general_conjugation_exact_gain_and_restoration(self):
        solver=load_solver(ROOT/'solvers/experiments/macro_append.py')
        rng=random.Random(314955)
        for _ in range(100):
            d=rng.choice((2,3));n=rng.randint(3,10);c=rng.randint(2,6)
            a,t,s=[[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
            indices,_,ops,_,_=solver.build(n,d,t)
            order=list(range(len(ops)));rng.shuffle(order)
            evaluator=solver.RefineState(n,d,a+s,t,list(zip(indices,ops)),order)
            fields=('grid','stamp','wishes','wstamp','counts','old_planes')
            before={name:getattr(evaluator,name)[:] for name in fields}
            gain,pair=solver.best_patch_exchange(evaluator,None,rng)
            self.assertEqual(before,{name:getattr(evaluator,name) for name in fields})
            fresh=solver.RefineState(n,d,a+s,t,list(zip(indices,ops)),order)
            self.assertEqual(evaluator.values,fresh.values)
            self.assertEqual(evaluator.goals,fresh.goals)
            if pair is not None:
                first,second=pair
                case=Instance(n,d,c,180,a,t,s)
                final,_=simulate(case,[ops[first],ops[second],ops[first]])
                self.assertEqual(match_count(case,final)-match_count(case,a),gain)

    def test_appended_macros_preserve_prefix_and_improve_score(self):
        solver=load_solver(ROOT/'solvers/experiments/macro_append.py')
        rng=random.Random(136088)
        for _ in range(45):
            n,d,c,k=rng.randint(3,8),rng.choice((2,3)),rng.randint(2,6),rng.randint(4,50)
            a,t,s=[[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
            indices,_,ops,_,_=solver.build(n,d,t)
            sequence=[rng.randrange(len(ops)) for _ in range(rng.randrange(k-2))]
            result=solver.finish_macros(n,d,k,a+s,t,list(zip(indices,ops)),sequence)
            self.assertEqual(result[:len(sequence)],sequence)
            case=Instance(n,d,c,k,a,t,s)
            old,_=simulate(case,[ops[x] for x in sequence])
            final,_=simulate(case,[ops[x] for x in result])
            self.assertGreaterEqual(match_count(case,final),match_count(case,old))

    def test_patch_exchange_delta_and_stamp_restore(self):
        solver=load_solver(ROOT/'solvers/experiments/macro_hybrid.py')
        rng=random.Random(83187)
        for _ in range(80):
            d=rng.choice((2,3));n=rng.randint(2*d,10);c=rng.randint(2,6)
            a,t,s=[[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
            indices,_,ops,_,_=solver.build(n,d,t)
            evaluator=solver.RefineState(n,d,a+s,t,list(zip(indices,ops)),list(range(len(ops))))
            allowed=solver.patch_allowed(n,d)
            before=match_count(Instance(n,d,c,180,a,t,s),a)
            gain,pair=solver.best_patch_exchange(evaluator,allowed,rng)
            self.assertEqual(evaluator.grid,a)
            self.assertEqual(evaluator.stamp,s)
            self.assertEqual(evaluator.wstamp,[6]*(d*d))
            if pair is not None:
                first,second=pair
                self.assertFalse(set(indices[first])&set(indices[second]))
                case=Instance(n,d,c,180,a,t,s)
                final,stamp=simulate(case,[ops[first],ops[second],ops[first]])
                self.assertEqual(stamp,s)
                self.assertEqual(match_count(case,final)-before,gain)

    def test_constructor_legality_and_score_floor(self):
        solver=load_solver(ROOT/'solvers/experiments/macro_hybrid.py')
        rng=random.Random(789122)
        for _ in range(24):
            n,d,c,k=rng.randint(3,10),rng.choice((2,3)),rng.randint(2,6),rng.randint(1,45)
            a,t,s=[[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
            case=Instance(n,d,c,k,a,t,s)
            ops=solver.solve_patch_exchange(n,d,c,k,a,t,s)
            final,_=simulate(case,ops)
            self.assertGreaterEqual(match_count(case,final),match_count(case,a))


if __name__ == '__main__':
    unittest.main()
