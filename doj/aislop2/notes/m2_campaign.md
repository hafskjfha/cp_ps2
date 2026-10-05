# One-million campaign from checkpoint 055

Starting stable320 score: 254,652,429. Required threshold: 255,652,429.
The frozen manifest and all old checkpoints are retained. Official runtime is five seconds.
Only canonical evaluations on the unchanged benchmark count as improvements.

Independent research domains: stronger construction, sequence rearrangement,
compact-board search and algebraic repair, and exact runtime savings.

## Root experiments before integration

- Packed rank transpose: exact across 56 legal N/D geometries; roughly fivefold
  large-input initialization microbenchmark speedup. No score change.
- Relabel/transpose restarts: original constructor, two variants, +44,891
  development points. Full solver, two variants, +141,221; duplicates 2-8 seconds
  per eligible case. Not integrated.
- Sequence crossover followed by exact refinement: +10,165 development points,
  mostly overlapping restart gains, up to 1.259 additional seconds. Rejected.
- Temporarily drop random, color, or spatial objective constraints: +16,918
  development points over 16 trials, up to 1.687 additional seconds. Rejected.
- Uniform tied-action sampling instead of gap-weighted offset sampling: +64,919
  cached development points at width 64, weaker than selected forward variant.
- Increased forward future weight to 1.0: +49,601 cached development points,
  weaker than weight 0.5.
- Reverse width 128: net +39,346 development points in the whole pipeline,
  maximum 6.507 seconds. Rejected for runtime.
- Pattern-directed stamp-pickup beam: zero development wins.
- Diverse reverse-beam finalists refined separately: zero development wins.

## First combined candidate

`m2_combined.py` (33,304 bytes) includes exact runtime kernels, an early width-64
quotient forward beam plus width-16 clustered beam, and generalized cycle repair.
Smoke20 passed: 18,295,068 points, maximum 4.126 seconds.
Full stable qualification is running; no checkpoint has been saved yet.

Constructor research: `notes/m2_construct.md`. Cycle research: `notes/m2_gap.md`.
Sequence and arithmetic-kernel research: `notes/m2_sequence.md`.

Full stable result for exact combined bytes: 255,006,286 (+353,857), all 320 valid, 375.834 total seconds, maximum 4.070 seconds. 33 wins and 3 losses against055. The additive forecast overstated gain by5,917 because the constructor and cycle repair overlap oncase173. Readiness and maximum-size qualification are running.

Additional full-horizon forward/backward frontier joining atthree cuts, with exact bitset all-pairs seam scores and free stamp-frame alignment, produced zero development wins; rejected.

Saved immutable submissions/best_056_255006286.py. Readiness38, maximum-size36, and all36 changed-score output reproductions passed. Worst verification runtime4.395s. solvers/current.py is the exact checkpoint. Further research continues toward255,652,429.
