# Compact gap-search campaign

Baseline: runtime055, stable320 score254,652,429. All diagnostics use the frozen manifest, current055 cache (`results/m2_parent_cache.json`), canonical simulator, and exact integer scoring. No checkpoint or shared score log was modified by this branch.

## Qualified fragment: exact three-cell cycle tail

`solvers/experiments/m2_gap_cycle_fragment.py` is the integration fragment. Append it before `main` after all existing solver definitions. `m2_gap_cycle_integrated_readable.py` is the complete readable integration with runtime055's readable source. It is a research artifact requiring packing before submission because the readable parent exceeds the submission source-size limit.

For D3, two corner-overlapping stamp placements generate a five-cycle when repeated three times. Multiplying this pattern with the corresponding half-turn pattern cancels to an exact three-cell cycle in12 operations. Conjugating a cycle by one legal stamp operation moves its three affected locations and adds2 operations. A bounded breadth-first search explores these conjugations and returns the first strict score improvement. The final stamp remains unconstrained. The generalized helper also supports desired labels in the stamp and wildcard labels in grid cells, for exact interior-window research.

The integration applies only for N>=5,D3 with at least12 spare operations and an inventory gap. It adds up to3 improving cycles, with at most1,000,000 conjugation transitions per attempt. Improvements are tested during child generation so the bound does not discard useful generated children. It retains the parent path and never accepts a worse score.

Full-pipeline existing-evaluator run on all7 stable inputs with applicable spare budget and an inventory gap:

| Case | Parent matches | New matches | Exact score gain |
|---|---:|---:|---:|
|062|317|320|9,259|
|152|22|23|40,000|
|168|35|36|27,778|
|173|166|167|5,917|
|185|120|121|8,265|
|221|168|169|5,918|
|298|322|323|3,086|

Total gain: **100,223**. Every output was canonical-validator valid. Maximum full-pipeline runtime was3.997s during a concurrent research session; timing is provisional until parent qualification. All other stable cases bypass the repair or stop at the existing inventory bound, retaining their operation sequences. This is a domain integration measurement, not a fresh320-case standalone qualification and not a checkpoint.

Evidence: `results/m2_gap_cycle_integrated_allspare.json`. The earlier small-domain full-pipeline run (`m2_gap_cycle_integrated_eligible.json`) verified6 unchanged stdout hashes and2 wins before the domain widened. Canonical random validation covered60 small near-target instances and80 additional near-target/generalized-wish cases spanning N5,6,7,8,11,13,18,30 and C2–6, including max-size geometry (`m2_gap_cycle_validation_broad.json`). Every returned score equaled canonical simulation, every path was legal, and every result retained the input score.

## Other measured probes

- Forward/backward beam-frontier joins used bit-sliced agreement to compare all seam states exactly. Width768 and4096 produced no wins on the five largest compact-board gaps. Width4096 took up to9.37s and is rejected. Sources/results: `m2_gap_mitm*`.
- Exact two-step ranked packed beams also produced only a20,408-point candidate on case276, with no gain on the other four compact cases. Sources/results: `m2_gap_packedlook*` / `m2_gap_look*`.
- Existing reverse beam at width512/branch12 gives case27631→32 (+20,408), maximum0.401s across the five compact probes. Width1024 and4096 did not increase that gain. This remains optional and unintegrated; width512 provides the best measured score/runtime tradeoff. Results: `m2_gap_reverse512.json`, `m2_gap_reverse1024_eligible.json`.
- Exact cycle replacement of weak12/14/16/20/24-operation interior windows found zero development gains. It was rejected (`m2_gap_cyclewindow_100.json`).
- Coordinate descent over six-operation repeated-pair macros found +7,378 stable cached diagnostic points: case075+3,472 and158+3,906, with maximum0.202s and no regressions. It propagates real suffix wishes through stamp coordinates, so the gains are global exact scores. Source `m2_gap_macrorefine.py`, result `m2_gap_macrorefine_320.json`. This is unintegrated and needs separate random differential validation before promotion.
- Joint lookahead over adjacent six-operation macros (24 alternatives, at most4 windows) only recovered case158's same3,906 points and cost up to0.663s. Rejected in favor of the simpler macro sweep (`m2_gap_macropair_320.json`).

The compact-domain broad search did not produce the requested300,000-point contribution; the strongest qualified fragment contributes100,223 points with a small, bounded addition to runtime.
