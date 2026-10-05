# Sequence refinement experiments

Frozen suites: cases/manifest.json (seed 20260925). Primary stable suite has 320 cases.

## Hypothesis 1: exact backward coordinate descent

Each stamp operation is a permutation of grid-plus-stamp colors. Inverting the
later operations on the final target (with unconstrained stamp cells) creates
an exact target for every earlier position in the sequence. Exhaustively
choosing a replacement operation can then improve final score using only the
cells touched by that operation. Starting from strict greedy and accepting only
nondecreasing changes should retain the baseline while improving collected
stamp colors for later operations. Three backward sweeps and up to four new
operation slots per sweep are the first bounded experiment.

Validation planned: differential replacement gains against full canonical
simulation, greedy floor preservation, smoke suite, then stable suite if useful.

Result: sequence_refine.py stable total 229289892, +983921 versus initial greedy,
all 320 valid, sum runtime 20.576s, worst 0.437s. Smoke total 15388809 (+61675).
This is a valid gain, but independent plateau lookahead has already reached
240849239. Keep the refinement implementation and apply it to that stronger
starting sequence rather than optimizing the weaker baseline further.

## Hypothesis 2: repair the lookahead sequence

The same exact backward coordinate descent may repair early choices in a
stronger lookahead sequence. Inline lookahead.py's constructor with the existing
three-sweep refinement, keeping it fully self-contained. Then test randomized
ties and additional sweeps to explore equal-score sequences without reducing
the final score.

Result: sequence_lookahead.py stable 241684688 (+835449 over lookahead), all320
valid, sum29.765s, max0.908s. Smoke17327125. Twenty fixed-seed small randomized
instances independently check that the combined solver preserves or improves
its constructor's score, using the canonical simulator.

## Hypothesis 3: traverse equal-score sequences

Coordinate descent stops quickly if existing operations are preferred on ties.
Randomizing candidate order and choosing equal-score alternatives changes how
colors flow through the stamp while preserving final score exactly. Six sweeps
and up to eight extra operation slots per sweep may expose later improvements.

Result: sequence_plateau.py stable243506592 (+1821904 over strict refinement),
all320 valid, sum55.944s, max1.828s. Smoke17556543. This improved on the then
multi4 benchmark, but the portfolio solver completed244316245 and readiness
first, so this variant was superseded before qualifying as a global checkpoint.

## Hypothesis 4: refine the selected portfolio winner

Inline portfolio.py and refine only its selected winning sequence, saving the
cost of optimizing each component independently. Four randomized sweeps keep
the expected worst runtime below three seconds.

Smoke: sequence_portfolio.py17705462 (+133724 over portfolio), all20 valid,
max2.714s. Stable245544191 (+1227946 over portfolio), all320valid, sum90.485s,
max2.720s. Readiness20/20 passed, max2.309s. Root was notified immediately for
checkpoint promotion. Full project test discovery passed47tests at this point,
including score preservation on the portfolio wrapper.

## Hypothesis 5: refine the three-way portfolio winner

The root added productive lookahead as a third construction strategy. Apply the
same refinement only to its selected sequence. Three sweeps give smoke17692065,
all20valid, max3.217s. Four sweeps improve smoke17738064, all20valid, max3.644s.
Since exact coordinate choices never reduce final score, the fourth sweep is
monotonic for a fixed construction and random seed; its runtime is acceptable.

Final candidate: solvers/experiments/sequence_portfolio3_four.py.

- Stable total246335486, average769798.39375; all320valid.
- Stable runtime sum94.641s, max4.271s, wall47.670s with jobs2 and concurrent
  readiness checks. Readiness sequential max2.992s, all20cases pass.
- Gain over two-way refined solver: +791295.
- Smoke17738064, +32602 over two-way refined solver.
- Results: results/sequence_portfolio3_four_stable.json and
  results/sequence_portfolio3_four_readiness.json.
- Full project discovery passes56tests, including random exact replacement gain
  comparisons against canonical full suffix simulation and randomized tests
  that refinement preserves each constructor's final score.
- Deterministic fixed-seed choices; no file input, no local imports, only the
  standard library, no stderr/stdout diagnostics. Single-file submission.
- All benchmark inputs and manifest remain unchanged.
- Simulator agent will independently run the separate maximum-size runtime
  holdout without these benchmark processes running.

The root owns global checkpoint promotion and solvers/current.py; this research
task does not mutate submissions, score history, or current.py.
