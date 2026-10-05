# Round 4: algebraic routing and temporal sequence repair

Recommended submission: [runtime_049_252862932.py](../submissions/runtime_049_252862932.py).
It is a self-contained, standard-library Python program of **91,944 bytes**.
`solvers/current.py` contains the same bytes; `results/best.json` points to this file.

Ten new strict score improvements were measured on the unchanged 320-case
benchmark. Checkpoint039 scored 251,862,073; checkpoint049 scores 252,862,932,
a gain of 1,000,859 (0.3974%). Average score rose from 787,068.978125 to
790,196.6625. Fifty-three cases improved, 267 tied, and none regressed.
These are local benchmark results, not a prediction of the official 40-case score.

The source limit is **100,000 bytes**, as clarified by the user. The earlier
10,000-byte interpretation was too restrictive. Checkpoints040–045 satisfy that
stricter limit; 046–049 retain the complete previous search portfolio as ordinary
Python. The old107,628-byte checkpoint039 remains an immutable historical result.

## Different search direction

Each stamp operation is an involution. Cancelling adjacent identical operations
therefore preserves both the board and stamp while recovering operation budget.
Composing two overlapping operations as `(P Q)^3` cancels many of their effects,
leaving a small permutation that can repair a few cells. Longer powers provide
complementary 10-, 12-, 18-, and 24-operation repairs. Integer color masks and
bit-parallel counters score all legal anchor positions with exact tie ordering.

Temporal repair propagates target wishes backward through an existing sequence.
It can insert an operation at any boundary or remove a low-value operation and
reinsert a better one elsewhere. This explores a different neighborhood from
changing the coordinates of an operation in its existing slot.

## Immutable score checkpoints

Every row passed the full 320-case CLI benchmark and submission-readiness checks.
The history includes source hashes, timing, and immutable evidence locations.

| ID | Stable score | Gain from preceding best | Change |
|---|---:|---:|---|
| 040 | 251,963,428 | 101,355 | Inverse cancellation, temporal repair, sparse routing |
| 041 | 252,038,607 | 75,179 | Four profitable routing steps |
| 042 | 252,085,720 | 47,113 | Five routing steps |
| 043 | 252,147,480 | 61,760 | Eight routing steps with size-dependent work |
| 044 | 252,152,063 | 4,583 | Wider deletion/reinsertion search |
| 045 | 252,192,457 | 40,394 | Twelve routing steps |
| 046 | 252,388,472 | 196,015 | Restore full039 core and exact bit-parallel scoring |
| 047 | 252,571,424 | 182,952 | Twelve fast routing repairs |
| 048 | 252,747,393 | 175,969 | Thirty fast routing repairs |
| 049 | 252,862,932 | 115,539 | Complementary cycle powers and shorter-generator revisits |

Additional relocation rounds, suffix-wish block reconstruction, causal block
reconstruction, color-scarcity weighting, and exact three-operation tail search
did not produce qualifying new bests. They were recorded without promotion.
Details: [experiments.md](experiments.md), [regret_experiments.md](regret_experiments.md).

## Verification and runtime follow-up

Canonical checks include 6,832 exhaustive insertion candidates, 180 deletion and
reinsertion comparisons, 1,200 injected inverse pairs, and 8,992 independently
simulated routing permutations. Reviews verify negative mask offsets, full count
carries, legal placements, tie order, remaining operation budget, stamp state,
and exact preservation of the original039 code outside the added stages.

The full history audit verified all 50 original checkpoint source hashes, all 320
frozen case hashes, and 16,000 case-input hashes across the reports. No prior
checkpoint was overwritten. Manifest SHA256:
`bd30204d28266a4d8c69f0dc028eec2ca8ac605d8e9f3f198fd1176f0ff506ac`.

Checkpoint049 passed its initial stable benchmark but had a borderline4.996s
maximum. Further isolated repeats found one real five-second timeout on a small
board. An early routing trial now attempts to reach the conserved-color upper
bound before the expensive late beam. It returns only at that proven bound;
failed trials preserve all inputs and continue the original search unchanged.
Independent AST, canonical, state-purity, and guard-integration tests passed.

The initial wrong small-board tracing harness expected a function absent from
this solver. That diagnostic failure was unrelated to output validity; the
correct deeper-beam tracer passed all13 cases. The actual timeout above is
recorded separately and motivated the runtime fix.

The early-bound-only version subsequently timed out on one of 36 maximum-size
holdouts. Exact speed ports address that broader runtime margin: cached target
masks, direct initialization of mismatch-count planes, deferred insertion tie
ranking, fused backward transitions, stable top-eight heap selection, and
parallel construction count updates. These preserve search decisions, random
draws, and results. An alternative update implementation was rejected because
its speed gain was inconclusive.

Additional correctness checks cover 1,800 mixed refinement updates, cached-row
isolation, 400 stable top-eight comparisons, 1,920 canonical construction
transitions, 64 escape/rollback checks, 32 clone checks, and 48 involutions.
The final integration audit confirms each component exactly matches its reviewed
source. No timer-based cutoff or benchmark-specific condition was introduced.

The selected runtime variant passed every final check:

| Check | Cases | Maximum wall time |
|---|---:|---:|
| Smoke | 20 | 3.775s |
| Frozen stable benchmark | 320 | 4.010s |
| Boundary/random readiness | 20, plus deterministic repeat | 3.067s |
| Slow-case repeats | 19 | 3.635s |
| Maximum N=30, K=180 holdouts | 36 | 4.795s |
| Small-board search holdouts | 13 | 3.766s |

All 320 scores equal checkpoint049. All 320 outputs are also byte-identical to
the early-bound-only variant, confirming that the subsequent speed ports preserve
its decisions. Relative to039, the final solver adds 351 matching cells across
the suite. The former small-board timeout passed four final repeats in
1.273–1.577s. The former large-board timeout finished in 2.881s with the same
722 matches and output hash.

Measurements use CPython3.12.12, one solver worker, five-second subprocess
timeouts, and include startup/output capture. The 4.795s maximum leaves only
0.205s on the slowest measured holdout; hidden-input or judge-machine runtime is
not guaranteed. No timing-dependent search cutoff was added.

This selection is a runtime-only tie, **not an eleventh score improvement**.
The ten strict checkpoints and `results/history.csv` remain unchanged.
`results/runtime_variants.json` records the separate selection, with six immutable
validation reports under `results/checkpoints/runtime_049_252862932.*.json`.
Final SHA256:
`3330e36b6f33ca8fe42b976ef11319b5536c2dcd137ba1b5c505b1e6079ca068`.

To reproduce the main checks from the repository root:

```powershell
python tools/benchmark.py submissions/runtime_049_252862932.py --suite stable --jobs 1 --output results/recheck_final_stable.json
python tools/check_submission.py submissions/runtime_049_252862932.py --random 12 --timeout 5 --output results/recheck_final_readiness.json
python tools/stress_solver.py submissions/runtime_049_252862932.py --timeout 5 --output results/recheck_final_stress.json
```
