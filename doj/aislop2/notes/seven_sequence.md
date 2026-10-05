# Seven-million campaign: sequence neighborhoods

Authoritative parent: `submissions/runtime_053_254103898.py`, stable score
254,103,898. Diagnostics use cached parent outputs and the canonical simulator,
validator, and exact integer score. These are research fragments, not submissions.
No checkpoint, history, current solver, or benchmark input was changed.

## Exact distant-pair repair

Hypothesis: replacing operations far apart can coordinate transported colors in
ways that adjacent pair/triple neighborhoods cannot. For a sampled pair of slots,
the intervening operations form an exact permutation. A replacement at the first
slot changes at most three stamp-sized sets of values. Transport those changes
to the second boundary, update the bit-parallel refinement state, and find the
globally best second action. Accept only a strict true-score improvement.

`solvers/experiments/seven_sequence_spaced.py` implements this, including ranked
first-action alternatives from several conditional gain levels. Accepted scores
are checked against independent snapshot reconstruction within the algorithm.

On the older parent052+beam24 development cache, 48 pairs with 10 random/local
alternatives gave +6,230 (two wins), max incremental 0.442s, total 8.575s. Adding
ranked alternatives and increasing to 64 pairs / 24 alternatives gave the same
6,230 at max 1.531s, total 32.713s. On the authoritative053 development100 cache,
24 pairs / 8 alternatives gave only **+2,222**, one win, max 0.423s, total 8.027s.

## Heat-bath coordinate annealing

Hypothesis: sample operation coordinates from the exact conditional score
distribution, making neutral/near-neutral exploration more effective than mostly
rejected random mutations. A backward sweep computes bit-parallel gain groups,
samples an action with exponentially weighted score, and updates suffix wishes.
The incumbent is retained throughout; temperature cools and restarts every 16
sweeps. This differs from the old global mutation probe and weighted objectives.

`solvers/experiments/seven_sequence_gibbs.py` implements this. Every completed
sweep checks the maintained score against full forward reconstruction.

On older052+beam24 development100, 32 sweeps / initial temperature0.4 gave +7,492
(three wins), max0.627s, total8.688s. On authoritative053 development100,
128 sweeps / initial temperature0.8 gave **+13,822** (three wins:007,015,021),
max incremental2.315s, total30.298s. The largest input costs make this unattractive.

## Coarse color objective continuation

Hypothesis: temporarily merge a pair of colors or apply a binary color partition,
refine that easier objective, then restore all actual colors and refine again.
This permits useful rearrangements rejected by the exact objective while retaining
true-score acceptance. Pair merges and partitions depend only on input colors.

`solvers/experiments/seven_sequence_coarse.py` tries 16 projections, two coarse
sweeps, then four true sweeps. On authoritative053 development100 it gave
**+7,778** (two wins:001,007), max incremental1.756s, total16.547s.

## Validation and conclusion

Every diagnostic candidate was output-validated and canonically simulated before
measuring its score; no candidate regressed. An additional inline random check
covered36 fresh instances and all three helpers:108 output-validity and
parent-score-floor checks passed. Internal exact-score assertions also passed.
Evidence is `results/seven_sequence_review.json` and the six development reports
under `results/seven_sequence_*`.

These directions do not justify a full320 qualification run or integration into
the already near-limit parent. The strongest measured development gain is13,822,
far short of the requested7,000,000 stable increase. Wider conditional-pair or
Gibbs runs are feasible but their observed return per CPU second is weak.
Substantial progress would require a different construction/objective or a
dramatic runtime improvement that enables much wider global search.
