# Regret and reconstruction experiments

Parent: `submissions/best_039_251862073.py`; frozen stable320 score251,862,073.

## Exact suffix-wish gap reconstruction

Hypothesis: coordinate/triple local optimization cannot rebuild the action ordering of a longer gap. Remove a6/10/16-action contiguous gap, propagate its retained suffix backward into exact wishes for both board and stamp, then greedily construct a replacement in alternating forward/backward directions. Allow2 additional slots when K permits. Retain only strict canonical final-score improvements.24 fixed-seed trials.

Source: `regret_rebuild.py`; standalone helper fragment `regret_fragment.py`.
Tests:32 fixed-seed canonical suffix-boundary comparisons, exhaustive best-action deltas, score-floor/K checks, and repeatability comparisons passed.
Smoke20:17,967,254, allvalid, max3.453s; every score/hash equals039. Development100:80,325,470, allvalid, max3.857s, runtime99.920s; every score/hash equals039. This experiment is rejected without fullstable.

## Causal gap reconstruction

Hypothesis: rather than uniform windows, trace a currently wrong final cell backward through the operation permutation and remove a window centered on one of its transporting operations. Rest unchanged. Same32 canonical testcases pass. Development100:80,325,470, allvalid, max3.522s, runtime101.933s; no score gain, rejected without fullstable.

## Residual color-scarcity objective

Hypothesis: residual target colors with high unmet demand relative to movable supply are easily sacrificed by ordinary greedy match counting. Temporarily weight all target cells of either of the two highest demand/supply colors twice, apply one exact weighted suffix sweep and two ordinary sweeps, and retain a candidate only if true score improves. This can enter a different sequence basin while preserving parent floor.

Source: `regret_color.py`; fragment `regret_color_fragment.py`.
Tests:30 fixed-seed canonical score-floor/K/repeatability cases passed. Smoke20 and development100 tie every039 score (17,967,254 and80,325,470 respectively); devmax4.124s. Rejected without fullstable.


## Exact tiny tail and compact27 reconstruction checks

Exact up-to-three operations enumerates the first two operations and chooses the exact best third.18 canonical exhaustive optimum/K/determinism tests passed. The039 N5/D2 residual case ties; all18 eligible compact27 cases also tie. Rejected.

On cached compact27 outputs after cancelling adjacent inverse pairs, longer-gap reconstruction adds6,945 only oncase293; two-step gap reconstruction adds1,600 only oncase095. Full cached diagnostic preserves parent floors, but these gains do not justify source budget.32canonical tests also pass for two-step reconstruction.

## Binary-to-wildcard exact-search consolidation

Hypothesis: one generic wildcard target-condition join can replace the specialized binary BFS and additionally solve arbitrary-color short suffixes. Ported the previously verified039 packed transitions/backward-wish join, using an exact depth5 call in the original binary branch and depth8 suffix attempts after the new algebraic/temporal pipeline. Old binary search and generic replacement both exhaustively cover all paths through5, so existing binary perfect solutions are retained.

Frozen source: `regret_wildcard_source.py`, packed `regret_wildcard.py`, parent `algebra27_t5_r8_source.py`. Bytes9,989. To fit, removed only AST-dead `greedy`, and merged State.escape/ProductiveState.escape after AST-normalizing the one extra min_gain parameter and proving identity. Twelve N4/D3 diagnostic cases allvalid, max1.652s. Exact new gains:case156/180/296 each15¡æ16, +187,500 versus parent; expectedstable252,339,563 requiresfullqualification. Tests:384canonical packed transitions/involutions,30old/new binary success-existence parity cases,8reachable targets throughdepth8withpacked/source path equality,32escape-dedup parity cases. Report `results/regret_wildcard_verification.json`. All passed.

A separate modern source ports this helper after additional routing powers. Root is coordinating full qualification; routing agent is testing a further exact apply-method consolidation to fit the modern candidate under10,000bytes.


User correction relayed by root: source limit is100,000bytes, superseding the repository's earlier10,000-byte text. Stopped all further packing searches. The final modern raw source (`regret_wildcard_final_source.py`) uses the full routing power list[6,6,9,5,12,3,6,9,12]; function definitions were regrouped without changing bodies (all defaults proven literals, no decorators). Its10,010-byte packed file has not undergone final whole-solver parity; do not promote it without qualification. Root will instead port new temporal/routing logic onto039, which already contains wildcard completion and retains the stronger parent search. The verified t5_r8+wildcard candidate remains frozen, but no fullstable checkpoint was claimed by this worker.
