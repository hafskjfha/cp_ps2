"""Bounded exact-state, escape, clone, and ABBA timing checks for State.apply."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import statistics
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.simulate import Instance, simulate


def load(filename, name):
    path = ROOT / 'solvers/experiments' / filename
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, path


old, old_path = load('runtime_route_early_bound.py', 'state_old')
new, new_path = load('runtime_state_fast.py', 'state_new')
trees = [ast.parse(path.read_text()) for path in (old_path, new_path)]
for tree in trees:
    cls = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == 'State')
    cls.body = [node for node in cls.body if not isinstance(node, ast.FunctionDef) or node.name != 'apply']
assert ast.dump(trees[0]) == ast.dump(trees[1]), 'Change extends beyond State.apply'


def fields(state):
    return {key: value for key, value in state.__dict__.items() if key != '_runtime_cover_bits'}


def check(states):
    assert fields(states[0]) == fields(states[1])
    assert states[0].best() == states[1].best()
    assert states[0].best_candidates() == states[1].best_candidates()
    state = states[1]
    weights = getattr(state, 'weights', [1] * len(state.grid))
    counts = [sum(weights[p]
                  for p in positions if state.grid[p] == state.target[p]) for positions in state.regions]
    assert counts == state.counts
    planes = [0] * len(state.old_planes)
    for region, count in enumerate(counts):
        value = state.size - count
        for bit in range(len(planes)):
            if value & (1 << bit):
                planes[bit] |= state.region_bits[region]
    assert planes == state.old_planes


rng = random.Random(440791)
transitions = escapes = clones = involutions = 0
for n in (3, 5, 9, 30):
    for d in (2, 3):
        for c in (2, 6):
            grid = [rng.randrange(c) for _ in range(n*n)]
            target = [rng.randrange(c) for _ in range(n*n)]
            stamp = [rng.randrange(c) for _ in range(d*d)]
            order = list(range(4 * (n-d+1)**2))
            rng.shuffle(order)
            for cls_name in ('State', 'ProductiveState', 'WeightedState'):
                states = [getattr(module, cls_name)(n, d, c, grid[:], target[:], stamp[:], order[:]) for module in (old, new)]
                check(states)
                for step in range(40):
                    action = rng.randrange(len(order))
                    reference = Instance(n, d, c, 1, states[0].grid[:], target[:], states[0].stamp[:])
                    canonical = simulate(reference, [states[0].actions[action][1]])
                    for state in states:
                        state.apply(action)
                    assert (states[1].grid, states[1].stamp) == canonical
                    check(states)
                    transitions += 1
                before = [fields(state).copy() for state in states]
                # Deep snapshot of fields mutated by apply, preserving geometry identity.
                snapshots = [(state.grid[:], state.stamp[:], state.counts[:], state.old_planes[:], state.matches, state.stampmask) for state in states]
                action = rng.randrange(len(order))
                for state in states:
                    state.apply(action)
                    state.apply(action)
                for state, snapshot in zip(states, snapshots):
                    assert (state.grid, state.stamp, state.counts, state.old_planes, state.matches, state.stampmask) == snapshot
                involutions += 1
                if cls_name != 'WeightedState':
                    for seed in range(2):
                        randoms = [random.Random(seed + 1071), random.Random(seed + 1071)]
                        kwargs = dict(width=12)
                        if cls_name == 'ProductiveState':
                            kwargs['min_gain'] = seed - 2
                        pairs = [state.escape(random, **kwargs) for state, random in zip(states, randoms)]
                        assert pairs[0] == pairs[1]
                        assert randoms[0].getstate() == randoms[1].getstate()
                        check(states)
                        for state, snapshot in zip(states, snapshots):
                            assert (state.grid, state.stamp, state.counts, state.old_planes, state.matches, state.stampmask) == snapshot
                        escapes += 1
                    children = [module.clone_state(state) for module, state in zip((old, new), states)]
                    assert children[1]._runtime_cover_bits is states[1]._runtime_cover_bits
                    for child in children:
                        child.apply(action)
                    check(children)
                    for state, snapshot in zip(states, snapshots):
                        assert (state.grid, state.stamp, state.counts, state.old_planes, state.matches, state.stampmask) == snapshot
                    clones += 1

# Repeated ABBA orders balance gradual changes in host load. Cache preparation is
# included in the first timed apply; constructors are outside the timed block.
timings = []
for n, d in ((9, 2), (9, 3), (30, 2), (30, 3)):
    c = 6
    grid = [rng.randrange(c) for _ in range(n*n)]
    target = [rng.randrange(c) for _ in range(n*n)]
    stamp = [rng.randrange(c) for _ in range(d*d)]
    order = list(range(4 * (n-d+1)**2))
    rng.shuffle(order)
    sequence = [rng.randrange(len(order)) for _ in range(10000)]
    samples = [[], []]
    final_fields = []
    for index in (0, 1, 1, 0, 0, 1, 1, 0):
        state = (old, new)[index].State(n, d, c, grid[:], target[:], stamp[:], order[:])
        apply = state.apply
        start = time.perf_counter()
        for action in sequence:
            apply(action)
        elapsed = time.perf_counter() - start
        samples[index].append(elapsed)
        final_fields.append(fields(state))
    assert all(fields == final_fields[0] for fields in final_fields)
    timings.append(dict(n=n, d=d, c=c, steps=len(sequence), old_sec=samples[0], new_sec=samples[1],
                        median_speedup=statistics.median(samples[0]) / statistics.median(samples[1])))

report = dict(passed=True, scope='Only State.apply changes; WeightedState.apply unchanged',
              canonical_transitions=transitions, escape_and_restore_checks=escapes,
              clone_isolation_checks=clones, involution_checks=involutions,
              parent_sha256=hashlib.sha256(old_path.read_bytes()).hexdigest(),
              candidate_sha256=hashlib.sha256(new_path.read_bytes()).hexdigest(),
              candidate_bytes=new_path.stat().st_size, abba_micro=timings,
              limitation='Apply micro timings are not full-solver speed measurements; no full benchmark run here.')
(ROOT / 'results/runtime_review_state.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
