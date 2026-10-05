# Early routing at a proven upper bound

Parent: `solvers/experiments/algebra39_cycles.py`, immutable checkpoint049 stable score 252,862,932. Runtime review found case265 near the five-second limit and an isolated timeout despite identical score/output on an earlier repeat.

Hypothesis: some nearly complete small boards can reach the color-inventory upper bound using cheap algebraic routing before entering the expensive late beam. Returning at that bound cannot lose score relative to any later search.

Implementation: `runtime_route_early_bound.py` injects a trial immediately after `solve_without_late_beam` inside `solve_without_hot_restart`, only for N=5..9, D=3. It cancels exact adjacent inverse pairs, evaluates the complete board and stamp, and tries the existing bitparallel sparse routing schedule. The new sequence is returned only when its canonical match count equals `color_bound(initial_grid + initial_stamp, target)`. A failed trial returns `None`; the original reference and original search continue unchanged. No timing thresholds or case-specific conditions are used.

Correctness evidence:

- An AST test removes the new helper and guarded call and verifies exact equality with the original entire program.
- Twenty fresh helper trials preserve grid, target, stamp, reference sequence, and the global random state. Any accepted trial is legal and reaches the inventory bound under the canonical simulator.
- All 30 affected fixed stable cases were run through the complete candidate in separate CLI processes with the normal validator and five-second timeout. All were valid; every per-case score equaled checkpoint049 (total subset score 25,156,623, score delta zero).

Measured runtime:

- First case265 run: 78 matches, 72 operations, 2.078s.
- Second case265 run in the 30-case diagnostic: 78 matches, 72 operations, 2.141s.
- Case317: 64 matches, 2.477s.
- All 30 affected cases: 43.337s total, 4.049s maximum (case056).

Files: `tools/test_runtime_route_early.py`, `results/runtime_route_early_265.json`, `results/runtime_route_early_small_diagnostic.json`. These are targeted runtime diagnostics; root coordinates full stable and isolated final qualification. Checkpoint049 was not modified.
