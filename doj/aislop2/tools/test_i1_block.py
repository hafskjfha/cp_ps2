"""Independent canonical oracles for exact-suffix block beam search."""
import importlib.util
import random
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.simulate import Instance, simulate, rotation_offsets
SOLVER_PATH = sys.argv.pop(1) if len(sys.argv) > 1 and sys.argv[1].endswith('.py') else 'solvers/experiments/i1_block_beam.py'


def load_solver():
    path = ROOT / SOLVER_PATH
    spec = importlib.util.spec_from_file_location('i1_test_solver', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def operations(n, d):
    return [(x, y, r) for x in range(n-d+1) for y in range(n-d+1) for r in range(4)]


def advance(n, d, colors, ops):
    instance = Instance(n, d, 6, 180, colors[:n*n], [0]*(n*n), colors[n*n:])
    grid, stamp = simulate(instance, ops)
    return grid + stamp


def objective(colors, wanted):
    return sum(a == b for a, b in zip(colors, wanted))


class BlockBeamTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.solver = load_solver()

    def test_all_rotations_match_canonical_and_are_involutions(self):
        rng = random.Random(193710)
        for d in (2, 3):
            for n in (3, 4, 7, 30):
                expand = self.solver.i1_packed_expand(n, d)
                ops = operations(n, d)
                for trial in range(3):
                    values = [rng.randrange(6) for _ in range(n*n+d*d)]
                    packed = sum(v << (3*i) for i, v in enumerate(values))
                    expanded = list(expand(packed))
                    self.assertEqual([aid for aid, _ in expanded], list(range(len(ops))))
                    for aid, child in expanded:
                        decoded = [(child >> (3*i)) & 7 for i in range(len(values))]
                        self.assertEqual(decoded, advance(n, d, values, [ops[aid]]))
                        self.assertEqual(advance(n, d, decoded, [ops[aid]]), values)

    def test_two_step_beam_equals_exhaustive_with_stamp_goals(self):
        rng = random.Random(920313)
        for d in (2, 3):
            n = 3
            ops = operations(n, d)
            for trial in range(12):
                values = [rng.randrange(6) for _ in range(n*n+d*d)]
                wanted = [rng.randrange(7) for _ in values]
                wanted[-1] = values[0]  # A live, scored reference stamp cell.
                wanted[0] = 6  # An unscored grid cell from the fixed suffix.
                oracle = objective(values, wanted)
                for first in ops:
                    after = advance(n, d, values, [first])
                    oracle = max(oracle, objective(after, wanted))
                    for second in ops:
                        oracle = max(oracle, objective(advance(n, d, after, [second]), wanted))
                path, score, count = self.solver.i1_search_block(
                    n, d, values, wanted, 2, width=512, node_budget=10000, seed=trial)
                self.assertTrue(all(type(i) is int and 0 <= i < len(ops) for i in path))
                actual = advance(n, d, values, [ops[i] for i in path])
                self.assertEqual(score, objective(actual, wanted))
                self.assertEqual(score, oracle)
                self.assertLessEqual(len(path), 2)
                self.assertLessEqual(count, 10000)

    def test_fixed_suffix_boundary_objective(self):
        rng = random.Random(991219)
        for d in (2, 3):
            for n in (4, 7):
                ops = operations(n, d)
                for trial in range(8):
                    values = [rng.randrange(6) for _ in range(n*n+d*d)]
                    target = [rng.randrange(6) for _ in range(n*n)]
                    prefix = [rng.choice(ops) for _ in range(4)]
                    suffix = [rng.choice(ops) for _ in range(6)]
                    before = advance(n, d, values, prefix)
                    wanted = advance(n, d, target+[6]*(d*d), list(reversed(suffix)))
                    path, score, count = self.solver.i1_search_block(
                        n, d, before, wanted, 4, width=8, node_budget=3000, seed=trial)
                    self.assertTrue(all(type(i) is int and 0 <= i < len(ops) for i in path))
                    final = advance(n, d, values, prefix+[ops[i] for i in path]+suffix)
                    self.assertEqual(score, objective(final[:n*n], target))
                    self.assertLessEqual(count, 3000)

    def test_repair_preserves_parent_floor_budget_and_determinism(self):
        rng = random.Random(992513)
        for d in (2, 3):
            for n in (3, 4, 7):
                ops = operations(n, d)
                idx = [[(x+u)*n+y+v for u, v in rotation_offsets(d, r)] for x, y, r in ops]
                actions = list(zip(idx, ops))
                for trial in range(5):
                    values = [rng.randrange(6) for _ in range(n*n+d*d)]
                    target = [rng.randrange(6) for _ in range(n*n)]
                    path = [rng.randrange(len(ops)) for _ in range(trial*3)]
                    args = (n, d, 6, 18, values, target, actions, path)
                    kwargs = dict(rounds=6, width=8, node_budget=5000)
                    result = self.solver.i1_block_repair(*args, **kwargs)
                    self.assertTrue(all(type(i) is int and 0 <= i < len(ops) for i in result))
                    self.assertEqual(result, self.solver.i1_block_repair(*args, **kwargs))
                    self.assertLessEqual(len(result), 18)
                    old = advance(n, d, values, [ops[i] for i in path])
                    new = advance(n, d, values, [ops[i] for i in result])
                    self.assertGreaterEqual(objective(new[:n*n], target), objective(old[:n*n], target))


if __name__ == '__main__':
    unittest.main()
