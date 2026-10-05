# Seven-million-point campaign result

Selected submission: [`runtime_055_254652429.py`](../submissions/runtime_055_254652429.py).

The requested gain of 7,000,000 points was not achieved. The verified gain is **548,531**, reaching **254,652,429** on the unchanged 320-case benchmark. Remaining shortfall: **6,451,469**.

| Measurement | Stable score |
|---|---:|
| Initial greedy checkpoint 000 | 228,305,971 |
| Campaign starting solver, runtime 053 | 254,103,898 |
| Requested threshold | 261,103,898 |
| Selected checkpoint 055 | 254,652,429 |

Compared with the campaign start, 41 cases improved, 273 tied, and 6 regressed. These are local results from 320 cases. The unseen official 40-case score has not been measured.

## New immutable checkpoints

| ID | Score | Change from preceding best | File |
|---|---:|---:|---|
| 54 | 254,492,748 | +388,850 | [best_054_254492748.py](../submissions/best_054_254492748.py) |
| 55 | 254,652,429 | +159,681 | [best_055_254652429.py](../submissions/best_055_254652429.py) |

All 56 checkpoints are preserved, and their hashes were checked. See [history.csv](../results/history.csv) for the complete score progression and the [previous report](million_report.md) for checkpoints 000–053.

## Search results

The selected solver searches backward from the target while leaving the final stamp unconstrained, then reverses the operation sequence. For targets with few distinct patches, this replaces an early constructor and feeds its result into existing refinement. Exact bit-parallel gains, static pickup masks, and bytearray state copies keep the search cost manageable.

The selected solver also uses a forward constructor that rewards keeping remaining mismatches adjacent. It runs before refinement on a disjoint input domain and skips the later plain beam. The final benchmark includes any regressions caused by this replacement.

The selected runtime variant preserves all 320 scores and stdout hashes from immutable checkpoint 055. Its private cluster states use bytearrays and update only the score planes consumed by the beam. Recorded paired helper timings show a 31.0% reduction in mean cluster-search runtime. The full stable run measured 445.680 seconds versus 456.433 seconds for checkpoint 055, with a selected stable maximum of 4.964 seconds. Expanded validation for the selected bytes is reported below. A further stamp-plane cache did not materially improve whole-program runtime and was rejected; see [the cache measurements](seven_construct_cache.md).

On the 100-case development suite, distant-pair repair gained 2,222 points, Gibbs coordinate annealing gained 13,822, and coarse-color continuation gained 7,778. Their gains did not justify the added runtime; Gibbs added up to 2.315 seconds. Disjoint-patch assignment produced no development wins.

A later experiment alternated global assignments across two shifted patch tilings. Allowing independently chosen rotations for each transfer improved its raw constructions, but neither variant beat checkpoint 055 on any of the 13 eligible development cases. The free-rotation variant took up to 1.617 seconds and passed 40 additional canonical checks. It was rejected; see [layered-assignment research](seven_sequence_layered.md).

Strict and neutral long-window reconstruction replaced windows of 12, 24, or 32 operations using beam width 24 and three or six rounds. On 36 eligible development cases it produced no new search gain over the best-known paths and checkpoint 055. An apparent 13,471-point improvement only recovered regressions relative to older checkpoint 053 paths.

Cached stable diagnostics found gains of 106,577 for mixed forward/backward construction, 336,679 for a wider standalone backward beam, and 321,463 for a clustered beam. These diagnostic gains overlap and cannot be added together. The mixed constructor was rejected for excessive integration cost.

Details: [campaign log](seven_campaign.md), [constructor research](seven_construct.md), [sequence research](seven_sequence.md), [backward review](seven_fastback_review.md), [integration review](seven_combined_review.md).

## Validation

The benchmark remains frozen at seed 20260925: 20 smoke cases, 100 development cases, and 320 stable cases across eight families. All 320 input hashes were rechecked. Evaluation uses the canonical simulator, strict output validator, exact integer scorer, reproducible generator, benchmark runner, and immutable checkpoints.

| Check on selected bytes | Result | Maximum seconds |
|---|---|---:|
| Stable benchmark | 320/320 valid | 4.964 |
| Random/boundary readiness | 38/38 plus repeat | 4.933 |
| Maximum-size holdouts | 36/36 valid | 4.620 |
| Added periodic holdouts | 14/14 valid | 4.081 |
| Changed-output reproduction | 47 exact scores and output hashes | 4.257 |

The stable run took 445.680 seconds in total, averaging 1.393 seconds per case. The worst verified runtime was 4.964 seconds against the 5-second limit. This leaves limited margin on this machine; hidden inputs or different hardware may take longer.

The selected file is 29,022 bytes, reads stdin, and emits only the required operations. It uses no local files or third-party dependencies. Its standard-library LZMA wrapper decodes exactly to the inspected readable Python source. `solvers/current.py` is an identical copy. SHA256: `ecfda09a7e51200f49ceed3bf025c840144d457ba31e5ff9679bda2d9555bfa6`.

## Limit of the result

Color conservation, exact short-prefix searches, whole-board rotation orbits, independently checked integer coverage certificates, and a stamp-transport bound that accounts for repeated grid contacts give a stable-score upper bound of **262,303,537**. This allowed at most **8,199,639** additional points at the campaign start; 178 baseline cases were already provably optimal. A 7-million-point gain required about 85.37% of that remaining room. The selected solver meets these ceilings on 178 cases, leaving at most **7,651,108** further points. This upper bound does not establish whether the requested threshold is attainable. The evaluated methods did not reach it.

Proofs and per-case evidence: [bound audit](seven_bound.md), [latest transport bound JSON](../results/seven_bound_transport.json), and its [full 320-case parent bound JSON](../results/seven_bound_joint.json).
