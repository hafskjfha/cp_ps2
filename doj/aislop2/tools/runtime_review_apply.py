"""Exact state/sequence checks for transposed RefineState.apply geometry."""
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.check_submission import make_case
from tools.simulate import Instance, match_count, simulate


def load(filename, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "solvers/experiments" / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


old = load("runtime_route_early_bound.py", "apply_old")
new = load("runtime_large_fast.py", "apply_new")
rng = random.Random(986113)
transitions = nested = sweeps = 0
for n in (3, 5, 9, 30):
    for d in (2, 3):
        for c in (2, 6):
            initial = [rng.randrange(c) for _ in range(n * n + d * d)]
            target = [rng.randrange(c) for _ in range(n * n)]
            indices, _, operations, _, _ = old.build(n, d, target)
            actions = list(zip(indices, operations))
            order = list(range(len(actions)))
            rng.shuffle(order)
            states = [module.RefineState(n, d, initial, target, actions, order) for module in (old, new)]
            assert states[0].__dict__ == states[1].__dict__
            for step in range(80):
                action, wishes = rng.randrange(len(actions)), bool(rng.randrange(2))
                for state in states:
                    state.apply(action, wishes)
                assert states[0].__dict__ == states[1].__dict__, (n, d, c, step)
                assert states[0].best() == states[1].best()
                transitions += 1
            stacks = [[], []]
            for step in range(40):
                if stacks[0] and (len(stacks[0]) > 4 or rng.randrange(3) == 0):
                    for module, state, stack in zip((old, new), states, stacks):
                        module.refine_restore(state, stack.pop())
                else:
                    action, wishes = rng.randrange(-1, len(actions)), bool(rng.randrange(2))
                    for module, state, stack in zip((old, new), states, stacks):
                        stack.append(module.refine_trial(state, action, wishes))
                assert states[0].__dict__ == states[1].__dict__, (n, d, c, "trial", step)
                assert states[0].best() == states[1].best()
                nested += 1
            if n <= 9:
                sequence = [rng.randrange(len(actions)) for _ in range(15)]
                assert old.refine(n, d, 20, initial, target, actions, sequence, passes=2) == new.refine(n, d, 20, initial, target, actions, sequence, passes=2)
                sweeps += 1

# One complete targeted run is compared against the reference output captured by
# the independently profiled unchanged solver. This is a diagnostic, not a score
# benchmark or a substitute for the root task's full runtime qualification.
case = make_case(30, 3, 6, 180, 916403757, "reachable")
expected = [tuple(operation) for operation in json.loads((ROOT / "results/runtime_review_large_operations.json").read_text())]
started = time.perf_counter()
answer = new.solve(case.n, case.d, case.c, case.k, case.a, case.t, case.s)
elapsed = time.perf_counter() - started
assert answer == expected
grid, _ = simulate(case, answer)
report = dict(passed=True, mixed_transitions=transitions, nested_trials_and_restores=nested, exact_refine_sweeps=sweeps,
              complete_reachable_case=dict(output_identical=True, matches=match_count(case, grid), runtime_sec=elapsed, operations=len(answer)),
              candidate_sha256=hashlib.sha256((ROOT / "solvers/experiments/runtime_large_fast.py").read_bytes()).hexdigest())
(ROOT / "results/runtime_review_apply.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
