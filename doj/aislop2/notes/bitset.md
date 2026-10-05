# Bit-sliced action evaluator

Candidate: `solvers/experiments/bitset_lookahead.py`.

Hypothesis: transpose target comparisons across actions into Python integer
bitsets to replace thousands of scalar `bit_count()` calls per best-action
query. For each reference stamp cell and color, one bitset identifies matching
actions. Binary bit planes sum these masks for all actions simultaneously.
Maintained planes store `D*D - old_patch_matches`; adding them produces a
nonnegative action key `D*D + immediate_gain`. Five descending bit filters
find the largest key. The lowest remaining bit preserves the baseline's
exact action tie order.

The constructor accepts an optional action order. It must be finalized before
bitsets are built. `apply()` updates old-match planes only for affected regions.
The high-level search currently matches `lookahead_multi4.py` exactly: four
deterministic restarts and 32 candidate two-ply escapes. Scalar packed masks
remain available for escape candidate selection.

Verification completed:

- `python -m unittest tools.test_bitset -v`: two tests pass.
- 2,400 randomized best-action/tie comparisons, spanning N=3,7,14,30 and both D.
- Resulting grid/stamp transitions agree with the canonical simulator.
- Complete output sequences equal the baseline on the first 24 frozen cases.

Measurements:

- Fixed N=30, D=3, C=2 state, 2,000 best-action queries: scalar 0.524759 s,
  bitset 0.010359 s (50.66x faster for this kernel).
- Four restarts / width 32 smoke: 17,530,904; 20/20 valid; 3.202 s total,
  0.416 s maximum, one benchmark worker.
- Four restarts / width 32 stable: 243,391,996; 320/320 valid; 35.697 s total,
  0.466 s maximum, one worker. All 320 output SHA256 values equal the scalar
  `lookahead_multi4` report, not only its aggregate score.
- The historical scalar stable result used two workers (42.608 s summed,
  1.602 s maximum); this is not a controlled whole-solver speed comparison.
- Variant `bitset_lookahead8.py` uses eight restarts / width 64. Smoke:
  17,617,494 (+86,590), 20/20 valid, 5.360 s total, 1.053 s maximum. Stable
  score: 244,416,962 (+1,024,966 against four restarts / width 32), all 320
  cases valid, 53.896 s total, 1.207 s maximum. Readiness: 38/38 valid,
  deterministic, maximum 0.623 s. The wider variant has the same transition
  and gain machinery, now also exercised by the randomized differential test.
- The wider standalone solver is below best_008's 246,335,486. It beats that
  checkpoint on 18 cases; choosing the better final grid from both on every
  case would add 280,207 for 246,615,693. This is an offline potential portfolio
  score, not a measured combined implementation or a new best checkpoint.

No history/checkpoint/current-solver files were changed by this experiment.
