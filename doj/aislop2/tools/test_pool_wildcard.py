"""Exact-path and canonical checks for target-dependent wildcard caching."""
import random
import unittest

from solvers.experiments import pool_wildcard_cache as candidate
from submissions import best_032_251668850 as reference
from tools.simulate import Instance, simulate


class WildcardCacheTests(unittest.TestCase):
    def test_repeated_prefix_calls_preserve_exact_join_paths(self):
        rng = random.Random(2026092551)
        backward_joins = 0
        calls = 0
        for trial in range(8):
            c = 2 + trial % 5
            grid = [rng.randrange(c) for _ in range(16)]
            stamp = [rng.randrange(c) for _ in range(9)]
            witness = [(rng.randrange(2), rng.randrange(2), rng.randrange(4))
                       for _ in range(8)]
            base = Instance(4, 3, c, 8, grid, [0] * 16, stamp)
            target, _ = simulate(base, witness)
            # The same target is visited with changing forward states, budgets,
            # and cache prefixes, then visited again with the original budget.
            for prefix, budget in ((3, 5), (2, 6), (0, 8), (0, 4), (3, 5)):
                board, carried = simulate(base, witness[:prefix])
                expected = reference.wildcard_finish(board, target, carried, budget)
                actual = candidate.wildcard_finish(board, target, carried, budget)
                self.assertEqual(actual, expected, (trial, prefix, budget))
                calls += 1
                if actual is not None:
                    backward_joins += len(actual) > 4
                    operations = [(aid // 8, (aid // 4) % 2, aid % 4)
                                  for aid in actual]
                    final, _ = simulate(Instance(4, 3, c, budget, board, target, carried),
                                        operations)
                    self.assertEqual(final, target)
                    self.assertLessEqual(len(actual), budget)
        self.assertEqual(calls, 40)
        self.assertGreater(backward_joins, 5)

    def test_cached_record_order_and_constraint_encoding(self):
        rng = random.Random(2026092552)
        target = [rng.randrange(6) for _ in range(16)]
        wanted = sum(v << (3 * i) for i, v in enumerate(target))
        expand = reference.packed_transitions()
        goal = wanted | (((1 << 27) - 1) << 48)
        visited = {goal: b''}
        frontier = [goal]
        records = []
        for depth in range(1, 4):
            layer = []
            for state in frontier:
                for aid, child in expand(state):
                    if child in visited:
                        continue
                    path = visited[state] + bytes((aid,))
                    visited[child] = path
                    wishes = child
                    encoded = []
                    for position in range(25):
                        color = wishes & 7
                        wishes >>= 3
                        if color != 7:
                            encoded.append(position * 6 + color)
                    records.append((depth, path, bytes(encoded)))
                    layer.append(child)
            frontier = layer
        cached = candidate.wildcard_backward_records(expand, wanted)
        for expected in records:
            self.assertEqual(next(cached), expected)
            self.assertEqual(len(expected[2]), 16)


if __name__ == '__main__':
    unittest.main()
