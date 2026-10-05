"""Exact initializer equivalence, including mutable goal-cache isolation."""
import ast
import importlib.util
from pathlib import Path
import random
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'solvers/experiments' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


old = load('runtime_route_early_bound')
new = load('runtime_init_fast')


class InitializationTests(unittest.TestCase):
    def test_only_initializer_and_cache_changed(self):
        a = ast.parse((ROOT / 'solvers/experiments/runtime_route_early_bound.py').read_text())
        b = ast.parse((ROOT / 'solvers/experiments/runtime_init_fast.py').read_text())
        b.body = [node for node in b.body if not (isinstance(node, ast.Assign)
                  and isinstance(node.targets[0], ast.Name) and node.targets[0].id == '_REFINE_GOALS')]
        for tree in (a, b):
            cls = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == 'RefineState')
            cls.body = [node for node in cls.body if node.name != '__init__']
        self.assertEqual(ast.dump(a), ast.dump(b))

    def test_all_fields_and_decisions_after_updates(self):
        rng = random.Random(20260925912)
        for trial in range(60):
            n, d, c = (3, 4, 7, 15, 30)[trial % 5], 2 + trial % 2, 2 + trial % 5
            target = [rng.randrange(c) for _ in range(n*n)]
            initial = target[:] + [rng.randrange(c) for _ in range(d*d)]
            for p in rng.sample(range(n*n), trial % (n*n+1)):
                initial[p] = rng.randrange(c)
            indices, _, ops, _, _ = old.build(n, d, target)
            actions = list(zip(indices, ops))
            order = list(range(len(actions)))
            rng.shuffle(order)
            a = old.RefineState(n, d, initial, target, actions, order)
            b = new.RefineState(n, d, initial, target, actions, order)
            self.assertEqual(a.__dict__, b.__dict__)
            for step in range(30):
                aid = rng.randrange(len(actions))
                wishes = step % 2 == 0
                a.apply(aid, wishes=wishes)
                b.apply(aid, wishes=wishes)
                self.assertEqual(a.__dict__, b.__dict__)
                self.assertEqual(a.best(), b.best())
            # Updates must never corrupt a cached initial goal mask.
            a = old.RefineState(n, d, initial, target, actions, order)
            b = new.RefineState(n, d, initial, target, actions, order)
            self.assertEqual(a.__dict__, b.__dict__)


if __name__ == '__main__':
    unittest.main()
