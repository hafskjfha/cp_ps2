"""Independent final-score checks for backward-target sequence refinement."""
import importlib.util
from pathlib import Path
import random
import unittest

from tools.simulate import Instance, simulate, match_count

ROOT = Path(__file__).resolve().parents[1]


class SequenceTests(unittest.TestCase):
    def load_solver(self, name='sequence_refine'):
        path = ROOT / ('solvers/experiments/'+name+'.py')
        self.assertTrue(path.exists(), 'sequence refinement solver must exist')
        spec = importlib.util.spec_from_file_location('sequence_refine', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_replacement_gain_matches_full_suffix_simulation(self):
        solver = self.load_solver()
        rng = random.Random(44129)
        for _ in range(24):
            n, d, c = rng.randint(3, 7), rng.choice((2, 3)), rng.randint(2, 6)
            a = [rng.randrange(c) for _ in range(n*n)]
            t = [rng.randrange(c) for _ in range(n*n)]
            s = [rng.randrange(c) for _ in range(d*d)]
            instance = Instance(n,d,c,180,a,t,s)
            actions = solver.build_actions(n,d)
            suffix_ids = [rng.randrange(len(actions)) for _ in range(9)]
            suffix = [actions[i][1] for i in suffix_ids]
            wishes = t + [-1]*(d*d)
            for i in reversed(suffix_ids):
                solver.transition(wishes,n*n,actions[i][0])
            best_id, gain = solver.best_action(a+s,wishes,actions,n*n,d*d)
            base = match_count(instance, simulate(instance,suffix)[0])
            chosen = suffix if best_id < 0 else [actions[best_id][1]]+suffix
            self.assertEqual(base+gain, match_count(instance,simulate(instance,chosen)[0]))
            actual_best = max([base]+[match_count(instance,simulate(instance,[op]+suffix)[0])
                                      for _,op in actions])
            self.assertEqual(base+gain,actual_best)

    def test_refinement_never_loses_greedy_score(self):
        solver = self.load_solver()
        rng = random.Random(84391)
        for _ in range(24):
            n,d,c,k = rng.randint(3,8),rng.choice((2,3)),rng.randint(2,6),rng.randint(1,25)
            a = [rng.randrange(c) for _ in range(n*n)]
            t = [rng.randrange(c) for _ in range(n*n)]
            s = [rng.randrange(c) for _ in range(d*d)]
            instance = Instance(n,d,c,k,a,t,s)
            actions = solver.build_actions(n,d)
            ids = solver.greedy(n,d,k,a,t,s,actions)
            old = [actions[i][1] for i in ids]
            found = solver.solve(n,d,c,k,a[:],t,s[:])
            self.assertLessEqual(len(found),k)
            self.assertGreaterEqual(match_count(instance,simulate(instance,found)[0]),
                                    match_count(instance,simulate(instance,old)[0]))

    def test_combination_preserves_lookahead_score(self):
        self.assert_constructor_preserved('sequence_lookahead')

    def test_random_plateau_preserves_lookahead_score(self):
        self.assert_constructor_preserved('sequence_plateau')

    def test_portfolio_refinement_preserves_constructor_score(self):
        self.assert_constructor_preserved('sequence_portfolio')

    def test_three_way_refinement_preserves_constructor_score(self):
        self.assert_constructor_preserved('sequence_portfolio3')

    def test_final_three_way_refinement_preserves_constructor_score(self):
        self.assert_constructor_preserved('sequence_portfolio3_four')

    def test_final_replacement_gain_matches_canonical(self):
        solver = self.load_solver('sequence_portfolio3_four')
        rng = random.Random(971641)
        for _ in range(20):
            n,d,c = rng.randint(3,8),rng.choice((2,3)),rng.randint(2,6)
            a = [rng.randrange(c) for _ in range(n*n)]
            t = [rng.randrange(c) for _ in range(n*n)]
            s = [rng.randrange(c) for _ in range(d*d)]
            instance = Instance(n,d,c,180,a,t,s)
            indices,_,ops,_,_ = solver.build(n,d,t)
            actions = list(zip(indices,ops))
            suffix_ids = [rng.randrange(len(actions)) for _ in range(9)]
            suffix = [actions[i][1] for i in suffix_ids]
            wishes = t+[-1]*(d*d)
            for i in reversed(suffix_ids):
                solver.seq_transition(wishes,n*n,actions[i][0])
            aid,gain = solver.best_action(a+s,wishes,actions,n*n,d*d,allow_zero=True)
            base = match_count(instance,simulate(instance,suffix)[0])
            selected = suffix if aid < 0 else [actions[aid][1]]+suffix
            self.assertEqual(base+gain,match_count(instance,simulate(instance,selected)[0]))
            best = max([base]+[match_count(instance,simulate(instance,[op]+suffix)[0])
                               for _,op in actions])
            self.assertEqual(best,base+gain)

    def assert_constructor_preserved(self, name):
        solver = self.load_solver(name)
        rng = random.Random(90143)
        for _ in range(20):
            n,d,c,k = rng.randint(3,8),rng.choice((2,3)),rng.randint(2,6),rng.randint(1,30)
            a = [rng.randrange(c) for _ in range(n*n)]
            t = [rng.randrange(c) for _ in range(n*n)]
            s = [rng.randrange(c) for _ in range(d*d)]
            instance = Instance(n,d,c,k,a,t,s)
            old = solver.construct(n,d,c,k,a[:],t,s[:])
            found = solver.solve(n,d,c,k,a[:],t,s[:])
            self.assertLessEqual(len(found),k)
            self.assertGreaterEqual(match_count(instance,simulate(instance,found)[0]),
                                    match_count(instance,simulate(instance,old)[0]))


if __name__ == '__main__':
    unittest.main()
