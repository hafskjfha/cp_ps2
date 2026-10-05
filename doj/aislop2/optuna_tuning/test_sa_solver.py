"""Differential checks for the standalone annealing solver.

Run from the repository root: python -m unittest optuna_tuning.test_sa_solver
"""

import random
import subprocess
import sys
import unittest
from pathlib import Path

from tools.simulate import Instance, format_instance, match_count, simulate
from tools.validate_output import validate_output
from optuna_tuning import sa_solver as sa


def make_instance(n=6, d=3, c=4, k=30, seed=0):
    rng = random.Random(seed)
    return Instance(n, d, c, k,
                    [rng.randrange(c) for _ in range(n*n)],
                    [rng.randrange(c) for _ in range(n*n)],
                    [rng.randrange(c) for _ in range(d*d)])


def input_bytes(instance):
    return format_instance(instance).encode('ascii')


class AnnealingSolverTests(unittest.TestCase):
    def assert_replay(self, instance, model, sequence, **kwargs):
        score, grid, stamp, states = model.replay(sequence, **kwargs)
        reference_grid, reference_stamp = simulate(
            instance, [model.decode(move) for move in sequence])
        self.assertEqual(grid, reference_grid)
        self.assertEqual(stamp, reference_stamp)
        self.assertEqual(score, match_count(instance, reference_grid))
        return states

    def test_all_reference_rotations(self):
        for d in (2, 3):
            for rotation in range(4):
                instance = make_instance(d=d, seed=rotation + 10*d)
                model = sa.Model(input_bytes(instance))
                move = model.encode((1, 2, rotation))
                self.assertEqual(model.decode(move), (1, 2, rotation))
                self.assert_replay(instance, model, [move], keep_states=True)
                # Swapping twice with the same reference rotation is an identity.
                score, grid, stamp, _ = model.replay([move, move])
                self.assertEqual((grid, stamp), (instance.a, instance.s))
                self.assertEqual(score, match_count(instance, instance.a))

    def test_random_sequences_and_mutated_suffixes(self):
        rng = random.Random(9412)
        params = sa.normalize_params({'iterations': 0})
        for d in (2, 3):
            for seed in range(10):
                instance = make_instance(d=d, seed=seed)
                model = sa.Model(input_bytes(instance))
                sequence = [rng.randrange(len(model.contacts))
                            for _ in range(rng.randrange(instance.k+1))]
                states = self.assert_replay(instance, model, sequence,
                                           keep_states=True)
                for _ in range(30):
                    changed, first = sa.mutate(sequence, model, rng, params)
                    self.assertLessEqual(len(changed), instance.k)
                    self.assertEqual(changed[:first], sequence[:first])
                    states = self.assert_replay(instance, model, changed,
                                               states=states, start=first,
                                               keep_states=True)
                    sequence = changed

    def test_each_mutation_type_and_boundary(self):
        rng = random.Random(76)
        for d in (2, 3):
            model = sa.Model(input_bytes(make_instance(n=3, d=d, k=1)))
            for kind in ('replace', 'insert', 'delete', 'swap'):
                weights = {f'{name}_weight': float(name == kind)
                           for name in ('replace', 'insert', 'delete', 'swap')}
                params = sa.normalize_params(weights)
                for initial in ([], [0]):
                    for _ in range(20):
                        candidate, first = sa.mutate(initial, model, rng, params)
                        self.assertLessEqual(len(candidate), 1)
                        self.assertTrue(all(0 <= m < len(model.contacts)
                                            for m in candidate))
                        self.assertEqual(candidate[:first], initial[:first])

    def test_deterministic_and_no_worse_than_greedy(self):
        for d in (2, 3):
            for seed in range(4):
                instance = make_instance(d=d, seed=seed)
                data = input_bytes(instance)
                params = {'iterations': 350}
                result = sa.solve(data, params=params, seed=712)
                self.assertEqual(result, sa.solve(data, params=params, seed=712))
                baseline = sa.solve(data, params={'iterations': 0}, seed=712)
                self.assertGreaterEqual(
                    match_count(instance, simulate(instance, result)[0]),
                    match_count(instance, simulate(instance, baseline)[0]))

    def test_minimum_and_maximum_inputs(self):
        for n, d, c, k in ((3, 2, 2, 1), (3, 3, 6, 180),
                            (30, 2, 2, 180), (30, 3, 6, 180)):
            instance = make_instance(n, d, c, k, seed=450)
            operations = sa.solve(input_bytes(instance), {'iterations': 40})
            text = sa.format_answer(operations)
            self.assertEqual(validate_output(instance, text), operations)

    def test_stdin_stdout_entrypoint(self):
        instance = make_instance(n=3, d=3, k=1)
        process = subprocess.run([sys.executable, str(Path(sa.__file__).resolve())],
                                 input=input_bytes(instance), capture_output=True,
                                 check=True, timeout=5)
        validate_output(instance, process.stdout)
        self.assertEqual(process.stderr, b'')
        self.assertLess(Path(sa.__file__).stat().st_size, 100_000)

    def test_bad_parameters_fail_explicitly(self):
        for params in ({'typo': 1}, {'iterations': -1}, {'iterations': 0.5},
                       {'start_temp': float('nan')}, {'end_temp': 0},
                       {'start_temp': 0.1, 'end_temp': 1},
                       {'local_probability': 1.5}, {'local_radius': 0},
                       {'tail_bias': -1}, {'swap_weight': -1},
                       {f'{key}_weight': 0 for key in
                        ('replace', 'insert', 'delete', 'swap')}):
            with self.subTest(params=params), self.assertRaises(ValueError):
                sa.normalize_params(params)


if __name__ == '__main__':
    unittest.main()
