"""Canonical checks for deeper forward search and exact tentative undo."""
import importlib.util
from pathlib import Path
import random
import unittest

from tools.simulate import Instance, rotation_offsets, simulate

PATH = Path(__file__).resolve().parents[1] / 'solvers/experiments/forward_three.py'


def load_solver(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ForwardTests(unittest.TestCase):
    def test_forward_scalar_initialization_preserves_sweeps_and_sequences(self):
        old = load_solver(PATH.with_name('forward_coordinate_triple.py'))
        new = load_solver(PATH.with_name('forward_coordinate_triple_fast.py'))
        rng = random.Random(50189)
        for trial in range(35):
            n,d,c,k = rng.randint(3,8),rng.choice((2,3)),rng.randint(2,6),rng.randint(1,25)
            initial = [rng.randrange(c) for _ in range(n*n+d*d)]
            target = [rng.randrange(c) for _ in range(n*n)]
            indices,_,operations,_,_ = old.build(n,d,target)
            actions = list(zip(indices,operations))
            sequence = [rng.randrange(-1,len(actions)) for _ in range(k)]
            order = list(range(len(actions)))
            rng.shuffle(order)
            self.assertEqual(old.forward_sweep(n,d,initial,target,actions,sequence,order),
                             new.forward_sweep(n,d,initial,target,actions,sequence,order))
            self.assertEqual(old.forward_refine(n,d,k,initial,target,actions,sequence,passes=2),
                             new.forward_refine(n,d,k,initial,target,actions,sequence,passes=2))

    def test_forward_coordinate_choices_match_exhaustive_final_scoring(self):
        solver = load_solver(PATH.with_name('forward_coordinate_suffix.py'))
        rng = random.Random(532675)
        for trial in range(20):
            n,d,c,k = rng.randint(3,5),rng.choice((2,3)),rng.randint(2,6),rng.randint(3,9)
            a = [rng.randrange(c) for _ in range(n*n)]
            t = [rng.randrange(c) for _ in a]
            s = [rng.randrange(c) for _ in range(d*d)]
            instance = Instance(n,d,c,k,a,t,s)
            indices,_,operations,_,_ = solver.build(n,d,t)
            actions = list(zip(indices,operations))
            sequence = [rng.randrange(-1,len(actions)) for _ in range(k)]
            order = list(range(len(actions)))
            rng.shuffle(order)
            trace = []
            original_class = solver.RefineState
            class TrackingState(original_class):
                def best(self):
                    choice = super().best()
                    trace.append((self.grid+self.stamp,self.wishes+self.wstamp,choice))
                    return choice
            solver.RefineState = TrackingState
            try:
                actual = solver.forward_sweep(n,d,a+s,t,actions,sequence,order)
            finally:
                solver.RefineState = original_class
            def final_score(path):
                grid,_ = simulate(instance,[operations[aid] for aid in path if aid>=0])
                return sum(x==y for x,y in zip(grid,t))
            prefix = []
            for i,old in enumerate(sequence):
                suffix = sequence[i+1:]
                grid,stamp = simulate(instance,[operations[aid] for aid in prefix if aid>=0])
                wishes = t+[6]*(d*d)
                for aid in reversed(suffix):
                    if aid<0:
                        continue
                    x,y,r = operations[aid]
                    for j,(p,q) in enumerate(rotation_offsets(d,r)):
                        pos = (x+p)*n+y+q
                        wishes[pos],wishes[n*n+j] = wishes[n*n+j],wishes[pos]
                baseline = final_score(prefix+[-1]+suffix)
                expected = (-1,0)
                for aid in order:
                    gain = final_score(prefix+[aid]+suffix)-baseline
                    if gain>expected[1] or (expected[0]<0 and gain==expected[1]):
                        expected = (aid,gain)
                self.assertEqual(trace[i],(grid+stamp,wishes,expected))
                self.assertGreaterEqual(baseline+expected[1],final_score(prefix+[old]+suffix))
                prefix.append(expected[0])
            self.assertEqual(actual,prefix)
            self.assertGreaterEqual(final_score(actual),final_score(sequence))

    def test_forward_refinement_preserves_canonical_score_and_budget(self):
        solver = load_solver(PATH.with_name('forward_coordinate_suffix.py'))
        rng = random.Random(512874)
        for trial in range(35):
            n,d,c,k = rng.randint(3,8),rng.choice((2,3)),rng.randint(2,6),rng.randint(1,30)
            a = [rng.randrange(c) for _ in range(n*n)]
            t = [rng.randrange(c) for _ in a]
            s = [rng.randrange(c) for _ in range(d*d)]
            instance = Instance(n,d,c,k,a,t,s)
            indices,_,operations,_,_ = solver.build(n,d,t)
            actions = list(zip(indices,operations))
            sequence = [rng.randrange(len(actions)) for _ in range(rng.randint(0,k))]
            result = solver.forward_refine(n,d,k,a+s,t,actions,sequence,passes=2)
            before,_ = simulate(instance,[operations[aid] for aid in sequence])
            after,_ = simulate(instance,[operations[aid] for aid in result])
            self.assertLessEqual(len(result),k)
            self.assertGreaterEqual(sum(x==y for x,y in zip(after,t)),sum(x==y for x,y in zip(before,t)))

    def test_cached_strong_weighted_engine_matches_uncached_reference(self):
        old = load_solver(PATH.with_name('forward_weighted_refine_strong_floor.py'))
        new = load_solver(PATH.with_name('forward_weighted_refine_informed_strong.py'))
        rng = random.Random(469532)
        for trial in range(20):
            n,d,c,k = rng.randint(3,8),rng.choice((2,3)),rng.randint(2,6),rng.randint(3,20)
            initial = [rng.randrange(c) for _ in range(n*n+d*d)]
            target = [rng.randrange(c) for _ in range(n*n)]
            weights = [rng.randint(1,4) for _ in target]
            indices,_,operations,_,_ = old.build(n,d,target)
            actions = list(zip(indices,operations))
            order = list(range(len(actions)))
            rng.shuffle(order)
            before = old.WeightedRefineState(n,d,initial,target,weights,actions,order)
            after = new.WeightedRefineState(n,d,initial,target,weights,actions,order)
            for step in range(15):
                aid,wishes = rng.randrange(len(actions)),bool(rng.randrange(2))
                before.apply(aid,wishes=wishes)
                after.apply(aid,wishes=wishes)
                self.assertEqual(before.best(),after.best())
                for attr in ('grid','stamp','wishes','wstamp','weights','wstamp_weights','counts'):
                    self.assertEqual(getattr(before,attr),getattr(after,attr))
            sequence = [rng.randrange(len(actions)) for _ in range(k)]
            self.assertEqual(old.weighted_refine(n,d,k,initial,target,weights,actions,sequence,passes=2),
                             new.weighted_refine(n,d,k,initial,target,weights,actions,sequence,passes=2))

    def test_weighted_geometry_cache_preserves_choices_and_sequences(self):
        old = load_solver(PATH.with_name('forward_weighted_refine_composite.py'))
        new = load_solver(PATH.with_name('forward_weighted_refine_cached.py'))
        rng = random.Random(318469)
        for trial in range(25):
            n,d,c,k = rng.randint(3,8),rng.choice((2,3)),rng.randint(2,6),rng.randint(3,20)
            initial = [rng.randrange(c) for _ in range(n*n+d*d)]
            target = [rng.randrange(c) for _ in range(n*n)]
            weights = [rng.randint(1,2) for _ in target]
            indices,_,operations,_,_ = old.build(n,d,target)
            actions = list(zip(indices,operations))
            order = list(range(len(actions)))
            rng.shuffle(order)
            before = old.WeightedRefineState(n,d,initial,target,weights,actions,order)
            after = new.WeightedRefineState(n,d,initial,target,weights,actions,order)
            for step in range(15):
                aid,wishes = rng.randrange(len(actions)),bool(rng.randrange(2))
                before.apply(aid,wishes=wishes)
                after.apply(aid,wishes=wishes)
                self.assertEqual(before.best(),after.best())
                for attr in ('grid','stamp','wishes','wstamp','weights','wstamp_weights','counts'):
                    self.assertEqual(getattr(before,attr),getattr(after,attr))
            sequence = [rng.randrange(len(actions)) for _ in range(k)]
            self.assertEqual(old.weighted_refine(n,d,k,initial,target,weights,actions,sequence,passes=2),
                             new.weighted_refine(n,d,k,initial,target,weights,actions,sequence,passes=2))

    def test_strong_weighted_bitplanes_cover_the_maximum_two_side_gain(self):
        solver = load_solver(PATH.with_name('forward_weighted_refine_strong_floor.py'))
        n,d = 6,3
        initial = [0]*(n*n)+[1]*(d*d)
        target = [0 if r<d and c<d else 1 for r in range(n) for c in range(n)]
        indices,_,operations,_,_ = solver.build(n,d,target)
        actions = list(zip(indices,operations))
        state = solver.WeightedRefineState(n,d,initial,target,[4]*(n*n),actions,list(range(len(actions))))
        state.apply(0,wishes=True)
        aid,gain = state.best()
        self.assertEqual(gain,8*d*d)
        before = sum(w*(a==b) for w,a,b in zip(state.weights+state.wstamp_weights,
                     state.grid+state.stamp,state.wishes+state.wstamp))
        x,y,r = operations[aid]
        changed = initial[:]
        for j,(p,q) in enumerate(rotation_offsets(d,r)):
            pos = (x+p)*n+y+q
            changed[pos],changed[n*n+j] = changed[n*n+j],changed[pos]
        after = sum(w*(a==b) for w,a,b in zip(state.weights+state.wstamp_weights,
                    changed,state.wishes+state.wstamp))
        self.assertEqual(after-before,gain)

    def test_strong_weighted_engine_preserves_original_weight_two_paths(self):
        old = load_solver(PATH.with_name('forward_weighted_refine_022.py'))
        new = load_solver(PATH.with_name('forward_weighted_refine_strong_floor.py'))
        rng = random.Random(362001)
        for trial in range(20):
            n,d,c,k = rng.randint(3,7),rng.choice((2,3)),rng.randint(2,6),rng.randint(3,20)
            initial = [rng.randrange(c) for _ in range(n*n+d*d)]
            target = [rng.randrange(c) for _ in range(n*n)]
            weights = [rng.randint(1,2) for _ in target]
            indices,_,operations,_,_ = old.build(n,d,target)
            actions = list(zip(indices,operations))
            order = list(range(len(actions)))
            rng.shuffle(order)
            before = old.WeightedRefineState(n,d,initial,target,weights,actions,order)
            after = new.WeightedRefineState(n,d,initial,target,weights,actions,order)
            for step in range(15):
                aid,wishes = rng.randrange(len(actions)),bool(rng.randrange(2))
                before.apply(aid,wishes=wishes)
                after.apply(aid,wishes=wishes)
                self.assertEqual(before.best(),after.best())
                for attr in ('grid','stamp','wishes','wstamp','weights','wstamp_weights','counts'):
                    self.assertEqual(getattr(before,attr),getattr(after,attr))
            sequence = [rng.randrange(len(actions)) for _ in range(k)]
            left = old.weighted_refine(n,d,k,initial,target,weights,actions,sequence,passes=2)
            right = new.weighted_refine(n,d,k,initial,target,weights,actions,sequence,passes=2)
            self.assertEqual(left,right)

    def test_strong_weighted_optimizer_matches_exhaustive_canonical_scoring(self):
        solver = load_solver(PATH.with_name('forward_weighted_refine_strong.py'))
        rng = random.Random(41576)
        for trial in range(25):
            n,d,c = rng.randint(3,6),rng.choice((2,3)),rng.randint(2,6)
            nn,dd = n*n,d*d
            actual = [rng.randrange(c) for _ in range(nn+dd)]
            target = [rng.randrange(c) for _ in range(nn)]
            weights = [rng.randint(1,4) for _ in target]
            indices,_,operations,_,_ = solver.build(n,d,target)
            actions = list(zip(indices,operations))
            order = list(range(len(actions)))
            rng.shuffle(order)
            state = solver.WeightedRefineState(n,d,actual,target,weights,actions,order)
            wishes,importance = target+[6]*dd,weights+[0]*dd
            def apply(values,aid):
                x,y,r = operations[aid]
                for j,(p,q) in enumerate(rotation_offsets(d,r)):
                    pos = (x+p)*n+y+q
                    values[pos],values[nn+j] = values[nn+j],values[pos]
            for step in range(12):
                baseline = sum(w*(a==b) for w,a,b in zip(importance,actual,wishes))
                expected = (-1,0)
                for aid in order:
                    changed = actual[:]
                    apply(changed,aid)
                    gain = sum(w*(a==b) for w,a,b in zip(importance,changed,wishes))-baseline
                    if gain>expected[1] or (expected[0]<0 and gain==expected[1]):
                        expected = (aid,gain)
                self.assertEqual(state.best(),expected)
                aid = rng.randrange(len(actions))
                if rng.randrange(2):
                    state.apply(aid,wishes=True)
                    apply(wishes,aid)
                    apply(importance,aid)
                else:
                    state.apply(aid)
                    apply(actual,aid)
                self.assertEqual(state.grid+state.stamp,actual)
                self.assertEqual(state.wishes+state.wstamp,wishes)
                self.assertEqual(state.weights+state.wstamp_weights,importance)

    def test_weighted_fast_apply_exactly_preserves_all_state_and_choices(self):
        old = load_solver(PATH.with_name('forward_weighted_refine_sa.py'))
        new = load_solver(PATH.with_name('forward_weighted_refine_sa_fast.py'))
        rng = random.Random(619517)
        for trial in range(30):
            n,d,c = rng.randint(3,8),rng.choice((2,3)),rng.randint(2,6)
            initial = [rng.randrange(c) for _ in range(n*n+d*d)]
            target = [rng.randrange(c) for _ in range(n*n)]
            weights = [rng.randint(1,2) for _ in target]
            indices,_,operations,_,_ = old.build(n,d,target)
            actions = list(zip(indices,operations))
            order = list(range(len(actions)))
            rng.shuffle(order)
            before = old.WeightedRefineState(n,d,initial,target,weights,actions,order)
            after = new.WeightedRefineState(n,d,initial,target,weights,actions,order)
            for step in range(20):
                aid,wishes = rng.randrange(len(actions)),bool(rng.randrange(2))
                before.apply(aid,wishes=wishes)
                after.apply(aid,wishes=wishes)
                self.assertEqual(before.__dict__,after.__dict__)
                self.assertEqual(before.best(),after.best())

    def test_weighted_wrapper_retains_unweighted_parent_floor(self):
        solver = load_solver(PATH.with_name('forward_weighted_refine.py'))
        rng = random.Random(107533)
        for n,d,c,k in ((5,2,3,3),(7,3,5,12),(9,2,4,18)):
            a = [rng.randrange(c) for _ in range(n*n)]
            t = [rng.randrange(c) for _ in range(n*n)]
            s = [rng.randrange(c) for _ in range(d*d)]
            instance = Instance(n,d,c,k,a,t,s)
            parent = solver.solve_weighted_parent(n,d,c,k,a[:],t,s[:])
            proposed = solver.solve(n,d,c,k,a[:],t,s[:])
            old,_ = simulate(instance,parent)
            new,_ = simulate(instance,proposed)
            self.assertGreaterEqual(sum(x==y for x,y in zip(new,t)),sum(x==y for x,y in zip(old,t)))

    def test_weighted_suffix_optimizer_matches_exhaustive_permutations(self):
        solver = load_solver(PATH.with_name('forward_weighted_refine.py'))
        rng = random.Random(734089)
        def apply(values,op,n,d):
            x,y,r = op
            for j,(p,q) in enumerate(rotation_offsets(d,r)):
                pos = (x+p)*n+y+q
                values[pos],values[n*n+j] = values[n*n+j],values[pos]
        for trial in range(35):
            n,d,c = rng.randint(3,7),rng.choice((2,3)),rng.randint(2,6)
            nn,dd = n*n,d*d
            initial = [rng.randrange(c) for _ in range(nn+dd)]
            target = [rng.randrange(c) for _ in range(nn)]
            weights = [rng.randint(1,2) for _ in range(nn)]
            indices,_,operations,_,_ = solver.build(n,d,target)
            actions = list(zip(indices,operations))
            order = list(range(len(actions)))
            rng.shuffle(order)
            state = solver.WeightedRefineState(n,d,initial,target,weights,actions,order)
            actual,wishes,importance = initial[:],target+[6]*dd,weights+[0]*dd
            for step in range(15):
                old_score = sum(w*(a==b) for w,a,b in zip(importance,actual,wishes))
                expected_action,expected_gain = -1,0
                for aid in order:
                    trial_state = actual[:]
                    apply(trial_state,operations[aid],n,d)
                    gain = sum(w*(a==b) for w,a,b in zip(importance,trial_state,wishes))-old_score
                    if gain>expected_gain or (expected_action<0 and gain==expected_gain):
                        expected_action,expected_gain = aid,gain
                self.assertEqual(state.best(),(expected_action,expected_gain))
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

    def test_weighted_refinement_preserves_its_final_cell_objective(self):
        solver = load_solver(PATH.with_name('forward_weighted_refine.py'))
        rng = random.Random(491899)
        for trial in range(30):
            n,d,c,k = rng.randint(3,7),rng.choice((2,3)),rng.randint(2,6),rng.randint(3,25)
            nn,dd = n*n,d*d
            initial = [rng.randrange(c) for _ in range(nn+dd)]
            target = [rng.randrange(c) for _ in range(nn)]
            weights = [rng.randint(1,2) for _ in range(nn)]
            indices,_,operations,_,_ = solver.build(n,d,target)
            actions = list(zip(indices,operations))
            sequence = [rng.randrange(len(actions)) for _ in range(rng.randint(0,k))]
            refined = solver.weighted_refine(n,d,k,initial,target,weights,actions,sequence,passes=2)
            instance = Instance(n,d,c,k,initial[:nn],target,initial[nn:])
            before,_ = simulate(instance,[operations[i] for i in sequence])
            after,_ = simulate(instance,[operations[i] for i in refined])
            self.assertLessEqual(len(refined),k)
            self.assertGreaterEqual(sum(w*(a==b) for w,a,b in zip(weights,after,target)),
                                    sum(w*(a==b) for w,a,b in zip(weights,before,target)))

    def test_prefix_rollouts_preserve_valid_best_prefixes(self):
        solver = load_solver(PATH.with_name('forward_rollout.py'))
        rng = random.Random(131871)
        for trial in range(20):
            n,d,c = rng.randint(3,8),rng.choice((2,3)),rng.randint(2,6)
            k = rng.randint(5,40)
            a = [rng.randrange(c) for _ in range(n*n)]
            t = [rng.randrange(c) for _ in range(n*n)]
            s = [rng.randrange(c) for _ in range(d*d)]
            instance = Instance(n,d,c,k,a,t,s)
            original = (a[:],t[:],s[:])
            operations = solver.prefix_rollout(n,d,c,k,a,t,s)
            self.assertEqual((a,t,s),original)
            self.assertLessEqual(len(operations),k)
            grid,_ = simulate(instance,operations)
            self.assertGreaterEqual(sum(x==y for x,y in zip(grid,t)),sum(x==y for x,y in zip(a,t)))
        for k in (24,25,40):
            n,d,c = 4,2,3
            a = [rng.randrange(c) for _ in range(n*n)]
            t = [rng.randrange(c) for _ in range(n*n)]
            s = [rng.randrange(c) for _ in range(d*d)]
            instance = Instance(n,d,c,k,a,t,s)
            parent = solver.solve_budget_parent(n,d,c,k,a[:],t,s[:])
            proposed = solver.solve(n,d,c,k,a[:],t,s[:])
            old,_ = simulate(instance,parent)
            new,_ = simulate(instance,proposed)
            self.assertGreaterEqual(sum(x==y for x,y in zip(new,t)),sum(x==y for x,y in zip(old,t)))
            if k <= 24:
                self.assertEqual(proposed,parent)

    def test_budget24_beam_preserves_parent_and_budget(self):
        solver = load_solver(PATH.with_name('forward_hybrid_budget24.py'))
        rng = random.Random(563813)
        for k in (13,24,25):
            n,d,c = 4,2,3
            a = [rng.randrange(c) for _ in range(n*n)]
            t = [rng.randrange(c) for _ in range(n*n)]
            s = [rng.randrange(c) for _ in range(d*d)]
            instance = Instance(n,d,c,k,a,t,s)
            parent = solver.solve_parent(n,d,c,k,a[:],t,s[:])
            proposed = solver.solve(n,d,c,k,a[:],t,s[:])
            self.assertLessEqual(len(proposed),k)
            parent_grid,_ = simulate(instance,parent)
            proposed_grid,_ = simulate(instance,proposed)
            self.assertGreaterEqual(sum(x==y for x,y in zip(proposed_grid,t)),sum(x==y for x,y in zip(parent_grid,t)))
            if k > 24:
                self.assertEqual(proposed,parent)

    def test_hybrid_beam_preserves_parent_score_and_large_budget_path(self):
        solver = load_solver(PATH.with_name('forward_hybrid_beam.py'))
        rng = random.Random(735113)
        for k in (1,2,3,5,8,12,13,20):
            n,d,c = 5,rng.choice((2,3)),rng.randint(2,6)
            a = [rng.randrange(c) for _ in range(n*n)]
            t = [rng.randrange(c) for _ in range(n*n)]
            s = [rng.randrange(c) for _ in range(d*d)]
            instance = Instance(n,d,c,k,a,t,s)
            parent = solver.solve_parent(n,d,c,k,a[:],t,s[:])
            proposed = solver.solve(n,d,c,k,a[:],t,s[:])
            parent_grid,_ = simulate(instance,parent)
            proposed_grid,_ = simulate(instance,proposed)
            self.assertGreaterEqual(sum(x==y for x,y in zip(proposed_grid,t)),sum(x==y for x,y in zip(parent_grid,t)))
            if k > 12:
                self.assertEqual(proposed,parent)

    def test_exact_two_matches_exhaustive_canonical_search(self):
        solver = load_solver(PATH.with_name('forward_exact_small.py'))
        rng = random.Random(375199)
        for trial in range(20):
            n,d,c = rng.randint(3,4),rng.choice((2,3)),rng.randint(2,6)
            a = [rng.randrange(c) for _ in range(n*n)]
            t = [rng.randrange(c) for _ in range(n*n)]
            s = [rng.randrange(c) for _ in range(d*d)]
            instance = Instance(n,d,c,2,a,t,s)
            operations = [(x,y,r) for x in range(n-d+1) for y in range(n-d+1) for r in range(4)]
            expected = sum(x==y for x,y in zip(a,t))
            for first in operations:
                grid,_ = simulate(instance,[first])
                expected = max(expected,sum(x==y for x,y in zip(grid,t)))
                for second in operations:
                    grid,_ = simulate(instance,[first,second])
                    expected = max(expected,sum(x==y for x,y in zip(grid,t)))
            proposed = solver.exact_two(n,d,c,2,a,t,s)
            grid,_ = simulate(instance,proposed)
            self.assertEqual(sum(x==y for x,y in zip(grid,t)),expected)

    def test_beam_clones_isolate_mutable_state_and_preserve_reference_score(self):
        solver = load_solver(PATH.with_name('forward_short_beam.py'))
        rng = random.Random(298177)
        for trial in range(10):
            n,d,c,k = rng.randint(3,7),rng.choice((2,3)),rng.randint(2,6),rng.randint(2,8)
            a = [rng.randrange(c) for _ in range(n*n)]
            t = [rng.randrange(c) for _ in range(n*n)]
            s = [rng.randrange(c) for _ in range(d*d)]
            instance = Instance(n,d,c,k,a,t,s)
            state = solver.State(n,d,c,a[:],t,s[:])
            before = (state.grid[:],state.stamp[:],state.counts[:],state.old_planes[:],state.stampmask)
            child = solver.clone_state(state)
            aid = rng.randrange(len(state.actions))
            child.apply(aid)
            self.assertEqual(before,(state.grid,state.stamp,state.counts,state.old_planes,state.stampmask))
            grid,stamp = simulate(instance,[state.actions[aid][1]])
            self.assertEqual((child.grid,child.stamp),(grid,stamp))
            self.assertIs(child.target_bits,state.target_bits)
            beam = solver.finite_beam(n,d,c,k,a,t,s)
            beam_grid,_ = simulate(instance,beam)
            self.assertLessEqual(len(beam),k)
            self.assertGreaterEqual(sum(x==y for x,y in zip(beam_grid,t)),sum(x==y for x,y in zip(a,t)))
            reference = solver.solve_reference(n,d,c,k,a[:],t,s[:])
            proposed = solver.solve(n,d,c,k,a[:],t,s[:])
            old_grid,_ = simulate(instance,reference)
            new_grid,_ = simulate(instance,proposed)
            self.assertGreaterEqual(sum(x==y for x,y in zip(new_grid,t)),sum(x==y for x,y in zip(old_grid,t)))

    def test_productive_beam_restores_state_and_selects_positive_first_move(self):
        solver = load_solver(PATH.with_name('forward_productive_three.py'))
        rng = random.Random(48221)
        for trial in range(50):
            n,d,c = rng.randint(3,9),rng.choice((2,3)),rng.randint(2,6)
            a = [rng.randrange(c) for _ in range(n*n)]
            t = [rng.randrange(c) for _ in range(n*n)]
            s = [rng.randrange(c) for _ in range(d*d)]
            state = solver.ProductiveState(n,d,c,a[:],t,s[:])
            before = (state.grid[:],state.stamp[:],state.counts[:],state.old_planes[:],state.stampmask)
            action = state.beam_step(rng)
            self.assertEqual(before,(state.grid,state.stamp,state.counts,state.old_planes,state.stampmask))
            if action is not None:
                instance = Instance(n,d,c,1,a,t,s)
                grid,_ = simulate(instance,[state.actions[action][1]])
                self.assertGreater(sum(x==y for x,y in zip(grid,t)),sum(x==y for x,y in zip(a,t)))

    def test_walk_search_restores_state_and_keeps_improving_prefix(self):
        solver = load_solver(PATH.with_name('forward_walk.py'))
        rng = random.Random(193756)
        improvements = 0
        for trial in range(50):
            n,d,c = rng.randint(3,9),rng.choice((2,3)),rng.randint(2,6)
            a = [rng.randrange(c) for _ in range(n*n)]
            t = [rng.randrange(c) for _ in range(n*n)]
            s = [rng.randrange(c) for _ in range(d*d)]
            instance = Instance(n,d,c,180,a,t,s)
            state = solver.State(n,d,c,a[:],t,s[:])
            before = (state.grid[:],state.stamp[:],state.counts[:],state.old_planes[:],state.stampmask)
            remaining = rng.randint(4,30)
            path = state.walk_tail(rng,remaining)
            after = (state.grid,state.stamp,state.counts,state.old_planes,state.stampmask)
            self.assertEqual(before,after)
            if path is not None:
                improvements += 1
                self.assertLessEqual(len(path),remaining)
                operations = [state.actions[aid][1] for aid in path]
                grid,stamp = simulate(instance,operations)
                self.assertGreater(sum(x==y for x,y in zip(grid,t)),sum(x==y for x,y in zip(a,t)))
                for aid in path:
                    state.apply(aid)
                self.assertEqual(state.grid,grid)
                self.assertEqual(state.stamp,stamp)
        self.assertGreater(improvements,0)

    def test_depth_three_search_restores_state_and_reports_real_gain(self):
        solver = load_solver(PATH)
        rng = random.Random(737031)
        triples = 0
        for trial in range(100):
            n, d, c = rng.randint(3, 9), rng.choice((2, 3)), rng.randint(2, 6)
            a = [rng.randrange(c) for _ in range(n*n)]
            t = [rng.randrange(c) for _ in range(n*n)]
            s = [rng.randrange(c) for _ in range(d*d)]
            instance = Instance(n, d, c, 180, a, t, s)
            state = solver.State(n,d,c,a[:],t,s[:])
            before = (state.grid[:],state.stamp[:],state.counts[:],state.old_planes[:],state.stampmask)
            path = state.escape_three(rng)
            after = (state.grid,state.stamp,state.counts,state.old_planes,state.stampmask)
            self.assertEqual(before, after)
            if path is not None:
                triples += 1
                self.assertEqual(len(path), 3)
                operations = [state.actions[aid][1] for aid in path]
                grid, stamp = simulate(instance, operations)
                self.assertGreater(sum(x==y for x,y in zip(grid,t)),sum(x==y for x,y in zip(a,t)))
                gain = 0
                for aid in path:
                    gain += state.gain(aid)
                    state.apply(aid)
                self.assertEqual(state.grid, grid)
                self.assertEqual(state.stamp, stamp)
                self.assertEqual(gain,sum(x==y for x,y in zip(grid,t))-sum(x==y for x,y in zip(a,t)))
        self.assertGreater(triples, 0)

    def test_solver_respects_budget_and_preserves_initial_score(self):
        rng = random.Random(104491)
        for filename in ('forward_three.py','forward_walk_three.py'):
            solver = load_solver(PATH.with_name(filename))
            for k in (1,2,3,4,10,30):
                n,d,c = 5,3,4
                a = [rng.randrange(c) for _ in range(n*n)]
                t = [rng.randrange(c) for _ in range(n*n)]
                s = [rng.randrange(c) for _ in range(d*d)]
                instance = Instance(n,d,c,k,a,t,s)
                operations = solver.solve(n,d,c,k,a[:],t,s[:])
                self.assertLessEqual(len(operations), k)
                grid,_ = simulate(instance,operations)
                self.assertGreaterEqual(sum(x==y for x,y in zip(grid,t)),sum(x==y for x,y in zip(a,t)))


if __name__ == '__main__':
    unittest.main()
