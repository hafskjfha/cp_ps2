# Forward search research

Current reference: best_010_246874186.py, stable 246874186, smoke 17764025,
maximum holdout runtime 3.559s. Frozen benchmark remains unchanged.

## Hypothesis 1: exact depth-three rescue after two-ply exhaustion

The existing fast bitset search stops when no sampled two-move transfer has
positive total gain. A three-move transfer may first collect a useful stamp,
then move an obstructing grid patch, and finally place the collected colors.
At otherwise terminal local maxima only, inspect 24 diverse first moves with
gain >= -2, up to four best non-undo second moves, and the exact best third
move. Execute a triple only when its exact total gain is positive and three
operations remain. This preserves the original constructor path as a prefix
and limits extra cost to plateaus where the existing search would stop.

Hypothesis recorded before implementation. Smoke/stable/runtime measurements
will decide whether the added forward search deserves inclusion.

Depth-three smoke: 17814331, +50306 versus best010; 20/20 valid,
maximum 3.220s with two workers. Canonical differential checks pass 100
tentative-search states, exact undo, gain accounting, and small K budgets.
Stable: 247272076 (+397890 versus best010), 320/320 valid, maximum
3.224s; readiness passed 38/38, maximum 2.814s. Source frozen and reported
to root for potential checkpoint promotion.

## Hypothesis 2: bounded neutral/lossy transfer walks

Some stamp routing requires more than three moves. After a constructor would
otherwise stop, explore two bounded walks of at most six two-operation
transfers. Permit total pair gain down to -1, exclude immediate undo, and
avoid revisiting carried stamps at the same score. For each transfer inspect
24 diverse first stamp states and up to four tied best second placements.
Keep only a prefix with strictly positive cumulative gain, undo all trial
operations, then execute the best prefix. This tests longer coordinated
transfers without accepting a worse answer or increasing operation budgets.

Walk smoke: 17812548 (+48523 versus best010), 20/20 valid, maximum 3.895s
with concurrent benchmark work. Canonical tests pass 50 random walk states,
exact restoration, operation bounds and improving-prefix checks. The next
walk variant incorporates root's independently tested exact bitset backward
refinement acceleration; require equal smoke outputs before stable scoring.

Fast walk retained all 20 original smoke output hashes. Stable 248036769,
+1162583 versus best010 and +764693 versus depth-three rescue, 320/320
valid, maximum 2.481s; readiness passed 38/38, maximum 2.539s. Candidate
frozen as forward_walk_fast.py and reported to root.

## Hypothesis 3: depth-three productive decisions

The productive constructor currently ranks first moves using a two-step
forecast. Rank eight diverse positive first moves by the best match count
reachable within three moves, considering up to four tied best second
placements. Execute only the first (strictly improving) move, then replan.
The other two portfolio constructors remain unchanged for this ablation.
Use exact fast backward refinement to reserve runtime for the forward beam.

Productive depth-three smoke 17787611 (+23586 versus best010), 20/20 valid,
maximum 2.774s. Stable/readiness pending, one benchmark worker.

Productive depth-three stable 246664463, -209723 versus best010; all 320
valid, maximum 2.328s; readiness 28/28, maximum 1.256s. Rejected as a policy
replacement despite the small smoke gain.

## Hypothesis 4: explicit beam over short operation sequences

For K<=12, preserving several entire grid/stamp states can avoid greedy
decisions that waste a large fraction of the budget. Explore a width24 beam,
up to eight candidate actions per state drawn from the best three immediate
gain levels. Rank children by current gain plus half their next best gain,
keep stamp diversity, and preserve the best prefix. Copy only mutable State
arrays, sharing geometry and target bitsets. Compare the refined beam path
with the existing refined constructor output so the new branch cannot lower
score; K>12 follows the existing solver exactly. The threshold bounds work
by operation budget and is not based on benchmark case identity.

Short-beam smoke ties the walk reference exactly at 17812548. Because few
smoke cases exercise K=2..12, development100 is being measured before a
full stable run. Clone isolation and reference-score-preservation checks
pass on canonical simulations.

Short-beam development100 improves the walk reference by 62359 total,
with three improved cases and no regressions; 100/100 valid, maximum
2.411s. Short-beam stable: 248453708, +416939 over walk_fast across ten
improved cases and no regressions; 320/320 valid, maximum 2.318s. Readiness
passed 38/38, maximum 2.145s. Candidate frozen and reported to root.

## Hypothesis 5: depth-three fallback after transfer-walk exhaustion

The paired walk cannot use a last budget of three operations, and its
sampled neutral transfers may miss a direct profitable triple. Keep the
entire walk constructor unchanged until it would stop, then invoke the
independently tested depth-three rescue. This adds only improving triples
to formerly terminal paths and avoids replacing successful paired walks.

Walk+three smoke 17815748 (+3200 versus walk), all 20 valid, maximum
1.955s with one worker. Walk+three stable: 248087044, +50275 over walk_fast
across nine improved cases and no regressions; 320/320 valid, maximum
2.309s. Readiness passed 38/38, maximum 2.246s. Its changed cases all have
K>12, complementary to the short beam. Candidate frozen and reported to root.

## Hypothesis 6: exact search for K=2

A two-operation budget admits an exact search using the fast all-action
bitset maximum. Enumerate each first action, apply it, find the exact best
second action, then undo it. Consider zero- and one-operation prefixes too.
Sort first actions by immediate gain; once first_gain+D² cannot exceed the
best two-operation gain, prune the remaining first actions. This yields a
provably optimal answer for K=2 without relying on greedy tie diversity or
sampled transfer candidates. K=1 uses the exact immediate maximum. Other
budgets keep the existing short-beam/walk solver unchanged.

The exact two-operation implementation matches exhaustive canonical
simulation on 20 random small boards. Benchmark validation is pending.

## Hypothesis 7: combine verified complementary forward policies

Integrate the short-budget beam and the post-walk triple rescue, which had
disjoint affected budget ranges in the fixed benchmark. Include the exact
K<=2 branch and verify the concrete combined file. Its measured score must
not be inferred from the two separate reports; benchmark the actual solver.

Combined forward solver smoke 17815748, stable 248509900, all 320 valid,
maximum 2.368s. Readiness passed 48/48, maximum 1.832s. The exact small
branch adds 5917 beyond the simple sum of the prior beam and triple gains.
This is below the new sequence-repair global best, so retain it as a tested
forward-search component rather than promote it alone.

## Hypothesis 8: preserve the stronger sequence-repair parent, add short beam

Root requested integration into frozen anneal_pair_hybrid.py, measured at
249115734 while readiness completes. K>12 follows the parent unchanged;
K<=2 returns the exact optimum; K=3..12 compares the parent's final output
with the separately refined finite-beam output. Initially omit a second
pair-repair pass on the beam candidate to retain runtime margin. The final
comparison uses actual grid matches, guaranteeing no lower score than the
parent for any input (subject to the independently tested exact K<=2 branch).

Hybrid-beam smoke 17801617, all 20 valid, maximum 3.220s. Full stable and
readiness running. Additional canonical tests verify parent-score retention
on K=1,2,3,5,8,12 and exactly identical parent operations for K=13,20.

Hybrid-beam stable: 249389357 (+273623 versus parent), 320/320 valid,
maximum 3.526s. Readiness passed 38/38, maximum 3.371s. All cases have
nondecreasing score; every K>12 output hash matches the parent exactly.
Frozen candidate and reports sent to root for global checkpoint promotion.

## Hypothesis 9: bound beam work by nodes, extend to moderate K

For K=13..24, use width12 instead of width24, keeping the maximum number
of expanded children near the original 24*8*12 bound. Compare this extra
beam candidate against the same parent result, while K<=12 retains the
existing beam and K>24 remains unchanged. This tests whether moderately
long horizons benefit without increasing the search's worst node budget.

Budget24 smoke ties the short version at 17801617; all 20 valid, maximum
3.419s. Development100 scores 79394951, all valid, maximum 3.716s.
Within newly enabled K=13..24, three cases gain 10619 total over the parent
and the remaining seven tie. Full stable measurement is warranted.

Budget24 stable: 249547073, +157716 versus the short hybrid beam, all
320 valid, maximum 4.120s during concurrent work. Every case is
nondecreasing, and all outputs outside K=13..24 remain byte-identical.
Readiness is the only remaining active process before root's exclusive
runtime stress window; no further heavy research runs will be started.

Readiness passed 38/38, maximum 3.433s. All pipelines are finished and
root was notified that the exclusive stress window can start. Candidate
forward_hybrid_budget24.py and its reports are frozen. Eight persistent
forward test groups pass, covering canonical transitions, tentative undo,
positive-prefix retention, clone isolation, exact two-move optimality,
parent-score preservation, and operation-budget boundaries.

## Hypothesis 10: shallow beam with greedy rollouts for large K

For K>24, keep a width12 beam for the first four moves, then greedily
complete up to eight diverse leaves using positive and novel neutral moves.
Preserve the best prefix throughout, refine only the best completed path,
and compare its actual final grid with the existing parent's output. This
tests opening-sequence diversity without maintaining a full beam for 180
moves. Geometry and target bitsets remain shared across cloned states.

Planned extra work is bounded by roughly 1704 state transitions (beam plus
rollouts), 37 scalar candidate scans, and one eight-sweep refinement. Target
added runtime is under roughly 0.6 seconds, pending measurement. The root
agent completed the exclusive stress window and released heavy runs; use
one benchmark worker. Parent maximum measured holdout is 3.697 seconds.

Rollout smoke: 17805077 (+3460 versus parent), 20/20 valid, maximum
4.280s under current load. Total smoke runtime 25.025s versus roughly
21.2s for parent: mean added cost about 0.19s, observed maximum increase
up to roughly 0.9s, exceeding the initial 0.6s estimate. Full stable,
readiness, and a required isolated maximum-size timing check determine
whether the tradeoff is acceptable. Wrapper explicitly retains each input's
parent answer unless actual final matches improve, and skips added work
when the parent reaches the global available-color upper bound.

Rollout stable: 249577684 (+30611 versus budget24), 320/320 valid,
maximum 4.502s with current contention. Readiness passed 38/38, maximum
3.179s. All scores are nondecreasing and all K<=24 output hashes remain
identical. Total benchmark process time 232.420s versus 218.552s for the
parent, a rough +0.044s mean increase with differing machine contention.
This modest score gain requires an exclusive max-size timing check before
promotion. No active benchmark processes remain; root has been notified.

Rollout was superseded by guided-triple best017 (249880999), so no exclusive
stress run or promotion is warranted. Retain it as a measured experiment.

## Hypothesis 11: exact weighted backward coordinate refinement

Use parent best017. Attach small integer weights to final target cells,
then propagate weights alongside wished colors when moving backward through
the suffix; initial stamp wishes carry weight zero. Optimize the exact
weighted objective at each coordinate using bit-sliced action gains.
Evaluate boundary weight2/interior1 and rare-target-color weight2/default1,
one weighted sweep followed by two ordinary sweeps for each scheme. Keep
the parent unless actual unweighted final matches strictly improve.

Required pre-benchmark checks: compare every selected action and reported
weighted gain against exhaustive canonical permutation scoring; validate
wish-color/weight swaps, including equal colors with unequal weights; prove
the weighted sweep never lowers its own fixed final-cell objective. Planned
extra cost is six total sweeps, two weighted, targeting less than 0.5s worst.

Pre-benchmark oracle checks pass: 525 randomized cut states compare the
selected action and weighted gain to exhaustive canonical permutation
scoring, with interleaved actual/wish/weight swaps. Thirty random sequences
preserve their exact weighted final-grid objective across two full sweeps.

Weighted refinement smoke: 17836074, all 20 valid, maximum 4.402s with
concurrent research load; total process time 22.479s. The measured source
is frozen. All own benchmark processes have finished and new heavy runs
are held for root's exclusive SA runtime stress window.

The smoke delta is +6921 versus best017, solely the N17 D2 C3 K90
striped case. Parent floor holds on all 20 cases. New SA-short already
scores 17845089 on smoke, so weighted refinement will need rebasing before
it can establish a new global result.

## Hypothesis 12: weight the parent's unresolved target cells

Static boundary/rare-color weights may emphasize cells already satisfied.
Instead, give weight2 to target cells mismatched by the parent answer and
weight1 elsewhere, optimize this fixed weighted objective for one sweep,
then run two ordinary sweeps and retain the parent floor. This permits a
single repaired hard cell to justify sacrificing an easy correct cell
during weighted refinement, while final selection uses exact ordinary
matches. Test as a replacement scheme to avoid increasing sweep cost.
During the exclusive stress window only code and lightweight tests run.

The alternate boundary mask should use relative legal-placement coverage:
weight2 where the number of covering regions is below the maximum for the
board. Unlike an absolute D-1 edge band, this remains nonuniform on N4 D3
boards; N3 D3 correctly has uniform coverage and skips this scheme.

Prepared forward_weighted_refine_adaptive.py with these two schemes,
retaining the original weighted engine byte-for-byte. Three small canonical
parent-floor checks pass (N4 D3 K18, N6 D2 K8, N7 D3 K12). No benchmark
was launched during the exclusive stress window.

Prepared forward_weighted_refine_sa.py by appending the original measured
boundary/rare schemes and exact weighted engine to frozen
anneal_guided_walk_sa_short.py. Its wrapper retains the complete SA answer
as the true-score floor. It is unmeasured pending root's stress release.

Stress window released after SA-short passed36/36, maximum4.526s.
Weighted-on-SA smoke: 17846689, +1600 versus SA-short, all20 valid,
maximum4.250s, total process time23.360s. Parent floor holds by construction;
the measured file is frozen. Prepared forward_weighted_refine_sa_adaptive.py
to compare unresolved-cell plus relative-boundary weighting at the same
six-sweep budget. Any promising stable candidate needs the pending verified
kernel speedup because the parent's isolated time margin is only0.47s.

Adaptive-on-SA smoke failed its time gate: 19/20 valid, one5.011s timeout.
No score-improvement claim is possible. Holding heavy runs for the exact
State.apply speed port, whose smoke is byte-identical to parent and whose
full stable parity is pending. Original weighted-on-SA's +1600 comes from
N25 D3 C3 K160 case015, a single additional correct cell.

## Hypothesis 13: aggregate weighted regional deltas before updating counts

Like the pending ordinary State.apply speedup, weighted-state application
can accumulate match deltas by overlapping region and update each region's
count/bitplanes once, including cancellation to zero. This removes a full
counts-list copy and repeated overlapping writes per operation. Verify the
new engine against the prior exact implementation over interleaved actual
and wished-color/weight swaps before any benchmark. This changes speed
only; selected actions and output paths must remain exact.

Created separate forward_weighted_refine_sa_fast.py and
forward_weighted_refine_sa_adaptive_fast.py. These incorporate the isolated
ordinary State.apply port plus weighted count aggregation. All fields and
best/tie choices match the previous weighted engine over600 randomized
interleaved swaps; the525 exhaustive weighted-action comparisons and30
weighted-sequence objective checks also pass. No timing claim yet.

Readiness confirmed ordinary State.apply exact parity on all320 stable
scores and output hashes. Fast static weighting smoke preserves all20
slow weighted output hashes, score17846689, max4.120s. Fast adaptive
weighting also scores17846689, all20 valid, max3.726s, total19.615s.
These timings had differing contention. Proceed with the adaptive variant's
stable suite because its stronger unresolved-cell hypothesis was previously
blocked by runtime rather than a score result.

Adaptive-fast weighted stable: 250616902, +57680 versus best020,
all320 valid, maximum3.881s, total process time274.868s. The newer
best021 (beam/perturbation plus SA) already scores250867386, so this older
parent variant is superseded and will not be submitted. A prepared
forward_weighted_refine_merged.py appends the tested adaptive weighted
wrapper to best021 and ports the exact State.apply change; it compiles.
Readiness reports further State/RefineState geometry speed ports pending,
which may provide a better parent for this small marginal improvement.

Cost ablation hypothesis: the weighted objective may produce its useful
escape within one following ordinary sweep, making the second ordinary
sweep redundant. Inspect both fixed weight schemes at zero/one/two
ordinary sweeps on the ten improved cases as an exploratory cost diagnostic,
not a new benchmark result or a replacement for the frozen suite. Keep
all final solver decisions general; no case-specific behavior is permitted.

The ablation shows the second cleanup sweep is needed by several gains,
including the largest N9 improvement. Boundary weighting provides8 of10
gains; unresolved weighting uniquely helps N18 (+2cells) and N13 (+1cell).
Retain both schemes and both cleanup sweeps in the next composition.

Root verified cached_best021.py has exact all320 output-hash parity and
introduced best022 at250872488. Created forward_weighted_refine_022.py
from immutable022, copied verified State and RefineState classes plus
_REFINE_GEOMETRY from cached021, then appended the tested adaptive weighted
engine and parent-floor wrapper. Three random composed-parent outputs are
identical to022, and canonical final scores preserve the parent floor.
Smoke started with one worker before any stable or readiness evaluation.

Smoke022: 17846689 (+1600 versus parent), all20 valid, maximum3.734s.
Fixed320 stable evaluation started; this file remains frozen.

## Hypothesis 14: stronger unresolved-target pressure

After annealing, a remaining improvement may require temporarily sacrificing
more than one correct cell to repair a hard mismatch. Generalize exact
weighted suffix scoring from weights0..2 to weights0..4, then use weight4
on unresolved targets and weight1 elsewhere. Retain ordinary weight2
boundary perturbation, two cleanup sweeps, and the exact parent-score floor.
The evaluator needs seven score bitplanes (maximum12*D*D=108) and binary
weight contributions; it must pass exhaustive canonical tests with all
weights1..4 before any benchmark. Prepare separately while022 evaluates.

Prepared forward_weighted_refine_strong.py. Its exact weighted optimizer
passes300 exhaustive canonical action comparisons with weights1..4 and
interleaved actual/wish/weight swaps. This is an unmeasured prototype;
weighted022 remains the only running full-suite candidate.

Weighted022 stable: 250917307, +44819 versus best022, all320 valid,
maximum3.392s, total process time275.732s. Eight cases improve and none
regress. Improvement cases span N9..27 and reachable, striped, near-uniform,
adversarial, checkerboard, repeated-stamp, and random distributions.
Readiness38 started on the exact frozen measured source; root notified.

For the next stronger-weight trial, retain both measured weight2 schemes
and append the unresolved-weight4 scheme as a third independent candidate.
This preserves the newly measured weighted022 score floor. Added work is
one weighted plus two ordinary sweeps, skipped when the color upper bound
is already attained. Generalized scorer must reproduce weight2 paths.

Weighted022 readiness passed38/38, maximum3.309s, deterministic and
static checks clean. Before promotion it was superseded by pool best023
at250921331. Root is measuring a binary small-board hook, then the weighted
wrapper will be merged onto the highest verified parent. Heavy runs are
held meanwhile; all weighted022 results and source remain frozen.

The stronger floor-preserving prototype keeps original weight2 decisions
exactly over300 interleaved transitions and20 full two-sweep sequences.
Its generalized weights1..4 oracle still passes300 exhaustive comparisons.

Root saved exact binary-hook best024 while readiness prepares the higher
pool+binary composite. Prepared forward_weighted_refine_composite.py from
frozen pool_binary_composite.py, appending the unchanged tested weighted
wrapper. Three light canonical checks preserve parent outputs inside the
wrapper and preserve parent scores outside; a generated reachable N4 D3 C2
target stays perfect with exactly the same binary solution. New heavy runs
are held until the composite's full qualification and exclusive stress.

Readiness agent measured the frozen composite at250983831, all320 valid,
maximum3.169s, with exact output hashes matching the appropriate023/024
parent on every case. Its readiness and exclusive stress are pending;
the prepared weighted wrapper has not yet been benchmarked.

The composite was saved as best025, then an informed-SA candidate measured
higher. Root is stress-testing that candidate and will combine it with025
before another post-weighted full run. All own heavy work remains stopped.

## Hypothesis 15: reuse canonical geometry inside weighted refinement

Use the already verified RefineState geometry cache for weighted states,
represent action bits in canonical action order, and encode shuffled tie
rank in bitplanes as ordinary RefineState does. This avoids rebuilding
positions for each weighted sweep. Actual colors, wishes, weights, counts,
and selected actions must remain exact. Verify randomized state/choice and
complete weighted-sequence parity before using the cached component.

Prepared forward_weighted_refine_cached.py, using the shared immutable
geometry and bit-sliced tie rank. All375 interleaved choices and25 full
two-sweep sequences match the previous weighted engine exactly.

Informed SA passed36/36 stress, maximum3.136s, and root saved best026.
Heavy runs released. Created forward_weighted_refine_informed.py by taking
the complete frozen pool_binary_informed.py parent and appending the cached
weighted component with its parent-score floor. Smoke begins while the
parent is independently measuring; both sources remain frozen.

Cached weighted-on-informed smoke passes20/20 at17942045, +7904 over
the frozen informed composite. Maximum3.269s, total19.740s. Gains are on
N15 D3 C5 K100 (+4444) and N17 D2 C3 K90 (+3460), no regressions.
Fixed320 stable started with one worker.

Prepared forward_weighted_refine_informed_strong.py with cached geometry,
weights0..4, and a third weight4 unresolved-target candidate after the two
measured weight2 candidates. It preserves the weight2 floor by retaining
those paths. Its cached engine matches the uncached strong reference over
300 interleaved transitions and20 full weighted two-sweep sequences; the
maximum two-sided gain72 for D3 passes its seven-bit accumulator test.
No benchmark yet for this stronger variant.

Cached weighted informed stable: 251305191, +24512 versus the measured
pool_binary_informed parent251280679, all320 valid, maximum3.237s,
total process time264.038s. Eight cases improve, none regress. Improvements
span N15..28 across checkerboard, stripes, reachable, repeated-stamp, and
local-adversarial families. Readiness38 started on the frozen source;
root has the exact candidate/report paths and score comparison.

Weighted informed readiness passed38/38, maximum3.202s, deterministic and
static checks clean. Root will promote its parent, then stress this exact
candidate in isolation before checkpointing. No heavy own jobs remain.

Weight4 review: the prototype retains both existing weight2 candidates in
the same order before trying the stronger candidate. Its generalized scorer
preserves all weight2 decisions, so the measured parent floor is retained.
Extra work is one weighted and two ordinary sweeps, only when the earlier
answers have not reached the available-color bound.

Boundary pressure alternative: most earlier gains came from boundary
weighting, so a separate candidate will replace only the third scheme with
boundary weight4/interior1. This has the same three extra sweeps as strong
unresolved weighting. Both preserve the measured weight2 paths and remain
unmeasured until the exclusive timing window closes.

Root saved weighted informed as best028_251305191.py after36/36 isolated
stress, maximum3.325s, p953.279s, mean1.729s. Resume exactly one bounded
experiment: boundary weight4, starting from best028's final sequence.
Choose boundary pressure because it supplied most previous gains. Keep the
parent code intact, append a separately named strong weighted evaluator,
perform one weighted and two ordinary sweeps, and retain the exact parent
answer unless actual matches improve. This adds three sweeps and skips
uniform coverage or an already attained available-color bound.

Boundary4-on028 smoke ties the parent at17942045, all20 valid,
maximum3.497s, total20.287s. No full stable run is justified yet. Use the
fixed100-case development suite as a gate for this same frozen experiment;
if it also ties, stop the variant. Parent floor is explicit, and the added
stage never replaces an equally scoring parent answer.

Boundary4 development gate: 80208624, exactly tied with best028 on the
same100 cases; all100 valid and every output hash identical to the parent.
Maximum4.073s, total85.153s under current load. No full320 or readiness run
is warranted because the extra work produced no measured gain. Stop this
single bounded variant and retain the weight2 checkpoint. All experiment
sources and smoke/development reports remain frozen.

## Hypothesis 16: alternate exact forward and backward coordinate refinement

Start from complete best028. Existing coordinate sweeps run right-to-left.
For a forward sweep, start actual colors at the initial state and pull the
final target wishes backward through the old sequence. At each position,
undo its old action from wishes, select the exact RefineState.best action,
then apply that chosen action to the actual prefix. Every replacement
optimizes the exact final objective conditioned on the current prefix and
unchanged suffix. Forward tie choices may escape backward plateaus.

Verify per-step gains/choices against exhaustive canonical swap scoring,
compare intermediate prefix/suffix states with direct permutations, and
verify complete sweeps never lower true final matches. The first bounded
candidate uses two forward/backward rounds (four total sweeps), retains
the complete best028 answer as its true-score floor, and stops at the
available-color upper bound. Run one benchmark worker.

Prepared forward_coordinate.py on best028. Exhaustive canonical checks
pass on20 random sequences: every chosen action, exact gain, prefix actual
state, and inverse-suffix wish state agrees at every coordinate. Another35
random cases preserve true final matches and K over two full forward passes.
No smoke benchmark has started: root is qualifying a higher triple-layer
candidate and requested an exclusive timing hold. Only light work continues.

Two light complete-wrapper checks preserve the parent score (N5 D2 K6,
N7 D3 K10). Generator supplied frozen anneal_weighted_triple.py, measured
251481350 with26 wins/no losses and readiness20/20. Prepared
forward_coordinate_triple.py by appending the unchanged tested forward
helpers and alternating wrapper to that complete triple parent. It compiles;
no benchmark starts before root releases the exclusive timing window.

Triple parent saved as best030_251481350.py after36 maximum-size stress
cases passed, maximum3.953s, p953.808s, mean1.955s. Root released timing;
the forward/backward wrapper starts smoke with one worker. Preserve the
full triple parent and assess added cost against the roughly1s margin.

Forward initialization speed hypothesis: build the inverse-suffix wish
vector using scalar canonical-equivalent swaps, initialize RefineState from
its grid wishes, then assign its stamp wishes. No cached field depends on
stamp wishes, so this avoids L expensive wish-bitset updates while keeping
the exact same state before the first coordinate. Verify full sweep/sequence
parity before measuring this separate speed variant.

Initial forward/triple smoke ties030 at17962810, all20 valid,
maximum4.608s, total25.999s under concurrent load. Prepared
forward_coordinate_triple_fast.py with scalar suffix initialization;
35 randomized raw sweeps and35 complete two-pass sequences exactly match
the slower implementation. Existing per-step exhaustive canonical tests
and35 monotonicity/budget tests still pass. Measure fast smoke, then use
development100 as the evidence gate; no full stable run without a gain.

Fast smoke has exact output-hash parity with the slower version, all20
valid, score17962810, maximum4.143s. Development100 is positive:
80286651, +6618 versus parent030's80280033, all100 valid,
maximum4.211s, total94.490s. Three single-cell gains occur on N30 D2 C4
K155, N16 D2 C2 K66, and N25 D2 C3 K117; no regressions. These larger
boards are separate from root's tiny-domain exact finisher. Proceed with
the fixed320 suite on frozen forward_coordinate_triple_fast.py.

Forward/triple stable: 251490939, +9589 versus030, all320 valid,
maximum3.948s, total317.417s. Five single-cell gains and no regressions:
the three development wins plus N25 D2 C6 K144 and N27 D3 C3 K93.
Thus four gains are D2, one D3. The standalone parent was superseded by
the tiny-board finisher; root requested preserving that independent gain.

Prepared forward_coordinate_suffix.py on frozen wildcard_suffix_fast.py,
which incorporates constructor undo and a further exact small-board suffix
repair. The RefineState class is bytecode-structure-identical to the tested
forward parent, and the tested forward helpers/wrapper are unchanged.
Expected additive total is251678439 if the new parent's measurement
confirms251668850. Smoke starts before any full qualification of this child.

Merged suffix smoke passes20/20, total17962810, maximum4.215s,
total26.559s. Parent full stable is now confirmed251668850, with only
case180 output changed from031. The merged full320 run is underway.
Retargeted exhaustive forward-coordinate and monotonicity/budget checks
to forward_coordinate_suffix.py; all21 forward test groups pass in5.257s.

Merged suffix stable confirms251678439, +9589 versus frozen parent
251668850, all320 valid, maximum3.620s, total297.170s. Exactly the
original five single-cell gains remain (079/090/095/271/283), zero losses.
The complete parent AST is unchanged except its final solve rename.
Readiness38 is now running before checkpoint recommendation.

Readiness passes38/38, maximum3.464s, including repeated-output
determinism and isolated execution/source checks. The separate21-test
forward suite supplies canonical differential evidence. Parent notified
of frozen candidate251678439 and all heavy jobs clear for exclusive stress.

## Hypothesis 17: prune modern sequences before bounded cleanup

The complete late_beam_forward parent may contain neutral or harmful
operations after annealing, triples, and alternating coordinate changes.
Use the previously tested exact right-to-left contribution pruning: delete
each operation when its removal preserves or improves final matches with
the already-pruned suffix. Only when the sequence shortens, run two ordinary
backward sweeps (seed offset6173), then compare the true final score with
the untouched complete parent. Skip parents already at the available-color
bound. Cost is O(K D^2) for pruning plus two sweeps only on shortened paths.
Retarget pruning tests and add exact deletion-oracle and wrapper-floor
checks. Smoke then development100 gates the full320 qualification.

Prepared frozen forward_prune_late.py with the entire late_beam_forward
parent, original exact prune_sequence, two backward cleanup sweeps only
when shortened, and strict true-score parent floor. Four test groups pass:
150 canonical subsequence floors,75 exact removal-oracle paths,30 full
wrapper/input/budget checks, and30 deliberately bad cleanup floor checks.
Smoke begins with one worker.

Prune smoke ties17962810, all20 valid, maximum4.592s, total27.545s.
Development100 ties80286651, all100 valid, maximum4.344s, total103.058s.
Every development output hash matches the complete late_beam_forward
parent exactly (parent stable251734381). Thus the bounded prune plus two
backward sweeps has no measured gain; stop without full320 or readiness.
Keep the measured parent and all frozen experiment files/reports.

## Hypothesis 18: weighted refinement of isolated remaining errors

Preserve immutable best034_251734381.py. Give weight2 only to cells
that are wrong after the full parent and have at most one wrong cardinal
neighbor; use weight1 elsewhere. Isolated errors may need coordination
that broad unresolved/boundary weights miss. Skip constant masks and
parents at the inventory bound. One qualified weighted_refine sweep plus
two ordinary cleanup sweeps is the complete additional budget; retain the
parent unless true unweighted final matches improve. Check the isolated
mask at boundaries, weighted action/objective correctness, and wrapper
floors before smoke/development gates.

Prepared frozen forward_isolated_034.py. Four canonical test groups pass:
135 mask-oracle cases,420 exhaustive weighted action/state comparisons,
50 weighted-sweep objective/budget checks, and40 wrapper floor/input checks.
The existing qualified weighted engine is copied unchanged. Smoke begins
with one worker.

Isolated-weight smoke ties17962810, all20 valid, maximum4.245s,
total24.050s. Development100 ties80286651, all100 valid, maximum3.885s,
total88.921s. Every development score and output hash exactly matches
immutable034. No measured value from the extra weighted/cleanup sweeps;
stop this bounded variant without full320/readiness. Retain all frozen
source, tests, and reports.

## Hypothesis 19: bounded late packed beam on N10..12

Preserve frozen late_beam_four_fast.py and extend only N10..12,D3.
Use a separately named helper with two-byte little-endian action paths,
six depth layers, width=min(256,50000//action_count), and at most two
strictly improving appended repairs. Require spare budget, at most N
remaining wrong cells, and score below the inventory bound. This caps
each full layer near50000 generated transitions; test the larger domain
and action IDs over255 canonically. No benchmark-specific decisions.

Frozen eligibility inspection finds4 qualifying cases out of17 in the
new N/D domain:029,049,089 in development and185 only in stable. None
is in smoke. Case049 has K1, making this a cheap single-step check. The
034 result rows are exact for this domain because four-fast changes only
N5..9. Detailed configurations are recorded in the eligibility report.

Prepared frozen forward_wide_beam_four.py. Four tests pass:1960
canonical packed transitions across allN10..12 placements/rotations at
C2/C6, explicit successful paths with IDs over255 onN11/N12, nine
wrapper budget/input/floor cases, and rejection of a harmful proposed
repair. Parent is copied in full; each accepted tail is verified by exact
simulation before retention. Smoke starts with one worker.

Wide-beam smoke ties17962810, all20 valid, maximum3.445s, total21.176s.
Development100 ties80286651, all100 valid, maximum3.193s, total83.815s.
All development output hashes match the complete four-fast parent exactly.
The sole eligible stable-only case185 was checked separately:966942,
117/121 matches, exactly the parent output hash, runtime2.157s. Thus every
eligible frozen case was measured and none improves. Reject the bounded
wide-beam extension without a full320 or readiness run.

## Hypothesis 20: late packed D2 overlap/rotation routing

The retained late beam covers onlyD3. Inspecting the full four-fast parent
shows13 N<=12,D2 cases below their inventory bound, but only3 have spare
operations. Excluding exactK<=2 leaves two eligible shapes: N5 with2 wrong
cells and3 spare operations, and N10 with4 wrong cells and9 spare. A late
D2 beam can search overlap/rotation routes through temporarily damaged
grid states that the retained D3 beam never visits. The solver condition
remains general and uses no case identity.

Prepare packed2_transitions with canonical 2x2 clockwise rotations and
two-byte action paths. For N<=12,D2,K>2, spare budget, at most N errors,
and score below inventory bound, run at most two strict repairs, each
depth<=6 and width=min(384,60000//action_count). Verify each proposed tail
with the exact transition and true score before accepting. Preserve the
full frozen late_beam_four_fast parent. During root exclusive timing,
only implementation/light canonical tests; no solver-heavy runs.

Prepared frozen forward_d2_beam_four.py and passed four light test
groups:2168 canonical packed transitions acrossN3/5/8/10/12,C2/C6;
80 sequential packed/full-state comparisons; high-ID improving paths;
wrapper K/input/floor checks and rejection of harmful tails. After root
released timing, measured both eligible frozen cases directly. Case057
remains96/100 (960000),1.303s; case148 remains23/25 (920000),0.595s.
Both output hashes exactly match the full parent. Since every eligible
case was directly measured with no gain, stop before smoke/development
or full320; no broader qualification is justified for this candidate.

## Hypothesis 21: four-operation windows with optimized middle pairs

Start from immutable035. A FourWindowWalker maintains actual prefix and
inverse suffix wishes around four operations. Diversify one outer endpoint
(or occasionally both) with local, mismatch-centered, identity, or random
placements. With endpoints fixed, use existing exact optimize_pair for the
middle pair with both existing middle actions, two identity choices, and
one random fixed-side choice. This jointly replaces four operations and
can route colors beyond the existing triple neighborhoods.

Use min(1800,max(120,180000//N^2)) proposals, giving200 atN30. Walk
neighboring window positions to avoid rebuilding state; accept nonnegative
moves, keep the best score, then one ordinary cleanup sweep if the path
changed. Pad at most eight spare slots, respectK, and compare true final
score against the complete parent. Canonically verify window boundary
states, exact deltas, nested restoration, floor andK before smoke/dev.

Prepared frozen forward_four_window_035.py. Three canonical test groups
pass:420 randomized window moves/proposals with complete prefix/suffix,
delta and nested-restoration checks;25 exhaustive allowed-middle-pair
optimizers;15 search and complete-wrapper score/K/input checks. Smoke
starts with one worker. The complete035 parent is preserved.

Four-window smoke ties17962810, all20 valid, maximum4.009s,
total26.660s. Development100 ties80286651, all100 valid, maximum4.136s,
total107.487s. Every development output hash exactly matches035. The
nondecreasing four-window neighborhood did not yield a retained improvement;
reject this bounded version without full320/readiness. A possible future
distinct continuation is temporary negative four-window acceptance, but
that is not included or measured in this frozen candidate.

## Hypothesis 22: annealed four-window routing

The nondecreasing four-window search may reject coordinated routes that
need a temporary loss. Preserve its frozen source and create a separate
035 variant with the same proposal budget and choices, but accept negative
deltas with exp(delta/temperature), cooling quadratically from0.8 to0.04.
Track the highest true score visited independently and clean only that
retained sequence; the complete parent comparison remains after cleanup.
Reuse canonical boundary/delta/restoration/pair/floor tests and explicitly
check that exploration actually accepts losses while returning its best
score floor. Smoke/development gate further measurement.

Frozen forward_four_window_anneal035.py differs only in negative-delta
acceptance and the local math import. Four test groups pass, reusing all
canonical window/pair/floor checks. Ten instrumented randomized searches
confirm temporary losses are accepted and each returned sequence attains
the highest visited true score. Smoke begins with one worker.

Annealed four-window smoke improves to17967254 (+4444), all20 valid,
maximum3.354s, total22.581s. One cell is gained on N15,D3,K100.
Development100 confirms80291095 (+4444), all100 valid, maximum3.533s,
total90.508s; no additional development gains or losses. Proceed with
the fixed320 full suite on this unchanged source.

Annealed four-window full stable confirms251778027 (+12396 versus035),
all320 valid, maximum3.277s, total331.315s. Four single-cell gains, zero
losses:005 N15D3K100 +4444;213 N14D3K6 +5102;219 N26D3K49 +1479;
287 N27D3K112 +1371. Entire035 parent AST is unchanged except final
solve rename. Readiness38 is running before checkpoint recommendation.

Readiness passes38/38, maximum3.296s, repeated-output determinism
passes. Four canonical test groups supply separate transition/window
differential evidence. Parent notified of frozen251778027 candidate; all
heavy jobs clear for any exclusive maximum-size timing check.

## Composition: hot search, commutator, annealed four windows, deeper beam

Preserve frozen anneal_hot_commutator_fast.py in full. Rename its final
solve to solve_four_parent; append the qualified FourWindowWalker and
annealed repair_four_windows stage, renaming its solve to
solve_without_deeper_beam; append the unmodified qualified root
late_beam_deeper_fragment.py. Budgets and strict true-score floors remain
unchanged at each added stage. The speed parent uses counts=None, so
retarget the entire four-window canonical suite and explicitly verify
nested proposals preserve that representation. Audit all parent/helper
ASTs. Preparation/light tests only until the frozen combined parent and
deeper readiness finish qualification.

Prepared frozen forward_all_repairs.py. All parent functions/classes
(including main), all three four-window nodes, and both deeper nodes are
AST-identical to their qualified sources except the required solve names.
Six canonical groups pass, including the complete four-window suite,
explicit counts=None nested restoration, and deeper-stage harmful-tail
rejection. Root deeper readiness38 has passed(max3.100s), checkpoint038
251809034 saved. Await combined-parent full qualification before heavy runs.

Combined parent qualified251807645 and deeper parent251809034; root
released heavy runs. All-repairs smoke17967254, all20 valid, maximum3.201s,
+4444 versus combined parent. Development80325470, all100 valid,
maximum3.246s,total89.372s; +32222 versus combined parent from005(+4444)
and056(+27778). Every development score equals the per-case maximum of
qualified combined/four/deeper parents. Full320 now running; expected
union251862073 remains a hypothesis until measured.

All-repairs full320 confirms251862073, exactly the expected per-case
maximum of all qualified components. All320 valid, maximum3.945s,
total304.199s. No interaction losses. Gain versus best038 is53039; gain
versus hot/commutator parent is54428 across005(+4444),056(+27778),
213(+5102),219(+1479),317(+15625). Readiness38 now runs before root
exclusive maximum-size timing; source remains frozen.

All-repairs readiness passes38/38, maximum2.938s, repeated-output
determinism passes. Six canonical groups cover duplicated four-window
state/delta/restoration logic and deeper-stage floor; AST composition
audit is saved. Root and readiness agent notified. All heavy jobs clear
for isolated maximum-size timing before checkpoint promotion.

## Hypothesis 23: annealed five-operation windows

Preserve immutable039. Generalize the exact boundary walker to windows
of five operations. Diversify an outer endpoint, then optimize the three
central actions using the qualified optimize_triple helper with2x2 fixed
central endpoint candidates (each existing endpoint plus one diversified
choice). Four exact best-action calls examine this constrained triple;
the old central triple remains a fallback. This coordinates five actions
without enumerating all paths.

Use min(1200,max(120,135000//N^2)) proposals (150atN30), neighboring
window traversal, annealing0.8to0.04, best-score retention, at most eight
padded spare slots, and one ordinary cleanup pass. Compare the final true
score with the complete039 parent. Canonical boundary/delta/restoration,
counts=None, constrained triple optimum, annealing retention, budget and
wrapper-floor checks precede smoke/dev; qualify full only on new gain.

Frozen forward_five_window_039.py passes four canonical groups:
420 randomized window boundary/delta/nested-restoration cases with
counts=None;25 constrained exhaustive central-triple optimizers;10
instrumented annealing best-retention searches with accepted losses;
15 complete wrapper input/K/score-floor cases. Smoke starts one worker.

Five-window smoke ties17967254, all20 valid, maximum3.795s,
total27.297s. Development100 ties80325470, all100 valid, maximum4.198s,
total103.215s. Every development output hash exactly matches039. No
new complementary gains justify the additional stage; reject this bounded
variant without full320/readiness. All source/test/report evidence retained.
