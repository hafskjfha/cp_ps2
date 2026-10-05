"""Upper-bound scheduling and exact last-attempt memoization oracles."""
import unittest
from unittest.mock import patch
from tools.test_solver import ROOT, load_solver
from tools.simulate import Instance, simulate, match_count


class EarlyBoundTests(unittest.TestCase):
    def setUp(self):
        self.solver = load_solver(ROOT/'solvers/experiments/complete_early_bound.py')
        self.grid = [0]*25
        self.target = self.grid[:]
        self.target[6] = 1
        self.stamp = [0]*9
        self.stamp[4] = 1
        self.instance = Instance(5,3,2,8,self.grid,self.target,self.stamp)

    def test_optimal_early_path_skips_deeper_search(self):
        m = self.solver
        with patch.object(m, 'solve_without_deeper_beam', return_value=[]), \
             patch.object(m, 'stamp_beam_uncached', return_value=[0]), \
             patch.object(m, 'deeper_beam_finish', side_effect=AssertionError('unneeded deeper search')):
            found = m.solve_without_palindrome(5,3,2,8,self.grid[:],self.target,self.stamp[:])
        self.assertEqual(match_count(self.instance, simulate(self.instance, found)[0]), 25)
        self.assertLessEqual(len(found), 8)

    def test_failed_early_attempt_preserves_original_fallback(self):
        m = self.solver
        with patch.object(m, 'solve_without_deeper_beam', return_value=[]), \
             patch.object(m, 'stamp_beam_uncached', return_value=None) as attempt, \
             patch.object(m, 'deeper_beam_finish', return_value=[0]):
            found = m.solve_without_palindrome(5,3,2,8,self.grid[:],self.target,self.stamp[:])
            self.assertEqual(attempt.call_count, 1)
        self.assertEqual(match_count(self.instance, simulate(self.instance, found)[0]), 25)

    def test_failed_attempt_is_cached_with_all_problem_data(self):
        m = self.solver
        with patch.object(m, 'stamp_beam_uncached', return_value=None) as attempt:
            for _ in range(3):
                self.assertIsNone(m.stamp_beam_finish(5,self.grid,self.target,self.stamp,8))
            self.assertEqual(attempt.call_count, 1)
            m.stamp_beam_finish(5,self.grid,self.target,self.stamp,7)
            self.assertEqual(attempt.call_count, 2)
            other = self.target[:]
            other[0] = 1
            m.stamp_beam_finish(5,self.grid,other,self.stamp,7)
            self.assertEqual(attempt.call_count, 3)

    def test_cache_returns_independent_paths(self):
        m = self.solver
        with patch.object(m, 'stamp_beam_uncached', return_value=[0]) as attempt:
            first = m.stamp_beam_finish(5,self.grid,self.target,self.stamp,8)
            first.append(3)
            second = m.stamp_beam_finish(5,self.grid,self.target,self.stamp,8)
            self.assertEqual(second, [0])
            second.clear()
            self.assertEqual(m.stamp_beam_finish(5,self.grid,self.target,self.stamp,8), [0])
            self.assertEqual(attempt.call_count, 1)

    def test_short_remaining_budget_keeps_parent(self):
        m = self.solver
        with patch.object(m, 'solve_without_deeper_beam', return_value=[]), \
             patch.object(m, 'stamp_beam_uncached', side_effect=AssertionError('budget guard')):
            self.assertEqual(m.solve_without_palindrome(5,3,2,2,self.grid[:],self.target,self.stamp[:]), [])


if __name__ == '__main__':
    unittest.main()
