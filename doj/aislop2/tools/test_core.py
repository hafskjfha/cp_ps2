"""Independent correctness checks: python -m unittest tools.test_core."""

from collections import Counter
import random
import unittest

from tools.simulate import (
    Instance, format_instance, match_count, parse_instance, rotation_offsets, simulate,
)
from tools.validate_output import validate_output
from tools.score import score


def fixture(n=3, d=2, c=6, k=180):
    return Instance(n, d, c, k, [i % c for i in range(n*n)],
                    [(i + 2) % c for i in range(n*n)],
                    [(i + 3) % c for i in range(d*d)])


def matrix_rotate(matrix):
    """Rotate a matrix clockwise without the canonical coordinate formulas."""
    return [list(row) for row in zip(*matrix[::-1])]


def independent_simulate(instance, operations):
    n, d = instance.n, instance.d
    grid = [instance.a[i:i+n] for i in range(0, n*n, n)]
    stamp = [instance.s[i:i+d] for i in range(0, d*d, d)]
    for x, y, r in operations:
        for _ in range(r):
            stamp = matrix_rotate(stamp)
        old_patch = [row[y:y+d] for row in grid[x:x+d]]
        for i in range(d):
            grid[x+i][y:y+d] = stamp[i]
        stamp = old_patch
        for _ in range((-r) % 4):
            stamp = matrix_rotate(stamp)
    return [v for row in grid for v in row], [v for row in stamp for v in row]


class ParsingTests(unittest.TestCase):
    def test_round_trip_minimum_and_maximum(self):
        for n, d, c, k in [(3, 2, 2, 1), (3, 3, 6, 180), (30, 3, 6, 180)]:
            instance = fixture(n, d, c, k)
            self.assertEqual(parse_instance(format_instance(instance)), instance)

    def test_bad_instance_headers(self):
        for header in [(2, 2, 2, 1), (31, 2, 2, 1), (3, 1, 2, 1),
                       (3, 4, 2, 1), (3, 2, 1, 1), (3, 2, 7, 1),
                       (3, 2, 2, 0), (3, 2, 2, 181)]:
            text = ' '.join(map(str, header)) + '\n' + '0 ' * 22
            with self.subTest(header=header), self.assertRaises(ValueError):
                parse_instance(text)

    def test_bad_instance_payloads(self):
        text = format_instance(fixture())
        for bad in ['', '3 2 6', text + '0', ' '.join(text.split()[:-1]),
                    text.replace('3 2 6 180', '3 2 6 1_80'),
                    text.replace('3 2 6 180', '3 2 6 ١٨٠'),
                    text.rsplit(' ', 1)[0] + ' 6',
                    text.rsplit(' ', 1)[0] + ' -1']:
            with self.subTest(bad=bad[:40]), self.assertRaises(ValueError):
                parse_instance(bad)


class RotationTests(unittest.TestCase):
    def test_all_rotation_offsets(self):
        expected = {
            2: [[0, 1, 2, 3], [1, 3, 0, 2], [3, 2, 1, 0], [2, 0, 3, 1]],
            3: [[0, 1, 2, 3, 4, 5, 6, 7, 8],
                [2, 5, 8, 1, 4, 7, 0, 3, 6],
                [8, 7, 6, 5, 4, 3, 2, 1, 0],
                [6, 3, 0, 7, 4, 1, 8, 5, 2]],
        }
        for d in (2, 3):
            for r in range(4):
                with self.subTest(d=d, r=r):
                    actual = [p*d+q for p, q in rotation_offsets(d, r)]
                    self.assertEqual(actual, expected[d][r])

    def test_invalid_rotations(self):
        for d, r in [(1, 0), (4, 0), (2, -1), (3, 4)]:
            with self.assertRaises(ValueError):
                rotation_offsets(d, r)

    def test_each_rotation_simulated_independently(self):
        for d in (2, 3):
            instance = fixture(n=5, d=d)
            for r in range(4):
                ops = [(1, 2, r)]
                with self.subTest(d=d, r=r):
                    self.assertEqual(simulate(instance, ops), independent_simulate(instance, ops))

    def test_repeating_same_operation_is_involution(self):
        for d in (2, 3):
            instance = fixture(n=5, d=d)
            for r in range(4):
                self.assertEqual(simulate(instance, [(1, 2, r)] * 2),
                                 (instance.a, instance.s))

    def test_zero_operations_copies_inputs(self):
        instance = fixture()
        grid, stamp = simulate(instance, [])
        self.assertEqual((grid, stamp), (instance.a, instance.s))
        self.assertIsNot(grid, instance.a)
        self.assertIsNot(stamp, instance.s)

    def test_random_sequences_against_independent_matrix_rotation(self):
        rng = random.Random(20490123)
        for trial in range(300):
            n, d, c = rng.randint(3, 30), rng.choice((2, 3)), rng.randint(2, 6)
            instance = Instance(n, d, c, 180,
                                [rng.randrange(c) for _ in range(n*n)],
                                [rng.randrange(c) for _ in range(n*n)],
                                [rng.randrange(c) for _ in range(d*d)])
            ops = [(rng.randrange(n-d+1), rng.randrange(n-d+1), rng.randrange(4))
                   for _ in range(rng.randrange(181))]
            actual = simulate(instance, ops)
            with self.subTest(trial=trial, n=n, d=d):
                self.assertEqual(actual, independent_simulate(instance, ops))
                self.assertEqual(Counter(actual[0] + actual[1]),
                                 Counter(instance.a + instance.s))

    def test_simulator_rejects_invalid_operations(self):
        instance = fixture(k=1)
        for ops in [[(-1, 0, 0)], [(0, 2, 0)], [(0, 0, 4)],
                    [(0, 0)], [(0, 0, 0.0)], [(True, 0, 0)],
                    [(0, 0, 0), (0, 0, 0)]]:
            with self.subTest(ops=ops), self.assertRaises(ValueError):
                simulate(instance, ops)


class OutputTests(unittest.TestCase):
    def test_accepts_legal_output_and_ascii_whitespace(self):
        instance = fixture()
        self.assertEqual(validate_output(instance, '0\n'), [])
        self.assertEqual(validate_output(instance, b'2\r\n0\t0 3\n1 1 0\n'),
                         [(0, 0, 3), (1, 1, 0)])
        self.assertEqual(validate_output(instance, '1 +0 01 0'), [(0, 1, 0)])

    def test_all_illegal_output_forms(self):
        instance = fixture(k=1)
        bad_outputs = [b'', b' ', b'-1', b'2 0 0 0 0 0 0', b'0 1',
                       b'1', b'1 0 0', b'1 0 0 0 0', b'1 -1 0 0',
                       b'1 0 -1 0', b'1 2 0 0', b'1 0 2 0',
                       b'1 0 0 -1', b'1 0 0 4', b'1 0 0 0.0',
                       b'1 0 0 1e0', b'1 0 0 0_0', b'1 0x0 0 0',
                       b'0\x00', b'\xff', '０', '0\u00a0',
                       b'0' + b' ' * 100000]
        for bad in bad_outputs:
            with self.subTest(bad=repr(bad[:50])), self.assertRaises(ValueError):
                validate_output(instance, bad)

    def test_exact_byte_limit(self):
        self.assertEqual(validate_output(fixture(), b'0' + b' ' * 99999), [])


class ScoreTests(unittest.TestCase):
    def test_exact_integer_score_and_match_count(self):
        instance = Instance(3, 2, 2, 1, [0]*9, [0]*4 + [1]*5, [1]*4)
        self.assertEqual(match_count(instance, instance.a), 4)
        self.assertEqual(score(instance, []),
                         {'matches': 4, 'total_cells': 9, 'score': 444444})

    def test_score_runs_actual_simulator(self):
        instance = Instance(3, 2, 2, 1, [0]*9, [1, 1, 0, 1, 1, 0, 0, 0, 0], [1]*4)
        self.assertEqual(score(instance, [(0, 0, 3)]),
                         {'matches': 9, 'total_cells': 9, 'score': 1000000})


if __name__ == '__main__':
    unittest.main()
