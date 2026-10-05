# Target-oriented routing experiments

Parent checkpoint: `best_039_251862073.py` (stable total 251,862,073).

Hypothesis 1: for stamp placements P,Q, `(P Q)^3` cancels all unaffected three-cycles. A single-corner overlap leaves a five-cycle across three grid cells and two stamp cells. These sparse permutations can fix isolated residual errors with less collateral damage than the four-operation commutator. Compile the exact permutation symbolically, test against the canonical simulator, and append only a strictly positive exact-gain macro. Both orderings and the square of the six-step macro are considered, within remaining K.

Only parent states with at least six operations unused and score below the color inventory bound are eligible. Initial measurements are targeted diagnostics, not full stable benchmark evidence.

## Measured scalar routing results

The first candidate retained parent039 and appended exact positive-gain sparse permutations. `tools/test_route_sparse.py` compared compiled permutations against the canonical simulator for both D values. The standalone `route_39_six_three.py` smoke20 run had 0 invalid outputs, total 17,974,907, and maximum observed runtime 3.758s under shared load.

Cached parent039 diagnostics (all 21 eligible states, including N>20):

| Candidate | Exact score delta | Winning cases | Maximum added seconds |
|---|---:|---:|---:|
| Six operations, one macro | 126,878 | 17 | 0.276 |
| Six operations, three macros | 221,439 | 17 | 0.658 |
| Six operations, up to 16 macros | 266,540 | 17 | 2.334 |
| Six/twelve operations, up to 16 macros | 263,808 | 17 | 3.971 |

Twelve-operation greedy choices can consume budget less effectively; retaining both paths yielded a diagnostic gain of 283,069 but was too slow on larger boards. Root identified and implemented cancellation of adjacent identical involutions. Cancellation preserved the entire board and stamp and increased route-eligible parent039 states from 21 to 40. Six-step routing after cancellation gained 440,687/550,475/652,147 for 3/5/8 rounds respectively; the adaptive limit `min(8,max(3,2500//N**2))` gained 568,062 with maximum added runtime 0.885s.

Exact scalar pruning uses the number of initially incorrect supported cells as an upper bound and subtracts surviving errors, stopping when it cannot beat the current best. This preserved every selected macro on all 40 cached states. Adaptive total routing runtime fell from 8.698s to 5.982s and the maximum from 0.885s to 0.609s.

## Larger algebraic powers

`(P Q)^5`, `(P Q)^6`, `(P Q)^9`, and `(P Q)^12` expose additional sparse permutations. Same-position rotations were also tested but gave no gain on the initial modern parent. Unique source-label differential tests verify the exact permutation rather than merely color scores.

On root's cached `algebra27_t8_r12` result (252,192,457), sequential powers produced:

| Added power | Total diagnostic score | Increment |
|---|---:|---:|
| 6 | 252,259,352 | 66,895 |
| 6 | 252,296,039 | 36,687 |
| 9 | 252,312,853 | 16,814 |
| 5 | 252,334,963 | 22,110 |
| 12 | 252,357,374 | 22,411 |
| 3 | 252,376,736 | 19,362 |
| 6 | 252,382,043 | 5,307 |
| 9 | 252,386,072 | 4,029 |
| 12 | 252,387,348 | 1,276 |

An intervening second power5 stage gave no gain and was omitted. These are diagnostics from validated cached parent sequences, not substitute full executable stable benchmarks. The `route_extra_powers` helper explicitly guards `remaining_K >= 2*power` and updates the exact stamp between stages.

## Exact bitparallel routing

Root suggested scoring all legal anchors simultaneously with color-position bitsets. `route_bits_fragment.py` implements this exactly: for each sparse permutation, add new matches and old mismatches into count bitplanes. The accumulated value is `mapping_size + gain`. Legal anchor masks prevent row wrapping; signed shifts handle negative relative columns. Selecting the largest value and then the lowest anchor bit preserves scalar iteration and tie ordering. Cached shifted color masks and source/destination equality masks reduce repeated work.

Frozen fragment SHA256: `dd65fb0c535b7b80656afe150daf584c1fd2ca22ef1eab2664d477502fdedc3f`.

Measured validation:

- 30 fresh complete-path comparisons against scalar routing, D=2/3, N=3..30, single and combined powers 3/5/6/9/12: exact same operations.
- All 40 cancellation-eligible parent039 paths: exact equality. Total helper time 5.982s scalar versus 0.485s bitparallel; maximum 0.609s versus 0.0278s.
- 36 fresh full-power holdouts, schedule `[6,6,9,5,12,3,6,9,12]`, N=3..30, D=2/3, C=2/6, K=1/180, random/near/stripes/reachable families: exact scalar path equality, canonical final board/stamp equality, output validity, and score floor. Paired maximum helper runtime 1.485s scalar versus 0.133s bitparallel; total 6.442s versus 1.612s.
- Independent reviewer verified signed shifts, anchor legality, bitplane capacity and ties. The unused `repeats=(2,), K=4` API discrepancy was fixed by retaining scalar's `K<6` guard; dedicated regression passed.
- The independent broader scalar review checked 5,552 unique-label permutations, 24 fresh pruned/unpruned paths, and 36 full-power holdouts.

Key artifacts: `tools/test_route_bits.py`, `tools/test_route_review.py`, `results/route_bits_cached_parity.json`, `results/route_bits_full_power_holdout.json`, and `results/route_review_holdout.json`. Root owns full solver runtime qualification, stable benchmarks and checkpoint promotion.

## Earlier source-size work

Before the code-size limit correction, exact consolidation of parent028 reduced duplicate state setup and count-plane selection. `route_core028_slim.py` passed exact state, method and small-solver equivalence tests; adding cancellation and adaptive routing packed to 9,812 bytes. This candidate was not promoted or fully benchmarked. A later State/WeightedState `apply` consolidation saved only four compressed bytes and was rejected as not useful. The corrected 100,000-byte limit makes these packaging experiments unnecessary for the final direction.
