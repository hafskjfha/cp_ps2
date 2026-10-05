# Exact temporal-refinement runtime reduction

Parent: `runtime_route_early_bound.py`; this work changes search evaluation cost, not candidates, seeds, tie decisions, budgets, or acceptance rules.

The final implementation is `solvers/experiments/runtime_temporal_fast.py`. Root can compose exactly four top-level definitions: `temporal_best`, `temporal_boundary`, `best_insertion`, and `deletion_deltas`. `RefineState.__init__` remains unchanged in this experiment so root's independent initializer optimization can be combined safely.

## Changes

1. `best_insertion` constructs `RefineState` with an empty order, skipping unused shuffled tie bitmask construction. It still performs the original seeded shuffle and stores its inverse ranks.
2. `temporal_best` computes the identical maximum gain. It resolves the smallest shuffled rank only when that gain strictly exceeds the best insertion found so far. Other positions cannot change the original insertion result, so their tie resolution is unnecessary.
3. `temporal_boundary` fuses the backward grid/stamp and wishes/wish-stamp swaps. Value and goal masks update together, and mismatch-count planes change only by the final comparison delta. Intermediate comparison changes that would cancel are not performed.
4. `deletion_deltas` also skips unused tie bitmasks. By the operation's involution property, `-gain(after applying operation) == gain(before applying operation)`, so it evaluates that gain before the fused boundary move.

## Evidence

`tools/test_runtime_route_early_temporal.py` verifies:

- 35 configurations across N=3,5,9,17,30 and D=2/3, each with 30 mixed one-sided and fused boundary moves: every state field and best action exactly matches the original implementation.
- Deferred tie resolution against five gain thresholds after every tested move.
- 24 randomized insertion, deletion, and complete temporal-repair paths: exact equality with the original implementation.

Measured N=30 temporal repair with 175 existing operations, five rounds and five deletion candidates per round:

| Stamp | Original | Final candidate | Ratio |
|---|---:|---:|---:|
| D=2 | 0.450s | 0.328s | 1.37x |
| D=3 | 0.644s | 0.423s | 1.52x |

Both measured paths were exactly identical. An earlier fused-boundary-only experiment showed inconsistent/small gains; deferred tie work supplied the useful improvement. Microbenchmarks are not full submission timing qualification.

The root's `runtime_combined_v1.py` was independently reviewed: all four definitions plus the early-bound helper/call were AST-identical to their reviewed versions. The initializer's goal-mask cache copies each row before mutation; its cover-mask addition builds the same mismatch-plane invariant required by the fused move. The full temporal differential test set passed against this composed source in 1.917s.

Root owns full stable, readiness and isolated maximum-size qualification. No checkpoint was modified by this experiment.
