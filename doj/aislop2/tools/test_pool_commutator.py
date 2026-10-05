"""Canonical checks for one bounded four-operation commutator append."""
import random
import unittest
from unittest.mock import patch

from solvers.experiments import pool_commutator_append as candidate
from tools.simulate import Instance, simulate


class CommutatorTests(unittest.TestCase):
    def test_exact_union_delta_and_complete_restoration(self):
        rng = random.Random(2026092571)
        checked = 0
        for n, d in ((3, 2), (3, 3), (4, 3), (7, 2), (8, 3), (16, 3)):
            for c in (2, 6):
                grid = [rng.randrange(c) for _ in range(n*n)]
                stamp = [rng.randrange(c) for _ in range(d*d)]
                target = [rng.randrange(c) for _ in grid]
                indices, _, operations, _, _ = candidate.build(n, d, target)
                before_grid, before_stamp = grid[:], stamp[:]
                for _ in range(24):
                    first, second = rng.randrange(len(indices)), rng.randrange(len(indices))
                    touched = tuple(sorted(set(indices[first]) | set(indices[second])))
                    for left, right in ((first, second), (second, first)):
                        word = (left, right, left, right)
                        gain = candidate.commutator_word_gain(grid, target, stamp,
                                                             indices, word, touched)
                        final, _ = simulate(Instance(n,d,c,4,before_grid,target,before_stamp),
                                            [operations[aid] for aid in word])
                        expected = sum(a==b for a,b in zip(final,target)) - sum(
                            a==b for a,b in zip(before_grid,target))
                        self.assertEqual(gain, expected)
                        self.assertEqual(grid, before_grid)
                        self.assertEqual(stamp, before_stamp)
                        checked += 1
        self.assertEqual(checked, 576)

    def test_bounded_tail_is_deterministic_legal_and_monotone(self):
        rng = random.Random(2026092572)
        for trial in range(16):
            n, d, c = 3 + trial % 3, 2 + trial % 2, 2 + trial % 5
            grid = [rng.randrange(c) for _ in range(n*n)]
            stamp = [rng.randrange(c) for _ in range(d*d)]
            target = grid[:]
            for _ in range(min(8,n*n)):
                target[rng.randrange(n*n)] = rng.randrange(c)
            indices, _, operations, _, _ = candidate.build(n,d,target)
            before = grid[:], stamp[:]
            args = (n,d,grid,target,stamp,indices,trial+7001)
            first = candidate.commutator_tail(*args, pair_limit=128)
            second = candidate.commutator_tail(*args, pair_limit=128)
            self.assertEqual(first, second)
            self.assertEqual((grid,stamp), before)
            if first is not None:
                self.assertEqual(len(first),4)
                final,_ = simulate(Instance(n,d,c,4,grid,target,stamp),
                                   [operations[aid] for aid in first])
                self.assertGreater(sum(a==b for a,b in zip(final,target)),
                                   sum(a==b for a,b in zip(grid,target)))
            self.assertIsNone(candidate.commutator_tail(*args,pair_limit=0))

    def test_wrapper_guards_k_and_parent_floor(self):
        rng = random.Random(2026092573)
        original_tail = candidate.commutator_tail
        def limited_tail(*args, **kwargs):
            return original_tail(*args, pair_limit=128)
        with patch.object(candidate,'solve_without_commutator',return_value=[]), \
             patch.object(candidate,'commutator_tail',side_effect=limited_tail):
            for k in (1,3,4,20):
                n,d,c = 4,3,4
                grid=[rng.randrange(c) for _ in range(n*n)]
                stamp=[rng.randrange(c) for _ in range(d*d)]
                target=grid[:]
                target[rng.randrange(n*n)]=rng.randrange(c)
                operations=candidate.solve(n,d,c,k,grid,target,stamp)
                final,_=simulate(Instance(n,d,c,k,grid,target,stamp),operations)
                self.assertLessEqual(len(operations),k)
                self.assertGreaterEqual(sum(a==b for a,b in zip(final,target)),
                                        sum(a==b for a,b in zip(grid,target)))
                if k<4:self.assertEqual(operations,[])

    def test_wrapper_can_append_a_strict_four_move_completion(self):
        rng = random.Random(2026092574)
        grid = [rng.randrange(2) for _ in range(16)]
        stamp = [rng.randrange(2) for _ in range(9)]
        witness = [(0,0,0),(0,1,0),(0,0,0),(0,1,0)]
        target,_ = simulate(Instance(4,3,2,4,grid,[0]*16,stamp),witness)
        self.assertNotEqual(grid,target)
        self.assertLessEqual(sum(a!=b for a,b in zip(grid,target)),12)
        with patch.object(candidate,'solve_without_commutator',return_value=[]):
            operations = candidate.solve(4,3,2,4,grid,target,stamp)
        final,_ = simulate(Instance(4,3,2,4,grid,target,stamp),operations)
        self.assertEqual(len(operations),4)
        self.assertEqual(final,target)

    def test_pair_cap_counts_each_inverse_trial(self):
        grid,stamp,target = [0]*16,[1]*9,[1]+[0]*15
        indices,_,_,_,_ = candidate.build(4,3,target)
        with patch.object(candidate,'commutator_word_gain',return_value=0) as gain:
            word = candidate.commutator_tail(4,3,grid,target,stamp,indices,817,
                                            pair_limit=7)
        self.assertIsNone(word)
        self.assertEqual(gain.call_count,14)


if __name__ == '__main__':
    unittest.main()
