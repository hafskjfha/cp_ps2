# Initial optimization round report

Best submission at the end of the initial round: [`best_010_246874186.py`](../submissions/best_010_246874186.py).

Stable benchmark: **246,874,186 / 320,000,000**, average **771,481.83**. Initial greedy: **228,305,971**, average **713,456.16**. Improvement: **18,568,215 points (+8.13%)**. The exact saved checkpoint reproduced all 320 per-case output hashes and scores. These are local generated-case scores, not an estimate of the official 40-input result.

## Benchmark and baseline comparison

Frozen seed 20260925; nested 20 smoke / 100 development / 320 stable. Stable 320 is the sole promotion benchmark. Eight families cover both stamp sizes, all color counts, every N=3..30, small and large operation budgets, exact endpoints, repetitive targets, reachable targets, near-matched and difficult random states. Independent runtime holdouts do not change the benchmark.

| Baseline | Stable total | Average |
|---|---:|---:|
| Zero operations | 174,748,782 | 546,089.94 |
| Best single operation | 186,065,927 | 581,456.02 |
| Strict immediate greedy | 228,305,971 | 713,456.16 |

## Every saved best checkpoint

| ID | Stable total | Change | Submission |
|---:|---:|---|---|
| 000 | 228,305,971 | Initial strict immediate-gain greedy; beats zero and single-operation baselines | [best_000_initial.py](../submissions/best_000_initial.py) |
| 001 | 240,756,242 | Packed greedy with neutral stamp-state exploration and four deterministic restarts | [best_001_240756242.py](../submissions/best_001_240756242.py) |
| 002 | 240,849,239 | Packed greedy with exact positive-total two-ply escape including negative setup moves | [best_002_240849239.py](../submissions/best_002_240849239.py) |
| 003 | 242,249,708 | One-hot match evaluation enables twelve deterministic plateau-search restarts | [best_003_242249708.py](../submissions/best_003_242249708.py) |
| 004 | 243,391,996 | Four deterministic lookahead restarts with randomized action tie orders | [best_004_243391996.py](../submissions/best_004_243391996.py) |
| 005 | 244,316,245 | Select better of twelve neutral plateau runs and four two-ply lookahead runs | [best_005_244316245.py](../submissions/best_005_244316245.py) |
| 006 | 245,343,012 | Three complementary searches including lookahead during positive-gain moves | [best_006_245343012.py](../submissions/best_006_245343012.py) |
| 007 | 245,544,191 | Four exact backward coordinate sweeps with neutral ties refine the two-stream portfolio | [best_007_245544191.py](../submissions/best_007_245544191.py) |
| 008 | 246,335,486 | Four randomized exact backward sweeps refine the best of three complementary constructors | [best_008_246335486.py](../submissions/best_008_246335486.py) |
| 009 | 246,786,935 | Bit-sliced action evaluation funds eight width-64 lookahead restarts and six refinement sweeps | [best_009_246786935.py](../submissions/best_009_246786935.py) |
| 010 | 246,874,186 | Bit-sliced plateau and lookahead search with eight exact backward refinement sweeps | [best_010_246874186.py](../submissions/best_010_246874186.py) |

## What improved the score

- Zero-gain moves explore new outgoing stamp states while preserving the best prefix. Fixed input-derived random seeds diversify tie orders.
- Exact two-ply lookahead accepts a negative first move only when the pair increases matches. Lookahead during productive moves supplies complementary paths.
- A three-strategy portfolio selects the best actual final grid before refinement.
- Backward propagation of target wishes evaluates operation replacements exactly. Random equal-score replacements expose improvements in later coordinate sweeps.
- One-hot color masks and transposed action bitsets reduce repeated Python candidate scans. This funded eight width-64 lookahead restarts and eight refinement sweeps while remaining within the five-second local checks.

## Less successful or limited ideas

- A single immediate operation scored 186,065,927; strict greedy was substantially stronger.
- Refining strict greedy alone reached 229,289,892, far below stronger constructors. It was retained as an experiment.
- Increasing plateau trials4->8->12 produced diminishing smoke gains. Widening plateau lookahead to 128 improved its own baseline but did not beat the best diversified constructor.
- Productive-step lookahead alone did not beat the strongest standalone restart search, but did help the portfolio.
- Three refinement sweeps lost smoke score versus four. Increasing six to eight sweeps later added only 87,251 stable points; further tuning was left for a future session.

## Final verification

- 60 unit/property/differential tests pass, including all four rotations for D=2/D=3, independent matrix simulation, exact replacement deltas, bitset/scalar action parity, and score-preserving refinement.
- 38 final readiness cases pass with isolated standard-library execution, syntax/import inspection, deterministic repeat, min/max boundaries, and strict validation.
- Stable 320 repeated using the exact saved file with jobs=1: no invalid outputs, total 246,874,186, aggregate runtime122.321s, mean0.382s, maximum2.711s.
- Maximum output on stable 320: 1,496 bytes; maximum operations: 180. The official byte limit is 100,000 bytes.
- All 11 checkpoint source hashes verified; scores strictly increase. Regeneration left all 321 case/manifest files unchanged.
- Independent review found no blocking correctness issues in rotations, apply/undo, bitset ordering, portfolio selection, or backward refinement.

**Final maximum-size holdout: all 36 cases passed.** Every case uses N=30 and K=180; both D values and all C values are covered, along with random and structured targets. Sequential runtime: maximum **3.559s**, p95 **2.864s**, mean **1.655s**, against the **5.000s** limit. Evidence: [final_stress.json](../results/final_stress.json). These are measured CPython 3.12.12 times on this machine; no wall-clock-dependent search or uncontrolled randomness is used.

## Family breakdown

| Family | Initial average | Final average | Delta |
|---|---:|---:|---:|
| checkerboard | 456,032.39 | 573,124.51 | +117,092.12 |
| local_adversarial | 887,554.22 | 918,040.20 | +30,485.97 |
| near_target | 944,852.86 | 955,247.95 | +10,395.10 |
| nearly_uniform | 904,278.00 | 938,213.44 | +33,935.44 |
| random | 540,988.28 | 582,879.18 | +41,890.90 |
| reachable | 837,079.90 | 925,878.60 | +88,798.70 |
| repeated_stamp | 618,500.12 | 681,547.97 | +63,047.85 |
| stripes | 507,712.63 | 587,671.18 | +79,958.55 |

Reproduction commands and tool descriptions: [README](../README.md). Machine-readable history: [history.csv](../results/history.csv). Final reproducibility evidence: [final_reproduction.json](../results/final_reproduction.json). Research details: [central log](experiments.md), [lookahead](lookahead.md), [sequence refinement](sequence.md), [bitsets](bitset.md).
