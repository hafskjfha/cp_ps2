"""Refinement continuation and canonical score checks for constructor pools."""
import random
import unittest

from solvers.experiments import pool_two
from solvers.experiments import pool_bits_two, pool_all8
from solvers.experiments import pool_twosided16
from solvers.experiments import pool_hybrid
from solvers.experiments import pool_weighted
from solvers.experiments import pool_triple_weighted, pool_coverage
from solvers.experiments import pool_iterated_weighted
from solvers.experiments import pool_iterated_fast
from solvers.experiments import pool_sa_fast, pool_sa_refinefast, pool_sa_equal
from solvers.experiments import pool_sa_geometry
from solvers.experiments import pool_constructor_base, pool_constructor_undo
from submissions import best_018_250064691 as iterated_reference
from tools.simulate import Instance, simulate


class PoolTests(unittest.TestCase):
    def cases(self, count):
        rng = random.Random(9761603)
        for _ in range(count):
            n, d, c, k = rng.randint(3, 7), rng.choice((2, 3)), rng.randint(2, 6), rng.randint(1, 20)
            yield Instance(n,d,c,k,[rng.randrange(c) for _ in range(n*n)],
                           [rng.randrange(c) for _ in range(n*n)],
                           [rng.randrange(c) for _ in range(d*d)])

    def test_split_sweeps_match_uninterrupted_refinement(self):
        rng = random.Random(368190)
        for case in self.cases(32):
            indices, _, ops, _, _ = pool_two.build(case.n, case.d, case.t)
            actions = list(zip(indices, ops))
            sequence = [rng.randrange(len(actions)) for _ in range(case.k)]
            args = (case.n,case.d,case.k,case.a+case.s,case.t,actions)
            complete = pool_two.refine(*args, sequence[:], passes=8)
            first = pool_two.refine(*args, sequence[:], passes=2)
            split = pool_two.refine(*args, first, passes=6, offset=2)
            self.assertEqual(split, complete)
            accelerated = pool_bits_two.refine(*args, sequence[:], passes=2)
            accelerated = pool_bits_two.refine(*args, accelerated, passes=6, offset=2)
            self.assertEqual(accelerated, complete)

    def test_refinement_preserves_score_and_canonical_simulation(self):
        rng = random.Random(86291)
        for case in self.cases(32):
            indices, _, ops, _, _ = pool_two.build(case.n, case.d, case.t)
            actions = list(zip(indices, ops))
            sequence = [rng.randrange(len(actions)) for _ in range(case.k)]
            original = pool_two.sequence_score(case.a+case.s,case.t,actions,sequence)
            result = pool_two.refine(case.n,case.d,case.k,case.a+case.s,case.t,actions,sequence,passes=3)
            actual = pool_two.sequence_score(case.a+case.s,case.t,actions,result)
            grid, _ = simulate(case, [actions[aid][1] for aid in result])
            self.assertEqual(actual, sum(a==b for a,b in zip(grid,case.t)))
            self.assertGreaterEqual(actual, original)
            self.assertLessEqual(len(result), case.k)

    def test_full_pool_solver_is_legal_and_does_not_lose_initial_score(self):
        for case in self.cases(12):
            operations = pool_two.solve(case.n,case.d,case.c,case.k,case.a[:],case.t,case.s[:])
            final, _ = simulate(case, operations)
            self.assertGreaterEqual(sum(a==b for a,b in zip(final,case.t)),
                                    sum(a==b for a,b in zip(case.a,case.t)))

    def test_all_refined_paths_dominate_single_selected_constructor(self):
        for case in self.cases(12):
            args = (case.n,case.d,case.c,case.k,case.a[:],case.t,case.s[:])
            raw_pool = pool_all8.construct(*args)
            indices, _, ops, _, _ = pool_all8.build(case.n, case.d, case.t)
            actions = list(zip(indices, ops))
            width = case.n-case.d+1
            original = [(x*width+y)*4+r for x,y,r in raw_pool[0][1]]
            original = pool_all8.refine(case.n,case.d,case.k,case.a+case.s,case.t,actions,original)
            baseline = pool_all8.sequence_score(case.a+case.s,case.t,actions,original)
            result = pool_all8.solve(*args)
            final, _ = simulate(case, result)
            self.assertGreaterEqual(sum(a==b for a,b in zip(final,case.t)),baseline)

    def test_forward_bitsets_match_scalar_suffix_wishes(self):
        rng = random.Random(710214)
        for case in self.cases(48):
            nn,dd = case.n*case.n,case.d*case.d
            indices, _, ops, _, _ = pool_two.build(case.n,case.d,case.t)
            actions = list(zip(indices,ops))
            sequence = [rng.randrange(len(actions)) for _ in range(case.k)]
            order = list(range(len(actions)))
            rng.shuffle(order)
            suffix = [None]*(len(sequence)+1)
            suffix[-1] = case.t+[6]*dd
            for i in range(len(sequence)-1,-1,-1):
                suffix[i] = suffix[i+1][:]
                pool_two.seq_transition(suffix[i],nn,actions[sequence[i]][0])
            state, expected = case.a+case.s,[]
            ordered = [actions[aid] for aid in order]
            for i in range(len(sequence)):
                chosen,_ = pool_two.best_action(state,suffix[i+1],ordered,nn,dd,allow_zero=True)
                if chosen>=0:
                    chosen = order[chosen]
                    expected.append(chosen)
                    pool_two.seq_transition(state,nn,actions[chosen][0])
            result = pool_twosided16.forward_sweep(case.n,case.d,case.a+case.s,case.t,actions,sequence[:],order)
            self.assertEqual(result,expected)
            before = pool_two.sequence_score(case.a+case.s,case.t,actions,sequence)
            after = pool_two.sequence_score(case.a+case.s,case.t,actions,result)
            canonical,_ = simulate(case,[actions[aid][1] for aid in result])
            self.assertEqual(after,sum(a==b for a,b in zip(canonical,case.t)))
            self.assertGreaterEqual(after,before)

    def test_hybrid_incremental_replacement_scores_match_canonical(self):
        rng = random.Random(870462)
        for case in self.cases(24):
            nn = case.n*case.n
            indices, _, ops, _, _ = pool_hybrid.build(case.n,case.d,case.t)
            actions = list(zip(indices,ops))
            sequence = [rng.randrange(len(actions)) for _ in range(case.k)]
            state = pool_hybrid.SequenceState(case.a+case.s,case.t,actions,sequence,nn)
            for _ in range(10):
                span = rng.randint(1,min(2,case.k))
                position = rng.randrange(case.k-span+1)
                replacements = [rng.randrange(-1,len(actions)) for _ in range(span)]
                delta = state.delta(position,replacements)
                proposed = state.sequence[:]
                proposed[position:position+span] = replacements
                grid,stamp = simulate(case,[actions[aid][1] for aid in proposed if aid>=0])
                expected = sum(a==b for a,b in zip(grid,case.t))
                self.assertEqual(state.score+delta,expected)
                state.accept(position,replacements,delta)
                self.assertEqual(state.score,expected)
                self.assertEqual(state.prefix[-1],grid+stamp)

    def test_weighted_action_bitsets_and_swaps_match_scalar_model(self):
        rng = random.Random(827189)
        for trial in range(24):
            n,d,c = (3,7,30)[trial%3],rng.choice((2,3)),rng.randint(2,6)
            grid = [rng.randrange(c) for _ in range(n*n)]
            target = [rng.randrange(c) for _ in grid]
            stamp = [rng.randrange(c) for _ in range(d*d)]
            order = list(range(4*(n-d+1)**2))
            rng.shuffle(order)
            solver = (pool_weighted,pool_triple_weighted,pool_coverage)[(trial//4)%3]
            state = solver.WeightedState(n,d,c,grid[:],target,stamp[:],order)
            for _ in range(20):
                best_gain,best_action = -100,-1
                for action in order:
                    positions = state.actions[action][0]
                    gain = sum(state.weights[p]*((state.stamp[j]==target[p])-(state.grid[p]==target[p]))
                               for j,p in enumerate(positions))
                    if gain>best_gain:
                        best_gain,best_action = gain,action
                self.assertEqual(state.best(),(best_gain,best_action))
                chosen = rng.randrange(len(order))
                case = Instance(n,d,c,1,state.grid[:],target,state.stamp[:])
                expected = simulate(case,[state.actions[chosen][1]])
                state.apply(chosen)
                self.assertEqual((state.grid,state.stamp),expected)
                if hasattr(state,'matches'):
                    self.assertEqual(state.matches,sum(a==b for a,b in zip(state.grid,target)))

    def test_color_bound_stops_already_optimal_imperfect_grids(self):
        for d in (2,3):
            case = Instance(3,d,2,180,[0]*9,[0]*4+[1]*5,[0]*(d*d))
            self.assertEqual(pool_triple_weighted.color_bound(case.a+case.s,case.t),4)
            result = pool_triple_weighted.solve(case.n,case.d,case.c,case.k,case.a,case.t,case.s)
            self.assertEqual(result,[])

    def test_iterated_seed_changes_and_continuations_match_reference(self):
        rng = random.Random(768392)
        for case in self.cases(24):
            indices, _, ops, _, _ = pool_iterated_weighted.build(case.n,case.d,case.t)
            actions = list(zip(indices,ops))
            sequence = [rng.randrange(len(actions)) for _ in range(case.k)]
            args = (case.n,case.d,case.k,case.a+case.s,case.t,actions)
            seed_offset = rng.randrange(500000)
            expected = iterated_reference.refine(*args,sequence[:],passes=4,seed_offset=seed_offset)
            full = pool_iterated_weighted.refine(*args,sequence[:],passes=4,seed_offset=seed_offset)
            self.assertEqual(full,expected)
            split = pool_iterated_weighted.refine(*args,sequence[:],passes=2,seed_offset=seed_offset)
            split = pool_iterated_weighted.refine(*args,split,passes=2,offset=2,seed_offset=seed_offset)
            self.assertEqual(split,expected)
        for case in self.cases(6):
            operations = pool_iterated_weighted.solve(case.n,case.d,case.c,case.k,case.a[:],case.t,case.s[:])
            grid,_ = simulate(case,operations)
            self.assertLessEqual(len(operations),case.k)
            self.assertGreaterEqual(sum(a==b for a,b in zip(grid,case.t)),
                                    sum(a==b for a,b in zip(case.a,case.t)))

    def test_delta_accumulation_matches_region_rescanning(self):
        rng = random.Random(209642)
        for trial in range(30):
            n,d,c = (3,9,30)[trial%3],rng.choice((2,3)),rng.randint(2,6)
            grid = [rng.randrange(c) for _ in range(n*n)]
            target = [rng.randrange(c) for _ in grid]
            stamp = [rng.randrange(c) for _ in range(d*d)]
            order = list(range(4*(n-d+1)**2))
            rng.shuffle(order)
            name = ('State','WeightedState','ProductiveState')[(trial//3)%3]
            before = getattr(pool_iterated_weighted,name)(n,d,c,grid[:],target,stamp[:],order[:])
            after = getattr(pool_iterated_fast,name)(n,d,c,grid[:],target,stamp[:],order[:])
            for _ in range(30):
                action = rng.randrange(len(order))
                before.apply(action)
                after.apply(action)
                self.assertEqual(before.grid,after.grid)
                self.assertEqual(before.stamp,after.stamp)
                self.assertEqual(before.matches,after.matches)
                self.assertEqual(before.counts,after.counts)
                self.assertEqual(before.old_planes,after.old_planes)
                self.assertEqual(before.best(),after.best())

    def test_refinement_delta_accumulation_preserves_both_swaps(self):
        rng = random.Random(99215)
        for n,d,c in ((3,3,2),(9,2,6),(30,2,2),(30,3,2),(30,3,6)):
            initial = [rng.randrange(c) for _ in range(n*n+d*d)]
            target = [rng.randrange(c) for _ in range(n*n)]
            indices,_,ops,_,_ = pool_sa_fast.build(n,d,target)
            actions = list(zip(indices,ops))
            order = list(range(len(actions)))
            rng.shuffle(order)
            before = pool_sa_fast.RefineState(n,d,initial,target,actions,order)
            after = pool_sa_refinefast.RefineState(n,d,initial,target,actions,order)
            for _ in range(100):
                action,wishes = rng.randrange(len(actions)),bool(rng.randrange(2))
                before.apply(action,wishes)
                after.apply(action,wishes)
                for field in ('grid','stamp','wishes','wstamp','values','goals','counts','old_planes'):
                    self.assertEqual(getattr(before,field),getattr(after,field))
                self.assertEqual(before.best(),after.best())

    def test_full_board_stamp_shortcut_matches_exhaustive_rotation_oracle(self):
        rng = random.Random(788713)
        for trial in range(60):
            c,k = rng.randint(2,6),(1,2,3,180)[trial%4]
            case = Instance(3,3,c,k,[rng.randrange(c) for _ in range(9)],
                            [rng.randrange(c) for _ in range(9)],
                            [rng.randrange(c) for _ in range(9)])
            possible = {tuple(case.a)}
            frontier = {(tuple(case.a),tuple(case.s))}
            for _ in range(min(k,4)):
                next_frontier = set()
                for grid,stamp in frontier:
                    node = Instance(3,3,c,1,list(grid),case.t,list(stamp))
                    for rotation in range(4):
                        final,buffer = simulate(node,[(0,0,rotation)])
                        possible.add(tuple(final))
                        next_frontier.add((tuple(final),tuple(buffer)))
                frontier = next_frontier
            expected = max(sum(a==b for a,b in zip(grid,case.t)) for grid in possible)
            operations = pool_sa_equal.solve(3,3,c,k,case.a[:],case.t,case.s[:])
            final,_ = simulate(case,operations)
            self.assertLessEqual(len(operations),min(k,2))
            self.assertEqual(sum(a==b for a,b in zip(final,case.t)),expected)

    def test_cached_constructor_geometry_preserves_independent_states(self):
        rng = random.Random(728144)
        for n,d,c in ((3,3,2),(9,2,6),(30,2,2),(30,3,2),(30,3,6)):
            target = [rng.randrange(c) for _ in range(n*n)]
            for _ in range(5):
                grid = [rng.randrange(c) for _ in range(n*n)]
                stamp = [rng.randrange(c) for _ in range(d*d)]
                order = list(range(4*(n-d+1)**2))
                rng.shuffle(order)
                before = pool_sa_fast.State(n,d,c,grid[:],target,stamp[:],order)
                after = pool_sa_geometry.State(n,d,c,grid[:],target,stamp[:],order)
                for _ in range(8):
                    action = rng.randrange(len(order))
                    before.apply(action)
                    after.apply(action)
                    self.assertEqual(before.__dict__,after.__dict__)
                    self.assertEqual(before.best(),after.best())

    def test_escape_snapshot_undo_preserves_pairs_rng_and_entire_state(self):
        rng = random.Random(812900)
        for trial in range(24):
            n,d,c = (3,9,30)[trial%3],rng.choice((2,3)),rng.randint(2,6)
            grid = [rng.randrange(c) for _ in range(n*n)]
            target = [rng.randrange(c) for _ in grid]
            stamp = [rng.randrange(c) for _ in range(d*d)]
            order = list(range(4*(n-d+1)**2))
            rng.shuffle(order)
            name = ('State','ProductiveState')[(trial//3)%2]
            before = getattr(pool_constructor_base,name)(n,d,c,grid[:],target,stamp[:],order)
            after = getattr(pool_constructor_undo,name)(n,d,c,grid[:],target,stamp[:],order)
            for _ in range(4):
                seed = rng.randrange(1000000)
                left,right = random.Random(seed),random.Random(seed)
                self.assertEqual(before.escape(left,width=16),after.escape(right,width=16))
                self.assertEqual(left.getstate(),right.getstate())
                self.assertEqual(before.__dict__,after.__dict__)
                action = rng.randrange(len(order))
                before.apply(action)
                after.apply(action)


if __name__ == '__main__':
    unittest.main()
