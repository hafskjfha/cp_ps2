# Million-point campaign: sequence neighborhoods

All diagnostic candidates preserve the supplied runtime055 incumbent, are validated with the canonical output validator, and are scored with the canonical simulator and exact integer score. These files are research helpers, not submission checkpoints. No current solver, checkpoint, global history, or frozen input was changed.

The target is a measured stable320 improvement over254,652,429 while respecting5seconds. Prior campaign work already explored random distant pairs, Gibbs updates, coarse objectives, long-window reconstruction, and two-layer assignment, with weak returns. This probe investigates different coordinated operation neighborhoods.

## Exact relocation

`m2_sequence_relocate.py` evaluates every relocation of a contiguous block of one, two, or three operations, optionally reversing its order. Physical prefix states and target wishes propagated backward through suffixes give exact candidate scores without replaying the entire suffix. Each accepted block has an independent full reconstruction assertion. Twenty-four fresh random instances passed canonical score-preservation checks.

Development100: two complete rounds plus one refinement sweep gained1,111 points on one case, max incremental0.771s, total6.896s. This is too weak to integrate.

## Joint spatial shifts

`m2_sequence_shift.py` simultaneously translates every operation in a temporal segment. For each translation and left boundary, physical values advance under the translated operations while suffix wishes advance under the original operations, giving exact scores for every right boundary in quadratic time. Tested offsets were the eight cardinal/diagonal offsets at distances1,2,3.

Development100: two rounds plus one refinement sweep gave zero gains, max incremental0.401s, total2.468s. No integration is justified.

## Complete adjacent-pair optimization

`m2_sequence_exactpair.py` enumerates every legal first action in an adjacent two-operation window and finds the exact best second action through the existing bit-parallel refinement engine. This fills a gap left by earlier sampled pair neighborhoods. The bounded domain is N<=14 and K>=5.

Development100: two sweeps plus one refinement sweep gave zero gains, max incremental0.701s, total0.964s. Cached320 with eight sweeps gained11,019 points on two cases, but took39.672s total and9.301s maximum incremental runtime. This fails the runtime/usefulness tradeoff.

## Exact runtime optimization

The parent requested a pivot to freeing time for better constructors. Grouped color-mask updates and transposed geometry in `RefineState.apply` were both slower in microbenchmarks and are excluded.

`m2_sequence_init_fragment.py` packs each color's board cells into four-bit-spaced masks using byte translation, gathers legal placement rows with integer bit operations, and constructs every rotated value mask. Local mismatch counts are packed integer sums of shifted board masks. It uses the parent's exact fast rank-mask transpose. Large-grid initialization measured about2.8x faster for D3 and1.95x for D2; small grids retain the old initializer.

`m2_sequence_best_fragment.py` evaluates the formerly scalar `best_action` with the same exact bit-parallel gains and preserves incumbent/zero-gain tie semantics. It measured2.5–3.2x faster on N30; N<16 keeps the old scan.

`m2_sequence_csa_fragment.py` uses a fixed carry-save-adder network for the eight or eighteen value masks consumed by `RefineState.best`. Microbenchmarks measured1.3–1.7x speedup. No stochastic choices or score rules change.

The combined frozen candidate is `solvers/experiments/m2_sequence_runtime_csa.py`, SHA2562a69875f9a49f1180eac82f2abb22fc9f04259489c6375d706e4fee7805c42e8. It includes the parent's rank-mask improvement. Across56 configurations covering every N=3..30 and both D, all3,360 state-transition and `best` comparisons,2,240 independent canonical forward checks, and336 scalar-vs-packed `best_action` comparisons passed. Differential evidence is `results/m2_sequence_runtime_differential.json`.

Provisional paired end-to-end timings against the parent's rank-mask-only code: case0014.349→3.560s (18.1% reduction), case0073.714→3.551s (4.4%). Both stdout hashes matched checkpoint055 exactly. Other research was running, so these are not isolated qualification timings.

Full320 exact-output/canonical parity passed: all320 stdout hashes matched checkpoint055 and total score remained254,652,429. Runtime was369.373s total and3.707s maximum in the shared-load diagnostic with20-second timeouts. Evidence: `results/m2_sequence_runtime_parity320.json`. This is exact-output parity evidence, not a score improvement or isolated5-second submission qualification.

The optional extension `m2_sequence_runtime_final.py` adds two more exact optimizations. `m2_sequence_applylocal_fragment.py` unpacks each geometry row and value-bit row into a local variable once before applying the stamp; it measured1.14x for N30/D3/C6 and1.19–1.24x for N10/D3, unlike the earlier slower unrolling that repeatedly indexed outer lists. `m2_sequence_weighted_fragment.py` applies spatial gathers and the fast tie masks to `WeightedRefineState`, using packed byte counters to compute weighted region sums. Weighted initialization measured7.7–9.7x faster on N30 and1.9–2.6x on N10.

The optional combined extension passed56 configurations with5,376 exact state/best comparisons, including2,688 weighted transitions, and reproduced eight whole-case stdout hashes. Source SHA256060990ac1fa220243c1819ca93f148f136ac569ae4f9f48014d1f7f815d43d78. It has not independently completed320-case parity; the earlier CSA variant has. Eight provisional paired wall timings improved seven cases, roughly3.2% aggregate beyond the CSA variant. Evidence: `results/m2_sequence_runtime_final_differential.json` and `results/m2_sequence_runtime_final_paired.json`.

## Private packed forward beam

The parent requested a faster compact constructor to make wider beam widths feasible. `m2_sequence_packed_cluster.py` implements `PackedClusterState`, `clone_packed_cluster_state`, and `packed_cluster_choices`. Each action gets a six-bit field. Static stamp-to-target columns add into the current mismatch-count fields, producing exact action scores. Board updates adjust the field integer by the coverage mask, and a slotted state copies only mutable state. The score and top candidate group computed for a child's future value are cached for its subsequent expansion. Random-number calls, action ranks, stamp deduplication, and tie ordering remain identical.

In the quotient constructor, replace only `ClusterState`, `clone_cluster_state`, and `million_choices` with the packed symbols. The new state supports the existing seven-argument constructor and `.grid`, `.stamp`, `.matches`, `.apply`, and `.best` interface. It calls the surrounding solver's `build` when no action list is supplied. Keep the original engine for large cases unless an end-to-end timing supports the replacement.

One thousand random state/best/choices/RNG comparisons passed. Independent canonical checks covered another1,080 transitions, and576 explicit negative-gain/plateau checks also verified clone isolation. At N8/D3, clone+apply+best improved2.52x; at N16/D3 it improved1.74x. Cloning alone was about2x faster.

Four complete compact quotient constructors at width128 returned exactly the same operation sequences: case0410.886→0.576s,1170.435→0.279s,2010.733→0.489s,2610.427→0.306s. Four additional N17–21 cases also matched exactly, improving18–24% on three cases and6% on one. Evidence: `m2_sequence_packed_constructor.json`, `m2_sequence_packed_medium_constructor.json`, and the micro/negative diagnostic JSON files under `results/`.

The five-bit forward variant in `m2_sequence_packed5_cluster.py` is also exact on1,080 transitions and four complete compact constructors. It did not clearly improve whole-constructor runtime over six-bit fields, so six-bit is the recommended forward version.

## Private packed backward beam

`m2_sequence_packed_back.py` supplies `PackedFastBack` with the same constructor, `.first`, `.apply`, `.best`, and `.choices` interface as `FastBack`. Its state is private to the backward constructor; the first two elements remain the board and stamp. The third element becomes an integer of five-bit action fields, followed by cached score data.

For each action the base field equals D² plus wanted-board matches to the original stamp minus wanted-board matches to the original grid. It lies in0..18. Adding the current wanted-stamp match columns gives0..27, which fits five bits without field overflow. Changing one board wish adds the difference of pickup masks and subtracts the change in original-grid matches. The match subtraction for the carried stamp is computed while applying the operation. Cached maximum candidates preserve every subsequent random choice.

The kernel passed1,440 state/best/choices/RNG comparisons and7,200 field-counter comparisons. Apply+best measured3.70x faster at N8/D3,2.31x at N16,2.42x at N18,1.98x at N22, and1.47x at N30. Large D2 cases do not benefit in the microbenchmark.

Four full backward constructors at width128 returned identical operation sequences: case0074.715→3.758s,1370.866→0.501s,1861.508→0.952s,2702.184→1.388s. Requested width48 and128 parity probes on005/006/007/047/154/186/283 are being completed separately. These are runtime-only changes; they do not themselves increase score. Root is responsible for integrating stronger widths and qualifying the final submission.
