# Stronger sequence neighborhoods

Starting checkpoint: best010, stable246874186, smoke17764025.
Benchmark inputs remain the frozen seed20260925 suites.

## Hypothesis1: cached exact mutation annealing

Single-operation coordinate descent accepts only nondecreasing final score.
Allowing small temporary losses may move between otherwise disconnected local
optima. Cache prefix grid+stamp colors and backward target wishes, making a
single or adjacent-pair replacement delta exact in the number of touched cells.
Refresh only the affected prefixes/suffixes after accepted moves. Deterministic
temperature cycles reset to the best sequence, which is always retained.

Neighborhoods: arbitrary replacement, local coordinate/rotation movement,
adjacent operation exchange, and canceling operation pairs. Preserve the full
best010 constructor/refinement first; initially spend2000-7000 extra bounded
proposals, scaled by board area, and measure the runtime overhead.

Before measuring, compare randomized mutation deltas and post-accept cached
states against full canonical simulation. Benchmark smoke first, then stable
only for a promising valid candidate within the5second hard limit.

Outcome1: anneal_cached.py smoke17764025, equal tobest010 with no improved
case. All20valid, totalprocess19.023s, max3.731s underjobs2. The extra search
cost did not earn a score gain; no stable evaluation performed. Differential
tests cover1200random accepted single/pair mutations and independent best-score
retention/determinism checks.

## Hypothesis2: exact completion of sampled adjacent pairs

Random pair changes are too unlikely to produce useful stamp contents. Instead,
sample one operation and choose the other operation by exhaustive exact
backward-target optimization. Alternate fixing the first and second operation.
Use only nondecreasing pair changes, retain legal operation count, and bound
proposal count by board area. This explores a neighborhood that individual
coordinate descent cannot cross while avoiding annealing's unrepaired damage.

Outcome2: anneal_pair.py smoke17772289 (+8264), all20valid, totalprocess20.653s,
max4.000s underjobs2. Gains are small but positive; the exact pair-completion
neighborhood is retained for broader testing.

## Hypothesis3: spend bitset-refinement savings on stronger pairs

The root supplied refine_bits_fragment.py, an exactly equivalent bitset version
of the expensive backward coordinate sweeps. Inline that verified replacement
to free runtime, triple the pair proposal budget to1000atN30 (capped2400), and
perform two additional cheap coordinate sweeps after the pair changes. Every
phase preserves final score. Snapshot: anneal_pair_bits.py.

Smoke3:17776733 (+12708 overbest010), all20valid, totalprocess21.804s,
max3.176s. Readiness20/20 passed, max3.443s with concurrent stable benchmark.

Stable3:248753972 (+1879786 overbest010), average777356.1625, all320valid,
totalprocess266.471s, maximum3.942s, wall134.268s. Improvement occurs mostly
outside the smoke subset. Root notified immediately of the readiness-qualified
candidate for checkpoint promotion.

## Hypothesis4: incremental exact pair sweeps

The scalar exact-completion scan rebuilds gain tables for each pair proposal.
Use RefineState incrementally while sweeping backward in pairs: undo the old
pair, tentatively apply one sampled operation, choose the exact best companion
with bitsets, undo the tentative operation, and select the strongest pair.
Keep the original pair among candidates to guarantee monotonic score, then
pull target wishes backward through the chosen pair. Alternate pairing offset
between sweeps and end with two ordinary repair sweeps. Initial budget:
two pair sweeps,16 sampled fixed operations per pair.

Smoke4: anneal_pair_sweep.py17777844 (+13819 overbest010), all20valid,
totalprocess11.823s, max2.218s. The incremental version improves both smoke score
and runtime versus sampled scalar completion. Broaden to four pair sweeps and
32candidate samples: anneal_pair_wide.py smoke17791128 (+27103), all20valid,
totalprocess19.379s, max3.666s. Full stable and readiness measurements running.

Stable4wide:248424233, all320valid, totalprocess157.334s, max3.381s;
readiness20/20 passed, max2.678s. This is329739 below scalar pairbits despite
being faster. Scalar pairbits wins smallN3..9 by432846; wide wins N10..30
by103107. Thus incremental sweeps have too few proposals for short sequences.

## Hypothesis5: increase depth or combine complementary pair neighborhoods

Eight16-wide sweeps at similar proposal count improve smoke17795622,
all20valid, max4.168s, but were not yet taken to stable because another combined
variant is more promising. Combining four32-wide sweeps with scalar completion
at half the large-board budget (500proposals atN30,2400cap forsmallboards), then
two coordinate repairs, gives anneal_pair_hybrid.py smoke17801617, all20valid,
max4.301s. Full stable evaluation running.

A naive alternative normalizing sweep count by initial sequence length
(max64sweeps,512/length) timed out on one smoke case: anneal_pair_adaptive.py
score16857088,1/20invalid,max5.014s. Rejected; short sequences can still occur
on large boards, so adapting only to sequence length does not control runtime.
Any follow-up adaptive variant must also bound board-area times operation-budget
times sweep-count, and preserve the established four-sweep upper workload on
the largest instances.

Area-bounded follow-up anneal_pair_budgeted.py smoke17791128, all20valid,
maximum3.537s with jobs1. Score ties the four-sweep version; expected benefit is
limited to short small-board sequences outside smoke, so deferred pending a
more direct budget normalization.

## Hypothesis6: normalize candidates rather than expensive sweep setup

For short sequences, increase sampled candidates per pair to about1000total
per sweep, keeping the established32minimum. If the sample budget covers all
legal first operations, enumerate each first move and find its optimal second
move exactly. In particular K=2 can be solved globally by one such complete
pair search, after which additional sweeps are unnecessary. This removes the
short-sequence sampling gap without repeatedly rebuilding large bitset states.

Hybrid stable:249115734 (+361762 overbest013), all320valid, totalprocess230.553s,
max4.214s. Readiness running before promotion. Source is frozen.

Exhaustive-short variant smoke17791128, all20valid, max3.457s. This ties wide
on smoke; its intended short-sequence improvements need development/stable
evaluation because the smoke subset lacks K=2 cases. Independent brute-force
tests verify K=2 global optimality on10random small instances.

## Hypothesis7: direct exact low-budget solve

For K<=2, bypass all construction restarts and refinement. Enumerate every first
operation (including no-op), then ask the bitset evaluator for the best second
operation. This is globally optimal in the two-operation space and avoids the
cost and incompleteness of sampled construction. K=1 is a direct exact best
move. Add this branch to the measured hybrid while preserving its behavior for
larger budgets.

Outcome7: direct-low-budget anneal_pair_exact.py smoke17801617, all20valid,
max3.881s. A targeted canonical evaluator probe of all32stablecases withK<=2
found zero score delta versus hybrid, allvalid. No full stable rerun; the root
assigned further exact/short-budget search to the simulator agent, so this
research branch stops here to avoid duplicate work.

Hybrid readiness passed20/20, max3.042s; root promoted it as best014249115734.

## Hypothesis8: jointly change three consecutive operations

Two-operation local optima can require three simultaneous changes. For a
selected triple, tentatively apply a candidate first operation to prefix colors
and a candidate last operation backward to target wishes. The bitset evaluator
then gives the globally best middle operation exactly. Retain the original
triple and evaluate a4x4grid of fixed ends. Two backward sweeps with different
block offsets plus two coordinate sweeps form the initial bounded experiment.
Candidate ends include old operations, no-op, the immediate exact best move,
and a random/local/target-mismatch-oriented placement. Append this neighborhood
to the measured hybrid, retaining its score floor. This is separate from the
root's forward macro constructor and other agent's search-pool selection.

Triple smoke:17824708 (+23091 overhybrid), all20valid, max4.198s. Canonical
tests exhaust every possible middle operation for the sampled end pairs and
verify the chosen triple's exact score and full bitset-state restoration.

## Hypothesis9: condition candidate first moves on candidate final moves

For each sampled last operation, pull wishes backward through that operation
and ask the exact evaluator for a promising first operation. Add those moves
to the candidate first-move pool before the existing joint triple optimization.
This spends a small number of cheap bitset queries on informed candidates and
reduces reliance on independently random endpoint choices. The existing exact
triple objective and score-preservation logic are unchanged.

Triple stable:249339886 (+224152 overbest014), all320valid, totalprocess249.389s,
max4.137s; readiness20/20 passed, max3.364s. Before promotion, the independent
small-budget beam solver reached249389357 and was saved asbest015. The triple
neighborhood should be complementary, so prepare merged candidates onbest015.

Guided triple smoke:17829153 (+27536 overbest014), all20valid,max4.334s.
Both source snapshots are frozen. Heavy benchmarks paused for the root's
exclusive maximum-size runtime holdout. Prepared anneal_beam_triple.py and
anneal_beam_guided.py, which refine the sequence selected bybest015 and retain
its exactK<=2 return path. Only lightweight correctness checks run during the
exclusive timing window.

## Hypothesis10: move incrementally between overlapping pair positions

The expensive scalar completion phase rebuilds tables for independent random
sequence positions. Maintain one RefineState for prefix position i and suffix
wishes at i+2, and move to neighboring pair positions by applying the intervening
sequence operations to its values and wishes. Accepted changes affect only the
two omitted operations, so these cached boundary states remain valid without
rebuilding. A bounded walk over overlapping pair positions can evaluate many
exact companions cheaply. Canonical tests will validate arbitrary position
jumps, proposal deltas, accepted edits, and both boundary states before any
benchmark. This experiment remains separate from construction/macro search.

Prepared PairWalker in anneal_pair_walk.py;450random position-jump and mutation
checks pass against canonical prefix/suffix states and full final-grid scores.
Prepared beam+triple merges also pass their parent-score-floor test. During the
exclusive holdout window, root saved best016249547073 (beam up toK24). Rebased
all three still-unbenchmarked candidates (anneal_beam_triple, anneal_beam_guided,
anneal_pair_walk) onto this immutable checkpoint. No heavy runs started while
the root's timing window remains active.

Exclusive holdout completed and heavy runs released, with one worker preferred.
Rebased guided-triple smoke17829153 (+27536overbest016), all20valid,
max3.815s,totalprocess21.708s withjobs1. PairWalker smoke17826315 (+24698),
all20valid,max3.567s,totalprocess23.509s withjobs1. Guided merge has the higher
smoke score, so its full stable evaluation runs first; the online pair candidate
remains frozen for subsequent evaluation. No checkpoint claims are made from
smoke scores alone.

## Hypothesis11: anneal exact completed pairs with inexpensive state movement

Revisit temporary score losses using the fast PairWalker instead of arbitrary
raw-operation mutation. Each proposal already optimizes the companion move,
so a small accepted loss is more likely to create a useful color route. Four
deterministic cooling cycles reset to the best retained sequence. Accept neutral
changes and save their equally scoring states for diversity. Initially double
the large-board proposal budget to2000 atN30, cap6000, and retain the best016
floor plus a final exact coordinate repair. Unit tests must verify best-score
retention and deterministic output before benchmarking.

Guided-triple merge onbest016 stable249880999 (+333926), all320valid,
average780878.121875, totalprocess236.596s, max3.958s withjobs1. Readiness
running before promotion. Root's bound_hybrid.py is independently score-equal
to best016 onall320cases and readiness38/38passed. Prepared separate bound
variants for guided triples, pair walking, and pair-walk annealing; the frozen
guided-triple source used by the completed benchmark remains unchanged.

Guided merge readiness20/20 passed, max3.700s. Root notified of the complete
qualified candidate immediately. For the next experiment, apply pair-walk
annealing after the guided triple refinement on the bound-optimized constructor,
then coordinate-repair the retained best sequence. This preserves the new
249880999 score floor by construction. Snapshot: anneal_guided_walk_sa.py.

Root promoted guided merge asbest017249880999. Combined-SA smoke17834708
(+5555overbest017), all20valid, but maximum4.968s onN30,D3,C6,K180 striped
target leaves insufficient margin. No stable evaluation for this budget.
Score gains are one cell on that large striped case (+1111) and one cell on
N15checkerboard (+4444). Reduce large-board proposal budget from2000to1000,
cap4000: anneal_guided_walk_sa_short.py. This preserves the best retained
sequence, but search trajectories differ, so remeasure rather than assuming
the same improvements. Root is independently adding iterated perturbation+
coordinate repair forN<=16; the frozen guided_bound source remains untouched.

Short-SA smoke17845089 (+15936overbest017), all20valid, max4.009s,
totalprocess21.404s withjobs1. Full stable evaluation running on this frozen
source; lower budget both improves this smoke result and restores timing margin.

## Hypothesis12: include exact immediate recommendations among fixed ends

The pair-walk proposals currently use random/global, local, and no-op fixed
operations. Spend one fifth of proposals on the exact best immediate operation
for the current omitted-pair boundary state, then still choose its companion
exactly. This adds a cheap informed candidate without raising proposal count
or changing the score-retention rule. Prepare a separate snapshot while the
short-SA full benchmark runs; do not alter the running source.

Short-SA stable250559222 (+678223 overbest017), all320valid,
average782997.56875, totalprocess261.491s,max4.683s withjobs1. Worst case007
is N30,D3,C6,K180 striped target; the same case took4.009s in smoke. Readiness
20/20passed,max3.799s. Promotion is explicitly deferred until exclusive36-case
maximum-size stress confirms runtime margin. All heavy jobs from this research
agent are now paused for the root-coordinated timing window.

Prepared, but not benchmarked, anneal_retained_small_sa.py by appending retained
best pair annealing to the root's frozen retained_small_beam.py. It keeps the
parent's exact low-budget handling and small-board deep beam, and adds an early
color-bound check before building PairWalker bitsets. This candidate must be
tested and measured after the exclusive window; it is not a submission choice.

## Hypothesis13: combine independent small-board and pair-annealing gains

The retained small-board parent preserves both the original sequence and the
iterated-refinement candidate before guided triples, and searches longer beam
prefixes on N<=6. Append the same fixed-budget pair annealing only after it has
selected its best result. This preserves its score case by case while testing
whether the two independent search directions have complementary gains.
The combined source is anneal_retained_small_sa.py. Added canonical parent-floor
checks across low K, the deep-beam branch, and larger boards, plus a check that
inventory-optimal sequences avoid constructing the annealing state. Execution
is pending release of the exclusive runtime measurement window.

The short-SA source passed the root's isolated36 maximum-size stress cases:
max4.526s, p954.133s, mean1.967s, all valid. Root saved best020250559222.
The combined retained-small source passed its two new canonical tests and
smoke20:17845089 (tiesbest020), all valid, max4.253s, totalprocess24.352s.
Its independent small-board gains occur outside smoke; full stable is running.

## Hypothesis14: walk overlapping triples with exact middle completion

Adjacent-pair annealing can change two consecutive operations. Extend the
cached boundary to three operations, mutate one endpoint while preserving the
other, and choose the middle operation exactly. This reaches separated changes
that pair descent cannot take directly. A fixed-budget cooling schedule permits
temporary losses while retaining the best sequence. Start as a separate layer
on the frozen short-SA source; canonical mutation-delta tests come first.
Its larger-state initialization and extra swaps must earn their runtime cost.

## Hypothesis15: delay small-board selection until after annealing

Annealing trajectories depend on their starting sequence. Selecting one of the
base, iterated, and deep-beam candidates before annealing can discard a sequence
that annealing would eventually improve more. On N<=16, anneal both retained
guided-triple branches and the eligible deep-beam candidate before choosing.
Larger boards keep the existing single-branch budget. This should preserve the
best020 score while retaining independent small-board gains, at a limited cost
on small instances. Prepare anneal_retained_dual_sa.py as a separate snapshot;
do not change the stable candidate currently running.

Combined retained-small stable:250867386 (+308164 overbest020), all320valid,
average783960.58125, totalprocess267.508s,max4.800s under shared load.
Ten cases improved and one regressed: case213 N14 K6 loses one cell because
the selected pre-annealing candidate changes. This supports testing the dual
variant; four independent canonical small-board comparisons already passed.
The combined candidate's readiness check is running before any promotion.

Combined retained-small readiness passed20/20,max3.874s. All147 N>16
stable outputs have identical hashes tobest020; larger-board search is the same
apart from the early bound check, so root accepted the prior maximum-size
holdout and saved best021250867386.

Dual-SA smoke had one timeout on case007 (5.031s), whose N30 search is unchanged.
This demonstrates thin shared-load timing margin rather than a small-board
regression. Do not promote that snapshot. Ported the root's separately verified
pool_sa_fast State.apply to anneal_retained_dual_sa_fast.py and
anneal_triple_walk_fast.py. It updates regional match counts by summed cell
deltas instead of recounting affected patches.1024 randomized incremental-state
and best-action parity checks passed. Dual-fast smoke is running.

## Hypothesis16: longer pair-walk sweeps cover more operations

The current walk reverses direction with probability1/16 at each proposal.
Under a fixed proposal budget this revisits a narrow region repeatedly. Reduce
the reversal probability to1/128 while preserving boundary reflection and
cooling-cycle restarts, giving longer passes through the sequence. This changes
no work budget and retains the best visited sequence. Prepare a separate
anneal_retained_long_walk.py from the frozen dual-fast source for later smoke.

Dual-fast stable250872488 (+5102 overbest021), all320valid, max4.037s,
totalprocess288.936s. Exactly the one lost cell in case213 is recovered; every
other score is unchanged. All147 N>16 output hashes again match the previous
candidate. Readiness20 is running. Prepared anneal_retained_triple_walk.py by
appending the canonically verified triple-walk layer to this measured source,
so the triple experiment retains all small-board gains and the faster updates.

Dual-fast readiness20/20passed,max3.314s, root saved best022250872488.
Triple-walk smoke17846200 (+1111), all20valid, max4.855s,total27.280s.
Runtime margin is too thin to expand the budget. Root's cached_best021 passed
all320 exact output hashes with State geometry and RefineState geometry/rank
cache optimizations. Copied both verified classes and _REFINE_GEOMETRY into
anneal_triple_cached.py and anneal_long_walk_cached.py before further runs.
Cached triple smoke will confirm output parity before stable evaluation.

Prepared the earlier informed-endpoint hypothesis on the current retained dual
parent with both verified caches: anneal_informed_cached.py. One fifth of pair
proposals use the exact immediate best operation at the omitted-pair boundary
as the fixed endpoint, then optimize the companion exactly as before. This
replaces one local-mutation mode without increasing proposal count. It remains
unbenchmarked until the current triple evaluation clears.

## Hypothesis17: hotter restart after preserving the full incumbent

On three independently generated random boards (N8/12, D2/3, K45/80), the
current pair annealer proposed16000 changes:1795 accepted zero-gain changes,
3 improvements, and only4 accepted one-cell losses. Most proposed changes
lost4..10 cells. The current cooling schedule behaves mostly as neutral
descent. Append a shorter hotter restart (temperature1.0 down to0.1) after the
full retained best022 search, always save its starting sequence, then run two
coordinate-repair sweeps. Use a seed derived from the input and incumbent
sequence, and cap work at600 proposals on N30 /2400 on small boards. This
tests stronger escape with a strict retained score floor and controllable cost.

Cached triple smoke matched all20 uncached output hashes, scoring17846200 with
max3.727s,total24.190s. Full stable250907216 (+34728 overbest022), all320valid,
max3.920s,totalprocess303.595s under shared load. Nine cases improved and zero
regressed:007,063,137,154,158,205,207,239,319. Readiness20 is running. This
candidate adds real work on maximum-size boards, so its final runtime gate
should include an isolated stress measurement rather than relying on output
parity with an older solver.

Cached triple readiness passed20/20,max3.060s. Prepared a separate
anneal_triple_hot_cached.py with the same bounded hot restart appended to the
new measured triple incumbent. Its retention rule preserves the triple gains;
the earlier anneal_hot_restart_cached.py remains an unbenchmarked ablation.

Longer-walk smoke17839558 (-5531 versus its retained-dual parent), all20valid,
max3.104s,total19.312s. Some repeated-stamp gains are outweighed by stripe and
checkerboard losses; reject this coverage change without a stable run.
Root's independent pool selector scored250921331, superseding the cached
triple's250907216 before a checkpoint. Keep the frozen triple component for
later combination, and finish the remaining two smoke hypotheses.

Informed-endpoint smoke17859660 (+14571 versus retained-dual parent),
all20valid,max3.012s,total18.850s. This is promising enough for a stable run,
but first finish the hotter-restart smoke and honor the root's upcoming
exclusive stress window. Source anneal_informed_cached.py remains frozen.

Hot+triple smoke17846200 ties the triple parent, all20valid,max3.750s,
total23.799s. No measured gain yet; no stable run started. A future development
ablation can decide whether gains exist outside smoke. All heavy work from
this agent is now clear for the root-coordinated exclusive stress window.
After release, prioritize the frozen informed-endpoint candidate's stable run.

Prepared anneal_best024_triple.py during the hold by appending the same frozen
triple-walk fragment to immutable best024250934988 (exact binary small-board
search on retained-dual, before the independent pool merge). No tests or benchmarks run during the timing hold;
this merged source remains unmeasured and is not a submission recommendation.

## Hypothesis18: cache omitted-window match counts without changing search

PairWalker.propose currently computes the old pair gain by applying and undoing
the first operation; TripleWalker does the same for two operations. Instead,
maintain the dot-match count of prefix colors against backward suffix wishes.
The old omitted-window gain equals the full sequence score minus this boundary
count. Window moves update the boundary count with exact operation_gain before
each value/wish swap, while accepted replacements leave the boundary unchanged.
This removes2 expensive bitset updates per pair proposal and4 per triple,
without changing any proposal, tie choice, acceptance decision, or work budget.
Implement separately as anneal_fast_walkers.py and compare both walker classes
against canonical states and the frozen old classes before parity benchmarks.

Boundary-cache oracle passed640 randomized steps covering both movement
directions, values/wishes swaps, and accepted arbitrary replacements. Every
proposal and delta equals the old walker, each cached boundary score equals
the explicit augmented dot product, and every full score matches canonical
simulation. N30/D3/C6/K180 microbenchmark, seed916448,1000 proposals with
reflected sweeps and unconditional acceptance: pair0.1905->0.1454s (1.31x),
triple0.2751->0.1776s (1.55x), identical final sequences. Results recorded in
anneal_fast_walkers_micro.json. This is an isolated performance result only;
full320 output parity is still required before calling the port qualified.

Informed endpoint stable251149505 (+277017 overbest022; +214517 overbest024),
all320valid,max3.222s,totalprocess234.877s. Versusbest022:24 improved cases,
8 regressions,288 ties. Readiness20 is running, after which all heavy work
will hold for the coordinated stress gate. Prepared anneal_informed_fast.py
with only the canonically tested PairWalker boundary cache changed; it has no
benchmark yet and must demonstrate full-output parity before use.

Informed readiness passed20/20,max2.932s. Root started its isolated36-case
maximum-size stress gate on the frozen measured informed source; other heavy
jobs are held. Promotion is pending this gate. The independently qualified
pool/binary composite was saved asbest025 in the meantime.

Informed isolated36-case maximum-size stress passed: max3.136s,p952.894s,
mean1.538s. Root saved best026251149505. Timing hold released; proceed with
smoke and full320 exact-output parity for anneal_informed_fast.py before
spending any saved time on a stronger neighborhood.

Boundary-cache smoke passed exact20/20 output-hash parity:17859660,
max2.863s,total17.768s. Full320 parity is now running on the frozen source.

## Hypothesis19: informed triple completion on the current composite

After the boundary cache qualifies, append a stronger triple walk to
pool_binary_informed.py. Retain its full output before any new search. Mutate
one endpoint, keep the other, and choose the middle exactly. For one fifth of
proposals, choose the mutated endpoint by exact immediate search after pulling
the retained final operation into wishes (or applying the retained first
operation to values). Restore the boundary after this proposal generation.
This extends the measured informed-pair idea to a larger neighborhood with
fewer random high-loss proposals. Keep the original triple temperature and
three restarts; budget1500 proposals on N30, cap6000 on small boards, then two
repair sweeps. Validate the informed endpoint against all legal endpoint
choices with the middle omitted, plus state-restoration and parent-score-floor
checks. Implementation waits for the pure boundary-cache parity gate.

Boundary cache qualified: exact320/320 output hashes and same251149505 total,
all valid,max3.166s,total236.764s under shared load. Readiness20/20passed,
max2.838s. Prepared anneal_informed_triple.py with the qualified fast walkers
and the planned conditional informed endpoint rule. Its new tests and smoke
are deferred while root runs exclusive stress on the weighted composite.

Weighted parent passed36-case stress and became best028251305191. Retargeted
the additive informed triple layer onto that immutable checkpoint as
anneal_weighted_triple.py, keeping the lower-parent prototype separate.
Canonical informed-endpoint optimality/state-restoration tests and five
weighted-parent score-floor checks passed (including the exact binary branch).
Smoke20 now running with one worker on the frozen merged source.

Weighted informed-triple smoke17962810 (+20765 overbest02817942045), all20
valid,max3.536s,total22.654s. Full stable251481350 (+176159), all320valid,
max3.882s,total323.827s under shared load.26 cases improved, zero regressed.
This confirms the stronger neighborhood retains the weighted parent case by
case while adding gains across both small and large boards. Readiness is the
last ordinary check before the next root-coordinated isolated timing gate.

Weighted informed-triple readiness passed20/20,max3.518s. All heavy work from
this agent is held for root's maximum-size stress gate. Source and result
artifacts are frozen. Shared the frozen source with the simulator agent for an
independent forward/backward coordinate-sweep wrapper; that work preserves
this candidate before testing additional improvements.

Weighted informed-triple passed the isolated36-case stress gate: max3.953s,
p953.808s,mean1.955s. Root saved best030251481350 and released heavy runs.

## Hypothesis20: restore temporary RefineState trials from small snapshots

Temporary endpoint trials currently undo a swap by applying it again, repeating
the cell-color bitset and regional-count updates. Save the touched grid colors,
stamp,63 value/goal bitsets, region counts and five planes before the trial;
restore them directly afterward. Actual/wishes nesting must restore in reverse
order. Apply this only to trial pair/triple completions and walker proposals;
permanent traversal swaps and constructor State remain unchanged. Require
canonical nested-restoration checks, exact old/new proposal/tie equality, then
full320 output-hash parity. No search budget changes until it qualifies.
This pure port stays based on030; the new tiny-board wildcard finisher can be
added independently after qualification.

Snapshot nested-restoration checks passed, including minimum/maximum boards,
post-constructor assignment of non-sentinel stamp wishes, no-op trials, and
mixed actual/wishes nesting.400 old/new walker proposals and tie decisions
also matched. Smoke20 had exact output-hash parity at17962810;max3.685s,
total23.642s under shared load. Initial micro results were mixed, so repeated
three trials in alternating order: median pair0.1394->0.1303s (1.07x), triple
0.1893->0.1659s (1.14x). Micro data are recorded separately; this does not yet
establish a faster complete solver. Full320 output parity is running.
The snapshot helpers target the unweighted RefineState fields used by sequence
trials, and snapshot live stamp wishes rather than assuming sentinel values.

Snapshot full320 qualification completed: all output hashes exactly match030,
score251481350, all320valid,max3.585s,total287.078s under shared load.
Readiness passed20/20,max3.449s. This is a behavior-preserving speed component.

## Hypothesis21: combine independent constructor and refinement undo ports

Frozen anneal_wildcard_snapshot.py starts from root wildcard_suffix_fast.py
(measured stable251668850). Transplant only the qualified snapshot helpers and
five unchanged parent units: optimize_pair, optimize_triple, triple_refine,
PairWalker and TripleWalker. AST source-span checks confirm every other
function/class, including constructor State undo, RefineState and all solver
budgets, exactly matches the parent. The root wildcard and extra suffix repair
remain unchanged. Require exact full320 output-hash parity and readiness before
an isolated maximum-size stress run. No search-budget increase in this port.

Combined speed qualification: merged nested canonical restoration tests and400
old/new walker proposals passed. Smoke all20 output hashes match the parent,
score17962810,max3.172s,total20.564s. Stable all320 output hashes also match
exactly at251668850,invalid0,max3.199s,total275.850s; parent hadmax3.957s,
total307.122s under separate shared-load runs. These timings suggest improvement
but isolated stress remains required to measure the final runtime margin.
Source merge audit and per-case parity summary are saved with result artifacts.

Combined readiness passed20/20,max2.731s, with canonical transition checks
recorded separately above. All heavy agent work is held for the root-coordinated
maximum-size stress gate. The source is frozen; this score tie is a pure speed
port and is not a new best-score checkpoint by itself.

## Hypothesis22: preserve the snapshot speed port through independent finishers

Root late_beam_forward.py extends the suffix wildcard solver with forward
coordinate sweeps and late exact beam finishing. Its State, RefineState and
five trial units are source-identical to the previously qualified parent.
Frozen anneal_late_snapshot.py transplants only those five snapshot trial
units and the two helpers. All other units are byte-identical within their
AST source spans; search budgets and independent finishers remain unchanged.
Require merged canonical tests and smoke parity now, then full320 exact-output
parity after root's parent report is available. Do not increase budgets.

Late-beam snapshot merge passed both canonical nested-restoration and400
walker-choice comparisons. Smoke20 output hashes exactly match the parent:
score17962810,invalid0,max3.621s,total23.469s under shared load. Full run is
held pending root's parent stable report, as requested. Source is frozen.

Root authorized the full run while its parent report was finishing. Merged
late-beam snapshot full320 is valid and all320 output hashes exactly match
late_beam_forward.py: score251734381,total295.248s,max3.876s. The unchanged
parent measuredtotal317.424s,max3.731s under separate shared-load runs; aggregate
time improved while the maximum varied upward, so no isolated timing claim is
made. Both source hashes match the frozen merge audit. Readiness is running.

Late-beam snapshot readiness passed20/20,max3.024s. Canonical nested snapshot
and walker-transition checks passed separately. All sessions drained and heavy
work is held for the root-coordinated combined speed stress test. The source
is frozen and no search budgets have changed.

## Late-beam cap4 independent small-board holdout

Root requested runtime and canonical validity checks for frozen
late_beam_four_fast.py (SHA516e709b120ffae1500da6a645d801335f81c497b377a92d10befc165b4177ca).
The reusable tools/anneal_late_holdout.py defines10 fixed-seed recipes covering
N5..9,D3,C3/6,K120/180 and reachable/near-target boards. Three predefined
reachable C6 reserve cases run only if none of the initial cases needs two
successful late repairs. All13 ultimately ran. Inputs, hashes, seeds, recipes,
raw and normalized output hashes, score and official subprocess timings are
recorded in results/anneal_late_four_holdout.json. Candidate bytes are unchanged.

A second fresh diagnostic process wraps the final reference solver and
late_beam_finish to count calls and validate each returned tail with the
canonical simulator. Its full output must match the official output after
line-ending normalization. Initial raw-byte comparison exposed Windows CRLF
versus reconstructed LF; the failing harness report is preserved separately,
and the corrected complete rerun passed. This was a harness formatting issue,
not a candidate output validity failure.

Final holdout passed13/13 canonical checks and13/13 diagnostic output parity.
Maximum2.566s,average2.108s under shared load. Eight cases entered late beam;
three made one successful repair each. None made two or more successful repairs
even after the three reserves, so this holdout does not establish coverage of
the third/fourth successful repair or the worst cost of all four repairs. It
complements root's measured stable cap4 examples and isolated timing checks.

## Hypothesis23: retain the full parent before a hotter triple restart

The current triple annealer starts at temperature0.44. A separately seeded
pass starting at0.9 may cross a one-cell valley and repair it later. Append it
after the complete frozen late_beam_four_fast parent, then run two ordinary
cleanup sweeps and retain the complete parent unless actual matches strictly
improve. Bound proposals at min(3000,max(300,675000//N©÷)), exactly750 atN30.
Use three cooling cycles down toward0.04 with a new input-derived seed.
Original anneal_triples and every parent budget remain unchanged. No claim
of improvement until smoke/full measurement; prior hotter ablations on older
parents tied smoke, so this is a bounded new test rather than an assumed gain.

The new test cases failed first because the candidate was absent. The new
self-contained source is anneal_retained_hot_triple.py. Source-span audit
confirms all parent units unchanged except renaming final solve to the saved
parent name; three new functions provide the optional retained branch. Heavy
benchmarks are held until the parent isolated timing gate is released.

Prepared hotter candidate passes14 canonical floor/K/determinism cases and
three full-parent comparisons, including exact parent preservation on ties.
Sixteen nested snapshot parameter cases and400 old/new walker choices also
pass; static submission inspection passes. Light test runtime was about5s
plus0.3s for restoration/choice checks. No smoke/full benchmark has started;
source and design audit are frozen pending the parent timing release.

After the035 isolated gate passed, hotter-pass smoke tied all20 parent output
hashes at17962810,invalid0,max3.357s,total22.863s. Development100 improved
80286651->80293248 (+6597),2wins/0losses. Case027 gains3cells (+3827),
case042 gains1cell (+2770). Devmax3.762s,total93.691s under shared load.
The gain is modest but affects two different large-board distributions and
timing remains plausible, so the frozen candidate proceeds to full320.

Hotter retained full320 improves035251765631->251801728 (+36097),8wins and
0losses,all320valid. The gains total11 matching cells and span N12..28, D2/D3,
C2..6, five families. Maximum3.741s,total344.597s under shared load compared
with parentmax3.337s,total287.177s on its separate run. The slowest new case
is N15,C5,K147 case205, which also improves by2cells. All100 overlapping
development outputs reproduce exactly in stable, supporting determinism.
Readiness is running; isolated timing remains pending before qualification.

Hotter candidate readiness passed20/20,max3.122s; its canonical floor and
state-restoration tests passed before benchmarking. All heavy sessions drained
and held for coordinated isolated timing or the independently qualified apply
speed-port composition. No checkpoint is recommended before that runtime gate.

## Hypothesis24: combine hot triples and commutators on the bit-plane engine

Root qualified refine_planes_only.py by exact320output parity to035 and
readiness38. Start from that frozen engine, append the unchanged retained hot
pass from037, then the exact pool_commutator_fragment last. Commute repair can
use operations left after hot repair, but interactions can prevent a particular
036 gain, so compare with per-case max(036,037) as an empirical hypothesis.
The full parent remains a guaranteed floor through both retained stages.
No parent budget, helper implementation or fragment is altered. Source audit
checks all59 parent units except renamed final solve are unchanged, hot helper
bodies exactly match037, and all fragment function bodies are identical.

Combined engine passed10 merged tests, including canonical floors, strict tie
retention,576 commutator delta/restoration checks, snapshot restoration with
counts=None,400 walker choices and deterministic hot repair. Smoke20 is valid
at17962810,max3.091s,total20.219s. Dev100 exactly matches all037 output hashes
at80293248,max3.423s,total92.726s. The known036 gain is outside development:
fixedcase173 retains +5917 over037 and matches036 (161matches,952662score),
valid in2.796s. Root agreed this complementary gain plus dev exact parity
justifies full320 despite development score tie. Per-case max(036,037) predicts
251807645; treat it as a hypothesis until the fixed full run completes.

Combined full320 measured251807645 (+5917 over037),all320valid. Every case's
score AND output hash exactly equals the selected better parent from036/037
(with hot037 selected on score ties). There are no interactions or deviations
from the predicted per-case maximum. Maximum3.498s,total302.448s under shared
load, versus hot-alone total344.597s on its separate run. Readiness running.

Combined readiness passed20/20,max2.785s. Canonical floor, restoration and
commutator tests passed earlier. All sessions drained; source frozen and heavy
work held for root's checkpoint/runtime decision and independent deeper-beam
composition after that component qualifies.

## Hypothesis25: packed all-action beam for short budgets on larger boards

Coverage review: existing finite_beam coversK3..24 atwidth24/12 but expands
only8 near-greedy moves per state, with a one-step future heuristic. Previous
all-action packed beams targetN<=9 finishers orN4 exact searches. A distinct
retained alternative can enumerate ALL legal moves at every frontier for
N>=10,K4..8 using3-bit packed grid+stamp states and widthmin(96,100000/actions).
This bounds children below703364 for maximum8depth, within the requested800k.
The frozen suite has26 eligible cases (4dev,0smoke), so targeted evaluation
is the useful first score gate. Parent is immutable038. Keep the best prefix
over all depths, apply two ordinary cleanup sweeps, and retain the complete
parent unless actual matching cells strictly increase. Action paths use two
bytes per ID to support the maximum3363 action. No parent budget changes.

Canonical rotation/high-ID, exhaustive two-move and parent-floor tests were
written and failed on missing candidate before implementation. Prepared
anneal_lowk_packed_beam.py and reusable fragment. No score claim yet.

Packed low-K tests pass for12 board/stamp/color configurations throughN30,
including all rotations, IDs255/256 and maximum IDs, involution, exhaustive
two-move optima on three small shapes, >255 returned-path witnesses for bothD,
and complete-parent floor checks. All26 eligible stable cases are valid.
Targeted delta+6993 from182 (+1cell,+3086,N18D3K7) and310 (+1cell,+3907,
N16D2K6), zero losses. Maximum total candidate runtime2.558s,total44.092s
under shared load. This is not yet a full320 improvement claim. Smoke/dev
next primarily verify parent behavior; both observed wins lie outside them.

Root requested one complete full benchmark rather than a standalone low-K
full below the upcoming composite. Prepared anneal_all_repairs_complete.py
from readiness-agent frozen pool_all_repairs_patch_stamp.py, adding the exact
low-K fragment last. AST source audit preserves every parent definition except
renaming final solve to the retained parent. No helper or budget changes.
Wait for the all-repairs parent full/readiness and patch/stamp smoke/dev plus
173/265 gates, then verify low-K gains182/310 on the composite before full320.
The complete union251887328 is a prediction only, not a measured score.

Standalone packed-beam smoke20 and dev100 both reproduce all038 parent
output hashes exactly: smoke17962810,max3.191s,total20.766s; dev80314429,
max3.307s,total85.971s. The candidate changes scores only on the two targeted
cases beyond development. All active jobs drained for root's all-repairs
isolated stress window. Complete composite passed all three canonical groups
and static inspection; its audit preserves75 parent definitions unchanged.

Complete-source smoke20 matches039 output hashes exactly at17967254, all
valid,max3.207s. Targeted low-K gains survive:182150matches/+3086 in2.652s;
310256matches/+3907 in1.409s. Awaiting readiness-agent patch/stamp dev gate.

Added a disjoint fixed-seed maximum-board K8 holdout (N30,D2/D3,C2/C6),
paired sequentially with the complete parent to cover the low-K beam's largest
enumeration budget skipped by N30/K180 stress. All4valid, no floor losses,
max candidate3.586s. Overhead1.415..1.750s under shared load, slightly above
the1.5s aim forD3C6 but below5s total. That fourth holdout improves by1cell;
others tie. Seeds,input/output hashes,source hashes and paired timings saved
in results/anneal_all_repairs_complete_lowk_holdout.json. No new benchmark
score claim is derived from holdout cases.

Readiness-agent final gates passed: patch/stamp smoke20 and dev100 exactly
reproduce039 output hashes, with173 +5917 and265 +12345 on fixed targeted
cases. Complete source and its parent SHA remain frozen. Started the single
complete320 benchmark; expected039+25255=251887328 remains only a prediction
until measured. Readiness agent concurrently runs13 independent small-board
holdouts, while this agent will follow full320 with standard readiness.
