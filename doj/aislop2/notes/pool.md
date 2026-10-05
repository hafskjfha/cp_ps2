# Constructor pooling, target weights, and exact update speed

All benchmark cases use the unchanged manifest. Timings below were usually
measured with other agents active; they are not controlled speed ratios.
Only immutable checkpoints selected by the root are global best submissions.
This agent does not edit current.py, submissions, checkpoint metadata, or history.

## Hypothesis and method

Raw constructor score can mis-rank paths after coordinate refinement. Preserve
the neutral-greedy, two-step lookahead, and productive-escape paths, refine a
small prefix of each, choose by the official final-grid score, and spend the
remaining sweeps on that choice. Comparisons use strict score improvement and
stable ties. The canonical simulator checks final-grid and stamp transitions.

Split refinement preserves the original input-derived random stream: an offset
burns the same number of complete action-order shuffles. Thus two sweeps plus
six with offset two match eight uninterrupted sweeps exactly. Later IL merging
adds an independent seed_offset argument; it does not change the continuation
offset. Differential tests compare both mechanisms with their scalar/original
implementations.

## Measured search experiments

- pool_two.py, based on best010: top two constructors receive two preliminary
  sweeps, then the winner receives six. Smoke 17,777,866, stable 246,940,264
  (+66,078 over best010), valid 320/320, max 4.218 s. Readiness 38/38, max
  3.343 s. Superseded by global best011 before promotion.
- pool_three.py (top three, one plus seven sweeps) was prepared but unmeasured.
  pool_bits_two.py and pool_bits_three.py use the exact accelerated refinement
  implementation. Split scalar/bitset sequence parity is tested.
- pool_all8.py: all three paths receive eight complete sweeps, then selection.
  Smoke 17,782,310, max 3.181 s. No stable run.
- pool_all16.py: all three receive sixteen sweeps. Smoke 17,814,860, stable
  247,296,280, valid 320/320, max 3.591 s. Later global best012 superseded it.
- pool_forward16.py uses best012 forward-walk construction and refines all
  three paths sixteen times (the refinement directions remain backward).
  Smoke 17,850,588, stable 248,256,087 (+219,318 over best012), valid 320/320,
  max 3.976 s. This exceeds selected-only walk32 by 20,225 but trailed best013.
- pool_extra8.py additionally retains the two best distinct discarded
  lookahead restarts and gives them eight sweeps. Smoke ties 17,850,588 while
  runtime rises; not advanced to stable.
- pool_twosided16.py uses eight backward sweeps followed by four forward and
  four backward sweeps. Smoke 17,847,128, below all-backward pool_forward16.
  Its exact forward suffix-wishes implementation is tested against an
  independent scalar model; the scheduling hypothesis did not pay off.
- pool_pairselect.py, based on best013: three paths get two sweeps, the winner
  gets six more, followed by the unchanged pair repair and final two sweeps.
  Smoke 17,797,494, stable 248,816,300 (+62,328 over best013), max 2.955 s.
  Readiness passed 38/38, max 2.252 s. Superseded by best014.
- pool_hybrid.py adds best014's pair sweep before repair. Smoke 17,829,298,
  stable 249,166,840 (+51,106 over best014), max 4.162 s. Readiness passed
  38/38, max 3.175 s. Superseded by best015.
- pool_beam.py preserves best015's exact K<=2 and beam K<=12 wrapper around
  pooled selection. Canonical small-case checks pass; no benchmark.
- pool_beam24.py preserves best016's extended K<=24 beam. Smoke 17,829,298,
  valid 20/20, max 4.249 s. No stable run of this unweighted merge.

## Weighted constructor

WeightedState assigns weight two to the outer D-1 cell rings and weight one
elsewhere. Four deterministic neutral-greedy restarts maximize weighted local
gain; the best prefix and final constructor comparison use actual unweighted
matches. Consequently the heuristic can prioritize difficult boundary cells
without changing the official objective or discarding an earlier better prefix.
Zero-gain moves avoid repeated outgoing stamp states.

Exact transposed action masks hold weight-one and weight-two matches. Six
binary planes encode weighted score plus the complement of the old region
count. Scalar best/tie comparison and canonical swap tests cover D2/D3 and
N3/N7/N30. The helper pool_weighted_fragment.py is explicitly a fragment;
every benchmarked solver inlines it and is self-contained.

- pool_weighted.py adds the fourth path to best014 raw selection: smoke
  17,808,185 (+6,568), max 4.084 s. No stable run.
- pool_weighted_pool.py gives it the same preliminary pooled refinement:
  smoke 17,835,866 (+6,568 over pool_hybrid), max 4.524 s. No stable run.
- pool_beam24_weighted.py merges this with best016: smoke 17,835,866; stable
  249,634,247 (+87,174 over best016), valid 320/320, max 4.545 s, summed
  235.787 s. Readiness 38/38, max 3.363 s. Superseded by best017.
- pool_beam24_extra.py is the extra-seed ablation with every weight set to one.
  Smoke returns exactly to 17,829,298, showing that weighted smoke gains come
  from the weighting rather than merely four additional restart seeds.
- pool_beam24_weighted_bound.py incorporates the root's verified global color
  conservation bound. WeightedState also maintains the actual match count.
  Small canonical and counter checks pass; this specific file has no full run.
- pool_coverage.py quantizes actual legal-placement coverage to weights one
  through three, giving corners more priority than edges. Three-weight binary
  planes match scalar best/tie and canonical transitions. No benchmark yet.

The conservation bound is sum(min(total supply, target demand)) across colors,
where supply includes the stamp. Constructors and refiners stop at this bound,
including already-optimal imperfect targets. The root verified the underlying
bound_hybrid against all 320 best016 scores before this transplant.

## Guided triple merges

pool_triple.py wraps the bounded pooled selector with best017's guided triple
refinement. Smoke 17,849,915 (+20,762 over best017), valid 20/20, max 3.679 s.

pool_triple_weighted.py adds the boundary-weighted fourth path. Smoke
17,867,678 (+38,525 over best017), valid 20/20, max 4.651 s. Stable 249,966,410
(+85,411 over immutable best017), valid 320/320, summed 210.048 s, max 4.181 s.
There are 22 improved cases, six regressions, and 292 ties. Gains split into
+22,570 on N<=16 and +62,841 on larger boards. This trails best018's 250,064,691,
so no checkpoint or readiness was requested for the frozen candidate.

pool_triple_preview.py applies a width-eight pair sweep to each candidate
after its two preliminary coordinate sweeps. Smoke 17,834,204, valid 20/20,
summed 25.298 s, max 5.002 s. Rejected: lower score than the plain selector and
insufficient runtime margin. Earlier pool_preview_pair.py was prepared on
best016 but not benchmarked.

pool_iterated_weighted.py merges the small-board iterated refinement from
immutable best018, retaining separate shuffle-continuation and seed offsets.
Twenty-four exact refinement checks and six canonical complete solves pass.
No smoke or stable benchmark yet; do not present it as an improvement.

## Exact delta accumulation

pool_iterated_fast.py changes State.apply and WeightedState.apply: accumulate
changed-cell match deltas into covered regions, then update each region count
and its binary planes once. Net-zero region changes are skipped. This replaces
rescanning every cell of each changed region. Actual grid/stamp swaps and
unweighted match counters remain exact.

Nine hundred randomized transitions compare all grid/stamp cells, match count,
region counts, binary planes, and best/tie choices to the original updates,
including ProductiveState. A 6,000-operation update-only kernel on N30 yielded
unweighted speedups 1.70x (D2 C2), 2.40x (D3 C2), and 2.50x (D3 C6); weighted
speedups were 1.78x, 2.38x, and 2.03x. These are kernel measurements, not whole
solver speed ratios.

pool_sa_fast.py isolates only State.apply from that change on the frozen
anneal_guided_walk_sa_short.py, which became immutable best020.

- Smoke: 17,845,089, all 20 scores AND output SHA256 values exactly match the
  parent, summed 20.116 s, max 3.468 s.
- Stable: 250,559,222, valid 320/320, all 320 scores AND output SHA256 values
  exactly match immutable best020, summed 251.145 s, max 3.906 s.
- Readiness: 38/38 passed, max 3.632 s. SHA and machine-readable evidence are
  in results/pool_sa_fast_stable.json and results/pool_sa_fast_readiness.json.

This is a verified exact speed refactor, not a score improvement. No checkpoint
was created by this agent. The root and simulator agent were notified that
State.apply is ready to port into their next candidates.

## Further isolated speed experiments

pool_sa_refinefast.py also accumulates RefineState region deltas, removing the
full region-count list copy per update. Five hundred interleaved grid/wishes
swaps compare every state field and best/tie choice. Update-kernel improvement
is modest: about 1.31x for N30 D2 C2, 1.01x for D3 C2, and 1.16x for D3 C6.
No full solver benchmark yet; it is separate from verified pool_sa_fast.

pool_sa_equal.py adds an exact full-board-stamp shortcut: for N==D, call
exact_two with min(K,2). Every reachable grid is a rotation of the original
grid or stamp, all achievable within two operations. Sixty random 3x3 D3
cases with K=1,2,3,180 match canonical exhaustive rotation-state enumeration
through four operations, using at most two operations. No score benchmark yet.

pool_sa_geometry.py is based on verified pool_sa_fast. It caches immutable
constructor geometry (regions, actions, scalar target masks, coverage) by
N,D,C,target. Mutable grid, stamp, counts, and bitplanes remain per instance.
Two hundred randomized transitions and changing initial grids/orders compare
all State fields and best/tie choices exactly. Sixteen N30 initializations
drop from 0.16-0.23 s to 0.049-0.084 s (2.7-3.3x initialization kernel speed).
Smoke: 17,845,089, all 20 scores and output hashes identical to best020,
summed 17.523 s, max 3.256 s. Stable parity PASSED: 250,559,222, valid 320/320,
all 320 scores AND output hashes match immutable best020, summed 245.231 s,
max 3.419 s. Readiness passed 38/38, max 3.582 s. The frozen State class is
qualified for integration into later candidates.

Thirteen tools.test_pool test groups pass. Unbenchmarked candidates above are
research files only; current global best remains whatever results/best.json
identifies. All saved benchmark/readiness JSON files retain solver hashes.

The research log was reconstructed from retained reports and experiment notes
after a Windows default-encoding write failed. Future writes use explicit UTF-8.

## Current retained-wrapper merge

Prepared pool_retained_large.py from immutable best021 (250,867,386). It keeps
the retained small-board IL/beam and pair-annealing wrappers. The N>16 parent
branch receives the weighted four-constructor pooled selector; the small-board
retained path still calls the original raw constructor. This isolates the
previously measured +62,841 large-board gain, while its interaction with later
annealing still needs measurement. State delta updates and constructor geometry
cache are included; RefineState remains the original pending the root's separate
cache parity checks. Six canonical full solves across branch boundaries pass.
Smoke/stable are pending behind the independent State-cache parity run.

pool_retained_cached.py additionally ports the root's RefineState geometry
cache with natural action bits and exact rank-plane tie breaking. Twenty-four
randomized four-sweep refinement sequences exactly match the uncached version.
Its smoke is pending the root's complete cached_best021 parity report.

The root's combined cached_best021 now has exact full-320 output parity, so
pool_dual_weighted.py is the active score candidate. It is based on immutable
best022 (250,872,488), incorporates both qualified cached classes, and changes
only the N>16 constructor selection. Five canonical branch checks pass; the
three N<=16 checks reproduce parent022 operations exactly. Smoke is
17,857,070 (+11,981 versus parent022's 17,845,089), valid 20/20, summed 20.259 s,
maximum 3.150 s. Full stable comparison is running. The earlier retained-large
and retained-cached files remain unbenchmarked preparations, not improvements.

Prepared pool_dual_weighted4.py to test more reliable preliminary ranking:
each of the four paths receives four coordinate sweeps, then the selected path
receives four further sweeps with RNG offset four. The selected path still gets
eight total constructor-refinement sweeps. This adds six extra sweeps across
the discarded paths relative to the two-plus-six policy. Smoke is pending;
the source is self-contained and does not change the frozen active run.

pool_dual_weighted.py full stable result: 250,921,331 (+48,843 versus immutable
best022), valid 320/320, summed 270.384 s, maximum 3.573 s. Fourteen wins,
two regressions, and 304 ties. Every N<=16 output hash is exactly unchanged.
Readiness passed 38/38, maximum 3.284 s. The integrated file directly passed
120 extra scalar-best/tie and canonical grid/stamp transition checks across
State and WeightedState, N3/N7/N30, D2/D3. Root notified for checkpoint
promotion; the source is frozen. The four-plus-four preview smoke is now running.

Root promoted the weighted selector as immutable best023 (250,921,331).
The four-plus-four preview smoke is 17,855,578, down 1,492 from two-plus-six,
valid 20/20, maximum 3.665 s and summed 22.362 s. Rejected without stable.

At the root's request, prepared pool_binary_composite.py by wrapping immutable
best023 with the frozen binary_transitions/binary_bfs helpers and solve wrapper
from binary_cached022.py. No weighted, cached, or annealing logic changes.
Sixteen canonical reachable N4/D3/C2 targets of depth one through five solve
perfectly within budget. Full smoke/stable await the root's binary readiness.

Binary readiness passed at the root and was checkpointed as best024.
pool_binary_composite.py smoke is 17,919,570, exactly the expected +62,500
over best023, valid 20/20, summed 18.905 s and maximum 3.113 s. Full stable is
running; disjoint per-case parent results predict 250,983,831, but this remains
an expectation until the composite run completes. The simulator agent is
preparing its independently validated weighted-refinement wrapper on this frozen
file and will wait for the complete comparison before running stable.

pool_binary_composite.py full stable PASSED: 250,983,831 (+48,843 versus
current best024), valid 320/320, summed 243.761 s and maximum 3.169 s. Every
output SHA256 matches the intended immutable parent: best024 for N4/D3/C2,
best023 for every other case. This equals the predicted disjoint sum exactly.
Readiness PASSED 38/38, maximum 2.873 s; root and simulator were notified with
complete evidence. No heavy jobs remain here, leaving room for the root's
exclusive stress check. The composite source remains frozen.

## Informed pair-annealing combination

Root saved the binary/selector composite as immutable best025 (250,983,831).
Generator's anneal_informed_cached.py independently measured 251,149,505.
Its only anneal_walk change replaces endpoint proposal mode one with
walker.state.best()[0]. Mode zero keeps the nearby-coordinate perturbation;
modes two/three remain random and mode four deletes an operation. This spends
one fifth of proposals on an informed endpoint, then exactly optimizes its
partner. Proposal budget, acceptance temperature, seeds and best-path retention
are unchanged (the random stream naturally differs when mode one skips draws).

Prepared pool_binary_informed.py from immutable best025, replacing only the
anneal_walk AST with the measured informed version. All other function/class
ASTs are identical to best025, including both caches, weighted selector and
binary hook. Sixteen direct 80-proposal annealing runs exactly match the
informed source's sequences and pass canonical legality and monotonicity checks.
No benchmark has been started; the root's exclusive informed-solver stress
window is still active.

Root stress passed and the informed source was saved as best026 (251,149,505).
The frozen pool_binary_informed.py smoke is 17,934,141 (+74,481 over best026's
17,859,660), valid 20/20, summed 18.235 s and maximum 3.037 s. The binary hook
accounts for +62,500 on case019; informed026 still leaves one mismatch there.
Full stable is running to measure the selector interaction with informed SA.

pool_binary_informed.py full stable: 251,280,679 (+131,174 over immutable
best026), valid 320/320, summed 255.970 s and maximum 3.311 s. Nineteen wins,
one regression, and 300 ties. Gains split into the binary hook's +62,500 and
the large-board selector's +68,674. Every small-board output outside the binary
domain is byte-identical to best026. Both cached classes, PairWalker, and the
informed anneal_walk also exactly match best026 ASTs. Readiness is running;
root notified immediately of the measured strict improvement. Source frozen.

Readiness completed: 38/38 passed, maximum 2.898 s. Root has complete promotion
evidence. No heavy jobs remain in this agent; the candidate stays frozen.

## Constructor escape undo

Root requested one exact constructor speed improvement after best028
(251,305,191), avoiding duplication of the already-qualified fast PairWalker.
Both constructor escape routines apply each trial swap and then undo it by
calling State.apply again, which repeats all changed-region delta work.

pool_constructor_base.py is immutable028 with the qualified fast PairWalker
from anneal_informed_fast.py. pool_constructor_undo.py additionally snapshots
the original region counts, bitplanes and match count once per escape call.
After scoring a trial, it swaps grid/stamp cells back directly and restores
those arrays and the original packed stamp mask. This preserves list identities
and avoids recalculating the same reversible deltas. Search order, candidate
selection, random draws and all scoring semantics remain unchanged.

Ninety-six differential escape calls across State/ProductiveState, D2/D3 and
N3/N9/N30 produce identical selected pairs, RNG states and complete instance
fields. All 14 pool test groups pass. Sixty-call N30 kernel timings (old/new):
D2 C2 0.3295/0.3127 s (1.05x), D3 C2 0.2161/0.1941 s (1.11x), D3 C6
0.2243/0.1824 s (1.23x). These are sequential kernel measurements; system load
was not isolated, so they do not establish a complete-solver speed ratio.

Smoke matches all 20 immutable028 output hashes and scores exactly:
17,942,045, valid 20/20, summed 21.994 s, maximum 3.555 s. This smoke coincided
with unit-test and other-agent load. Full stable output parity is running;
paired complete-solver timing against the fast-PairWalker-only control can
isolate the constructor contribution afterward.

pool_constructor_undo.py full stable parity PASSED: all 320 scores AND output
hashes exactly match immutable best028, total 251,305,191, valid 320/320,
summed 249.496 s and maximum 3.541 s under shared load. Readiness is running.
Root requested holding new heavy jobs afterward for exclusive triple-search
stress, so complete-solver paired timing remains deferred. Kernel improvements
above are the isolated evidence for the constructor change; no whole-solver
speed ratio is claimed from the shared-load totals.

Readiness PASSED 38/38, maximum 2.870 s. Both constructor escape methods and
the combined qualified fast PairWalker are ready for later integration. Source
is frozen; all heavy jobs are held for the root's exclusive stress window.

## Triple speed port

Root requested pool_triple_fast.py on generator's frozen
anneal_weighted_triple.py (measured 251,481,350). The source's State and
ProductiveState methods exactly match the previously tested constructor
control. Only State.escape and ProductiveState.escape were replaced with the
qualified snapshot-undo methods. An AST audit confirms every other statement,
function and class is unchanged, including the already-fast PairWalker and
TripleWalker. Thirty-six selected-pair/RNG/complete-state comparisons and
canonical applied-path checks pass on the combined source. No benchmark has
started: the root is coordinating the triple solver's isolated stress window.

Triple stress passed and the source was saved as immutable best030
(251,481,350). The port's entire module AST equals the measured source after
substituting back only the two original escape methods; the source SHA256 also
matches the measured triple report. pool_triple_fast.py smoke matches all 20
best030 output hashes and scores: 17,962,810, valid 20/20, summed 23.455 s,
maximum 4.186 s under shared load. Full stable parity is now running with one
worker, followed by readiness. This is a speed port and changes no search budget.

pool_triple_fast.py full stable parity PASSED: all 320 scores AND output hashes
exactly match immutable best030, total 251,481,350, valid 320/320, summed
297.994 s and maximum 3.696 s under shared load. Readiness is running. Root was
notified that the two-method speed port is ready for the next gap composition
once the final readiness gate passes. The frozen source retains the existing
fast PairWalker and TripleWalker without modification.

Readiness completed: 38/38 passed, maximum 3.203 s. Root received complete
parity/readiness evidence. No heavy jobs remain; pool_triple_fast.py is frozen.


## Independent suffix-wildcard review (2026-09-25)

Reviewed frozen `wildcard_suffix_fast.py` (SHA256 `c1ebe3678ced159e13741d50ee5fb53da4379c3fa679367412151f5dbbd1bf4e`) without edits. No correctness or operation-budget defects found: prefix replacement succeeds only at the complete target; the packed actions are involutions; forward/backward tails total at most min(8, remaining K). Failed attempts preserve the parent result. Verified 1,600 packed transitions against the canonical simulator and 800 wildcard-state involutions.

Ten fixed-seed N4/D3 holdouts crossed C2..6 with K20/180 and random, reachable, or near-target families: all legal, maximum2.077 seconds. Two instrumented high-color cases confirmed exact output reproduction and eight-move completion in the original finishing call, so three extra fully reachable C6 cases were added to exercise repeated suffix attempts. All three retained mismatches with inventory bound16, proving repeated-branch coverage; times2.024,1.978,3.885 seconds. All13 cases passed the hard5-second subprocess deadline, no stderr, canonical validation/scoring. Report `results/pool_wildcard_suffix_holdout.json` stores source/input/output hashes, complete inputs, fixed seeds, extra witnesses, and branch traces.

Runtime caveat: the search can make five independent bounded-depth calls and has no global elapsed-time/node cutoff. Extra case02 (K180,120-move reachable witness, seed2026092533) is useful for isolated tiny-domain stress, with measured3.885-second runtime under concurrent load. No claim of global worst-case timing is made from these13 cases.


## Lazy target-dependent wildcard cache (2026-09-25)

Hypothesis: suffix retries rebuild the identical backward BFS from the target with nine wildcard stamp positions. Reusing its exact ordered states/paths and16-byte position/color constraint encodings should reduce repeated-search cost without changing first-match choices. `pool_wildcard_cache.py` is based on immutable032 and changes only `wildcard_finish`, adds a lazy backward-record generator, and keeps one target cache plus shared packed geometry. The forward BFS remains unchanged; target changes replace the cache. Flattened match indexes preserve stable count sorting and the least forward-state bit tie.

`tools/test_pool_wildcard.py` passed40 exact path comparisons across repeated prefixes and mixed move budgets, canonical completion checks, and direct three-layer BFS order/constraint parity. Static readiness inspection has no errors or flags. Candidate SHA256 `9befeb3c50d815ef76402aaecc41d49c7b66cc759721ee25ab24107a92c1e86b`.

Paired sequential runs on all13 tiny holdouts preserved every output hash and canonical validity. Sum18.659 to16.802 seconds (1.11x); hardest C6/K180 retry case4.480 to3.369 seconds; two C6/K20 retry cases2.156/2.154 to1.910/1.906 seconds. These are one paired pass under concurrent system load, not a global worst-case guarantee. Reports `results/pool_wildcard_cache_holdout.json` and `results/pool_wildcard_cache_affected.json`. All12 affected stable N4/D3 cases preserved032 output hashes, max1.811 seconds. Full320 parity is running; no qualification claim yet.

Qualification complete: all320 stable outputs match immutable032 byte-for-byte, same total251,668,850, all valid, max3.695 seconds (aggregate311.761 seconds under shared load). `results/pool_wildcard_cache_parity.json` records hashes and manifest identity. Submission readiness passed38/38, max3.714 seconds. The cache on the hardest tiny holdout retains35,712 backward records (~5.67MB for list/tuples/path bytes/constraint bytes, excluding transient BFS dictionaries); exhausted generation releases transient search state. Import-free port fragment: `solvers/experiments/pool_wildcard_cache_fragment.py`, containing both cache globals, `wildcard_backward_records`, and `wildcard_finish`; existing `packed_transitions` remains unchanged. This is a score-equivalent speed improvement, so no new score checkpoint is requested.


## Combined exact speed baseline on034 (2026-09-25)

`pool_all_fast.py` composes the fully qualified target-dependent wildcard cache onto frozen `anneal_late_snapshot.py` (parentSHA16546ee2bbd2c318292962ae11abc3d442e9511293fa1d4486a12099deecdcf8). The parent snapshot source subsequently passed all320 output hashes against immutable034 and its readiness checks. CandidateSHA87341a360f3fa1eb151c42c2611a99f914fe3649af2856af69056a7cd24c6c57. Only wildcard_finish changes from that parent, with two cache globals and the lazy backward-record helper added; no search budgets changed.

Light composed-engine checks passed16 nested snapshot/canonical transition cases and5 exact wildcard completion paths. Smoke20 outputs exactly match034, total17,962,810, max3.282 seconds. Merge audit and smoke reports are `results/pool_all_fast_merge.json` and `results/pool_all_fast_smoke.json`. Combined full320 parity/readiness gate is running; candidate is frozen. The separate four-repair cap experiment belongs to root and is excluded from this source.

Combined source qualification completed: `pool_all_fast.py` reproduces all320 immutable034 output hashes exactly, total251,734,381, all valid, max3.287 seconds and aggregate281.446 seconds under shared load. Readiness passed38/38, max3.316 seconds. Reports: `results/pool_all_fast_stable.json`, `results/pool_all_fast_parity.json`, `results/pool_all_fast_readiness.json`. SourceSHA87341a360f3fa1eb151c42c2611a99f914fe3649af2856af69056a7cd24c6c57 remains frozen. This is an exact speed baseline awaiting any separately coordinated isolated timing; no search-cap changes and no new score checkpoint.


## Four-move commutator append preparation (2026-09-25)

Hypothesis: a single PQPQ or QPQP append over overlapping placements can relocate remaining mismatches while undoing much of the stamp disruption. `pool_commutator_append.py` wraps frozen `late_beam_four_fast.py` without modifying any parent named unit. It runs only for N<=16,1..12 remaining mismatches,>=4 spare operations, and below the inventory bound. Deterministic input-seeded order examines at most20,000 unique unordered overlapping action pairs, both inverse words, with P focused on a mismatch. Each trial scores exactly the union of touched grid cells and undoes all four swaps. Only the best strict final match gain is appended; reaching the inventory bound exits early.

Preparation tests passed5 methods in `tools/test_pool_commutator.py`:576 exact canonical word deltas with complete grid/stamp restoration,16 repeated deterministic bounded-tail cases, K/parent-floor guards, a guaranteed positive four-move completion, and exact pair-cap enforcement. Static self-contained inspection passed. Report `results/pool_commutator_prepare.json`; candidateSHA0f98fc940dc3283dd15ab0b8a8bb0f3f7955285354dbc9fc1ec1e9688aa6d68a. Smoke/stable benchmarks are deliberately held for root isolated timing; no score improvement claimed.

Commutator smoke20 and dev100 are valid and tie035 exactly; none of the smoke cases and four dev cases satisfy its guards. Enumerating parent results finds11 eligible stable cases. The seven remaining eligible cases all passed; case173 (N13,D3,C3,repeated_stamp) gainsone matched cell, +5,917 score, with the others tied. Maximum of those seven runs2.446 seconds. Reports `results/pool_commutator_{smoke,dev,remaining,eligible,comparison}.json`. Full320 benchmark is now running because the targeted gain is positive and runtime remains plausible; no global best claim yet.

Commutator fully measured: stable251,771,548 (+5,917 over035), all320 valid, one win/no losses and319 byte-identical outputs. The sole win is case173 byone matched cell. Stable max3.252 seconds, aggregate316.381 under shared load. Readiness passed38/38, max3.088 seconds. SourceSHA0f98fc940dc3283dd15ab0b8a8bb0f3f7955285354dbc9fc1ec1e9688aa6d68a remains frozen. Reports `results/pool_commutator_stable.json`, `results/pool_commutator_readiness.json`, and updated comparison. Import-free `pool_commutator_fragment.py` contains three append functions; integrating it requires renaming the prior solve to solve_without_commutator. Parent notified for checkpoint promotion; this agent does not edit history/current/submissions.


## Independent planes-only RefineState review (2026-09-25)

Read-only review of `refine_planes_only.py` found no correctness or integration defect. AST changes from035 speed parent are limited to RefineState and the None-aware refine_trial helper; WeightedRefineState is unchanged. All counts use sites were audited: ordinary refinement uses planes, snapshots retain the None sentinel, State/WeightedState/beam counts stay lists, and weighted refinement is separate. Borrow/carry is bounded because each +1 match cell was previously unmatched and each -1 match cell was previously matched in every covering region; deficits remain0..D² and fit four bits.

Three independent oracle tests passed in0.702 seconds:21 extreme initial states,168 mixed actual/wish transitions,120 scalar best/tie checks,16 nested snapshot pairs, both geometry-cache warmup orders over8 cases,96 weighted-state transitions, and724 exact cover-mask checks. Tests `tools/test_pool_refine_planes_review.py`; report `results/pool_refine_planes_review.json`. No solver edit or heavy benchmark was performed.


## Independent deeper-beam13-case holdout (2026-09-25)

Ran the fixed13 recipes from `tools/anneal_late_holdout.py` on frozen `late_beam_deeper.py`, including all three declared reserve cases. New harness `tools/pool_deeper_holdout.py` leaves the prior harness untouched. Official timings execute an unchanged solver snapshot with a5-second hard timeout; separate diagnostic subprocesses wrap only solve_without_deeper_beam/deeper_beam_finish and temporarily count packed-expansion calls and completed heap-selection layers. Every diagnostic output must match the official output after newline normalization.

All13 passed canonical legality/scoring and exact diagnostic output parity. Maximum3.374614 seconds, mean2.541806 seconds, explicitly under shared machine load. Six cases entered actual deeper search; four reached depth8; three found strict repairs. reachable_n7 succeeded with an eight-move tail, directly covering the extended depth. All13 preserve the reference score floor, and frozen source remained unchanged. Report `results/pool_deeper_holdout.json` includes full inputs, recipes, hashes, depth/frontier evidence, and timing scope. No solver edits or extra unplanned cases were needed.


## Global and local three-move patch exchanges (2026-09-25)

Evaluated root frozen `late_patch_swap_append.py` (global PQP/QPQ) and `late_palindrome_append.py` (local ordering) only on all13 stable cases eligible against035: N<=16,>=3 spare moves,1..12 mismatches, below the inventory bound. Global was valid13/13 and gainedone cell/+5,917 on case173 only, duplicating the existing commutator gain; max2.696 seconds. Local was valid13/13 and gainednothing, max2.479 seconds. Full035 runs were therefore skipped. Reports `results/pool_patch_swap_subset.json` and `results/pool_patch_swap_local_subset.json`.

Bounded follow-up `pool_patch_swap_after_comm.py` retains immutable036, then tries one qualified global PQP appendix. AST audit preserves every parent definition;36 extra canonical word-delta/restoration checks passed, static self-contained inspection is clean. All13 cases eligible against036 passed. Case173 gainsanother cell/+5,917 beyond036, all others tie; maximum2.679 seconds under shared load. CandidateSHA69871376e245b0d259249fb6c9d7dba6224f10e5d0c42db02972a27924d2f9d6 is frozen. Reports `results/pool_patch_swap_after_comm_{merge,subset}.json`. Smoke validation is running; no full-stable or new-best claim yet.

036+PQP smoke validation passed20/20, score17,962,810, max3.434 seconds. Per root coordination, no full run is needed on that superseded parent. Prepared `pool_all_repairs_patch_swap.py` on frozen `forward_all_repairs.py`, then `pool_all_repairs_patch_stamp.py` by appending the root stamp-aware width384/depth8 helper. ParentSHA8494b5931955f69e0e7f9a7fa0a882788eba681820e755c574e3cf1e81c3e9eb; finalSHA83150fbf9b981f6118493cf479d4fcc0108c56b84f44d449bc328be783d578da. All parent AST units remain unchanged under wrapper renaming. Light integration tests passed exact end-to-end disjoint PQP completion, K guard, andfour canonical nonempty-prefix floor checks for the stamp-aware layer; static inspection clean. Final-source gates (smoke/dev,173/265, then full if improved) are held until the all-repairs parent qualifies. Merge report `results/pool_all_repairs_patch_stamp_merge.json`.

Final patch/stamp gates passed on039 parent: smoke20 and dev100 output hashes are all identical to039; dev score80,325,470, max3.441 seconds. Targeted173 gainsone cell/+5,917 (3.058 seconds),265 gainsone cell/+12,345 (4.162 seconds), total+18,262 on the two targets. Generator received green for the single complete full320 with its low-K component. Gate report `results/pool_all_repairs_patch_stamp_gates.json`; no full run was duplicated on the intermediate source.

Independent complete-source runtime holdout: `tools/pool_complete_holdout.py` wraps stamp_beam_finish and solve_without_stamp_beam in separate diagnostic processes, preserving the earlier deeper harness. All13 fixed recipes passed canonical legality/scoring and exact normalized output parity on frozen `anneal_all_repairs_complete.py`. Maximum4.378736 seconds (reachable_n9), mean2.919154 seconds, explicitly shared machine load. Six cases actually search, and all six complete eight unsuccessful layers at retained width<=384, covering full-depth search cost. No extra independent-input repairs were found. All preserve the parent floor. Report `results/pool_complete_holdout.json`; final-source SHAe6e70f3990f80540f45ae1c3df8b30587cfada22ccb9735708b9a112d47ffd0e. Source unchanged; worker released after completion.
