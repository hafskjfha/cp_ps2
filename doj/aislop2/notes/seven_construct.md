# Broad construction probes

All probes use the frozen development cases and the canonical simulator/output validator. They compare independently constructed candidates against the archived runtime053 score floor (`million_safe_stable.json`), retaining a candidate only if its true final match count is higher. Their added runtime is provisional because agents may be working concurrently; no new stable checkpoint is claimed here.

## Residual-shape beam

Hypothesis: the existing forward beam's immediate score plus one-step gain may scatter remaining mismatches into isolated cells. A small secondary reward for adjacent wrong-cell pairs keeps difficult cells near each other, which may improve late placement opportunities. Beam construction is followed by six exact single-operation refinement passes and two pair passes. Immutable parent solver and frozen suites are unchanged.

| Variant | Eligible dev cases | Gain over053 | Wins | Added maximum seconds |
|---|---:|---:|---:|---:|
| Cluster weight0.15, width16, first20 eligible |20|65,498|9|1.263|
| Cluster weight0.5, width24 |46|56,211|4|2.336|
| Cluster weight0.1, width24 |46|82,954|9|2.006|
| Cluster weight0.15, width16, all dev |46|77,650|10|1.380|

The coordinated frozen stable cached diagnostic for width16/weight0.15 improved40 cases by **321,463** total points, with42.833s aggregate added work and1.449s maximum. Every candidate was checked by the canonical simulator and output validator. This is a diagnostic retained-parent score, not a new standalone submission measurement. See `results/seven_construct_stable_m2_w16_s0p15_seed0_n320.json` and the reference-preserving helper `solvers/experiments/seven_construct_cluster_frozen.py`.

The faster exact helper stores remaining-wrong cells in a bit mask and updates adjacency by toggling touched cells in sequence. It is in `seven_construct_cluster_fast.py`. Its tested full-pipeline scores match the original helper; timing comparisons made while sibling agents run are provisional.

## Early integration

Rather than append another beam, insert the clustering candidate after `construct_all` and bypass the final `million_beam` in the affected domain. This reuses the existing later refinements. Whole-pipeline development comparison for `n>16,k>10` yielded+77,775 over053 (11wins,9losses,35cases). D3 contributed+77,862 andD2−87. Inserting into `construct_pool` instead yielded+81,333 but took slightly longer and did not improve the complementary domain enough to prefer it.

The selected integration domain is `n>16,D=3,K>10`, excluding the root agent's reverse-beam domain (at most4C distinct **unrotated** target patch tuples and initial matches below88% of the inventory bound, withN>=10,K>=12). On the exact final safe parent's affected16 development cases, early cluster insertion measured **+43,209**,7wins,2losses, maximum4.433s in the concurrent diagnostic. The full output was canonically validated. Losses werecase062(−6,172) andcase075(−3,472); this integration does not retain the previous per-case floor, so only a fresh full benchmark can qualify it as an improvement.

`solvers/experiments/seven_construct_integrated_fragment.py` is the4.8KB flat drop-in fragment. Insert it after existing helpers and before `main()` is called. It shares existing solver globals, introduces a separate `cluster_improve`, wraps `construct_all`, and wraps `million_beam` to remove the replaced stage. It is designed to compose with root's reverse constructor by excluding that domain.

Authoritative integration measurement: `results/seven_construct_integrated_early_w16_n100_fast_complement.json`. No further heavy benchmarks are running from this branch during root's standalone qualification.

### Exclusion-gate correction

The first integration fragment incorrectly counted all four target-patch rotations when excluding the reverse domain. Root's reverse constructor counts only unrotated patch tuples. Both the fragment and probe now use the exact root definition. A320-case static gate audit confirms that **all16 measured development memberships are unchanged**, so the measured+43,209 development delta still applies to this domain. Six stable-only cases change from cluster to reverse-only:143,154,186,247,270,294. Those paths must be covered by root's reverse measurement and the final combined validation; they have not been re-run here. Evidence is in `results/seven_construct_gate_audit.json`.

Prepared `solvers/experiments/seven_construct_combined_readable.py` by inserting the corrected fragment into root's readable reverse source before `main`. Parent source SHA256:390c3b5dfd7e502074c8679e1959cf3bae1ff4c3aab1eb21f4ffdb188dc1147d. The combined source compiles and preserves every original parent AST node; it is an unmeasured readable integration artifact and is too large for submission before compaction. See `results/seven_construct_combined_review.json`.

## Exact runtime optimization after combined qualification

Root's fresh combined stable benchmark subsequently measured254,652,429, all320 valid. The broad construction changes contributed to a548,531-point campaign improvement, below the requested seven million. Root requested a same-output runtime optimization because the boundary readiness maximum was4.901s.

The private `ClusterState` leaves unused `.counts` and `.stampmask` metadata unchanged, maintaining the exact mutable grid, stamp, match count, and score bit planes used by `million_choices` and `State.best`. Geometry coverage masks are built once on the initial state, then shared by all children. The private clone copies only grid, stamp, and score planes. A second equivalent variant stores grid and stamp as `bytearray` to make copying and state-key construction faster. Existing refinements reconstruct their own complete state from the resulting operation path.

Frozen bytearray readable source: `solvers/experiments/seven_construct_fast_bytearray_readable.py`, SHA256db33ee57d94a85e7ddbceb916e1cd7e23b12aeda8fe050b80fc9c5f44326f9d4. The only changed existing expressions select the private initial state and clone inside `cluster_improve`;103 other definitions are AST-identical. Both the list and bytearray private-state variants passed960 canonical transitions,960 exact `best` comparisons, and960 exact `million_choices` comparisons across16 configurations, all four rotations, D2/D3, and min/max N/C. Clone isolation and immutable unused metadata were checked.

Initial isolated standalone comparison (all outputs byte-identical):

| Input | Parent seconds | Planes-only lists | Planes-only bytearrays |
|---|---:|---:|---:|
| Stable case001 |4.846|4.387|4.170|
| Boundary N30D3C2K180 |2.491|2.410|2.244|
| Boundary N30D3C6K180 |4.823|4.415|4.588|

Whole-run timing has noise, so the helper was also measured twice on the C6 boundary. Mean cluster-helper time fell from1.336s to1.015s with lists and0.922s with bytearrays (about31% faster), with exactly identical operations in every run. See `results/seven_construct_fast_boundary_probe.json`, `seven_construct_fast_differential.json`, and `seven_construct_fast_bytearray_static.json`. This optimization changes runtime, not measured score. Root will qualify the exact packed bytes with a fresh stable run.

## Fresh long-window reconstruction hypothesis

After combined55,6,451,469 points remain to reach the requested threshold, versus a rigorous remaining ceiling of7,711,770. The N>=10,K>=24 domain has only5,913,993 ceiling and therefore cannot satisfy the request by itself, even if its bound were attainable. Broadening toN>=6,K>=8 covers7,006,103 relaxed headroom.6,615,993 of all remaining headroom lies on outputs that already use the full operation budget. Updated per-case evidence: `results/seven_construct_next_headroom.json`.

The new constructor experiment is joint long-window reconstruction, not another coordinate-refinement restart. Existing `i1_search_block` enumerates every placement for every beam state, so its160,000-transition limit commonly permits only short4-operation windows on larger boards. `seven_construct_window.py` instead uses bit-parallel ranked-action sampling to search12/24/32-operation windows at width24. It preserves the exact incumbent trajectory in the frontier at every depth.

For a window[left,right), the physical start is the true grid+stamp after the fixed prefix. The desired end is target+[wildcards] propagated backward through the entire fixed suffix, including desired stamp labels. Their agreement across allN²+D² coordinates equals the final global grid score for any replacement. Generalized `FastBack` supports the seven label values already; the experiment supplies the desired stamp at the right boundary instead of resetting it to wildcards. The bound counts all real desired labels across grid and stamp.

Three deterministic windows sample a12-operation suffix, a24-operation weak interval (ranked by its removal score under exact suffix wishes), and a32-operation seeded interior interval. Only strict global-score improvements are retained and independently re-simulated internally. This differs from the rejected destruction probes, which reconstruct by individual coordinate sweeps, and from the expensive all-placement shallow block beam.

The diagnostic driver uses the best cached053/complementary operations as seeds and compares outcomes against55's measured per-case score. It records `new_search_delta` separately to avoid attributing an already-better cached seed to the new search. Sources compile; measurement is intentionally held while root runs isolated qualification. No gain or runtime claim is made yet.

### Long-window results: rejected

The released diagnostic window evaluated all36 eligible development cases. Strict3-window reconstruction at width24 produced **zero new search points** over the combined55/current-best-seed floor, taking6.445s total and0.390s maximum. A single bounded variant accepted equal-score shorter or different blocks to move across score plateaus, then ran6windows; it likewise produced **zero new search points**, taking11.847s total and0.647s maximum.

The second variant improved old053 seed007 by6matches and seed021 by1, but neither exceeded55. Both reports also show13,471 points recoverable simply by choosing already-better053 cached paths on cases027/062/075; these are explicitly excluded from `new_search_delta` and are not credited to this search. Canonical validation passed for every diagnostic output, and the input seed score was retained.

Reports: `results/seven_construct_window_w24_r3_n100.json` and `results/seven_construct_window_w24_r6_n100_neutral.json`. Independent sequence-agent review found no scoring issue. A separate fixed-seed property check covers24 random instances, arbitrary non-wildcard stamp wishes, incremental reverse-action gains, exact global suffix equivalence, and full strict/neutral window replacements; evidence is `results/seven_construct_window_review.json`. This direction is not recommended for integration or full stable benchmarking.

Moderate weights yield a diverse useful candidate but fall far short of the requested seven-million stable improvement. A stronger weight sacrifices too many matches during construction. Results preserve full operation sequences for independent verification.

## Disjoint-patch assignment

Hypothesis: global assignment of disjoint initial patches to target patches could avoid greedy movement choices. A standard-library Python Hungarian assignment chooses each patch's destination and rotation. Cycles are realized legally through the stamp, then optimized by the existing exact sequence refinements. This is a structurally different constructor.

The first partition probe improved zero of46 eligible development cases, with maximum construction/refinement time0.560s. Fixed disjoint partitions leave too much freedom unavailable and produce weak starts for local refinement. Rejected; the implementation and measurement are retained as diagnostics.

Other rejected broad probes: border-priority beam(+38,148dev), deeper immediate-gain level sampling(+10,000dev), beam-parent diversity quotas(+29,507dev), and all-action structured-target two-step construction(+13,334dev but6.59s maximum added runtime). These did not beat the clustering variant's score/runtime tradeoff.
