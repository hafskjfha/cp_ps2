# Continued optimization final report — 2026-09-26

Best submission: [`best_052_252937025.py`](../submissions/best_052_252937025.py). `solvers/current.py` is byte-identical. This is a self-contained Python program using only standard input/output and standard-library modules.

Frozen stable 320 score: **252,937,025 / 320,000,000**, average **790,428.203125**. Initial greedy score: **228,305,971**. Total improvement: **24,631,054 (+10.79%)**. This session began at checkpoint 050 and adds **42,226**, with eighteen improved cases and no regressions. These are local generated-case measurements, not a prediction of the official forty-input result.

## Benchmark and baselines

Frozen seed 20260925; nested smoke 20, development 100 and stable 320. The manifest and all 320 input hashes are unchanged. Eight families cover random, near-target, reachable, checkerboard, stripes, repeated stamps, nearly uniform and local adversarial inputs. Every N=3..30, D=2/3, C=2..6 and K endpoints 1/180 are represented. Stable 320 alone decides score checkpoints. Maximum-size runtime holdouts are separate.

| Baseline | Stable total | Average |
|---|---:|---:|
| Zero operations | 174,748,782 | 546,089.94 |
| Best immediate single operation | 186,065,927 | 581,456.02 |
| Repeated strict immediate greedy, checkpoint 000 | 228,305,971 | 713,456.16 |

Baseline evidence and early method breadth remain in [the initial report](final_report.md) and [experiment log](experiments.md). The existing infrastructure was independently audited before further solver work; no new dedicated test files were created.

## This session’s measured directions

| Method | Evidence and result | Decision |
|---|---|---|
| Additional suffix beam, width8/depth4 | Development100 tied parent | Parked |
| Additional suffix beam, width6/depth6 | Development100 +3,086 | Superseded by deeper probe |
| Retained suffix beam, width4/depth10, 120,000 transitions | Stable 320 252,909,754; +14,955 over 050; seven wins, no losses | Saved 051 |
| Exact short-horizon meet-in-the-middle | Nine eligible frozen cases already at proven optimum; sixteen exhaustive canonical comparisons | No score gain; parked |
| Uniform rotation change across one contiguous operation segment | Cached development 100 +5,442; exact canonical and independent review checks | Combined with suffix search |
| Exact whole-grid shortcut N=D | All reachable boards are rotations of original board or stamp, attainable in at most two moves | Runtime shortcut; equal optimum |
| Suffix + segment rotation + exact shortcut | Stable 320 252,937,025; +27,271 over 051; eleven wins, no losses | Saved 052 |

The suffix search keeps complete packed board-and-stamp states, an incumbent path and a fixed expansion budget. It accepts only exact final-score gains. The segment move changes every rotation in a selected interval by the same offset; conjugation cancels internal stamp rotations, allowing sparse endpoint differences to be scored with backward target labels. A separate exact sequence-delta check verifies each accepted edit.

Earlier successful methods include plateau exploration, negative setup moves with positive two-move return, diversified constructors, bit-parallel scoring, backward sequence refinement, beam reconstruction and sparse color routing. Earlier failed and limited methods are retained in the central experiment log. This session did not retune the frozen benchmark.

## Verification and runtime

- Stable 320: all valid; aggregate 353.798s, mean 1.106s, maximum 4.174s with one worker and a five-second timeout.
- Readiness: 38/38 valid plus identical deterministic repeat; maximum 3.807s.
- Maximum-size holdouts: 36/36 valid at N=30/K=180 across both D values and all C values; maximum 4.351s, p95 4.192s, mean 2.305s.
- All seven051 wins and all eleven052 wins reproduced their exact scores and output hashes in fresh subprocesses.
- Canonical transition audit: 1,800 direct/state transitions, 600 packed transitions and thirty exhaustive candidate gain/tie checks. Segment repair: 25,200 exhaustive mutations plus 648 independently reviewed mutations. Whole-grid shortcut: forty randomized orbit checks.
- Fresh final integrity: all 53 immutable checkpoint hashes, all 320 frozen inputs, strict score progression, current/best equality, full score arithmetic and readiness rows verified.
- Submission size: 99,738 bytes, below 100,000. Maximum output in stable 320: 1,498 bytes; maximum operation count: 180.
- Worst observed final-solver qualification time: **4.351s / 5.000s**, on this machine using CPython 3.12.12. Python 3.10+ is required for int.bit_count; hidden-instance or other-machine timings are not guaranteed.
- The source remains ordinary Python. Whitespace, six unused docstrings and four reversible identifier renames were compacted; independently reversed AST equality passed. No compressed or external payload is required.
- New component profiling is saved in [session_component_profile.txt](../results/session_component_profile.txt); its instrumented timing is not used for contest runtime claims.

Evidence: [final integrity](../results/session_final_integrity.json), [stable](../results/session_combined_stable.json), [readiness](../results/session_combined_readiness.json), [maximum-size holdouts](../results/session_combined_stress.json), [reproduction](../results/session_combined_reproduced.json), [independent audit](session_audit.md), [small-grid probe](session_small.md), [segment probe](session_sequence.md).

## Every strict best checkpoint

All prior files are preserved. Historical 039 exceeds the current 100,000-byte source limit and is retained as historical evidence; use the selected 052 file above. Runtime-only equal-score variant 049 is documented separately in results/runtime_variants.json.

| ID / submission | Stable total | Gain | Description |
|---|---:|---:|---|
| [000](../submissions/best_000_initial.py) | 228,305,971 | Initial | Initial strict immediate-gain greedy; beats zero and single-operation baselines |
| [001](../submissions/best_001_240756242.py) | 240,756,242 | +12,450,271 | Packed greedy with neutral stamp-state exploration and four deterministic restarts |
| [002](../submissions/best_002_240849239.py) | 240,849,239 | +92,997 | Packed greedy with exact positive-total two-ply escape including negative setup moves |
| [003](../submissions/best_003_242249708.py) | 242,249,708 | +1,400,469 | One-hot match evaluation enables twelve deterministic plateau-search restarts |
| [004](../submissions/best_004_243391996.py) | 243,391,996 | +1,142,288 | Four deterministic lookahead restarts with randomized action tie orders |
| [005](../submissions/best_005_244316245.py) | 244,316,245 | +924,249 | Select better of twelve neutral plateau runs and four two-ply lookahead runs |
| [006](../submissions/best_006_245343012.py) | 245,343,012 | +1,026,767 | Three complementary searches including lookahead during positive-gain moves |
| [007](../submissions/best_007_245544191.py) | 245,544,191 | +201,179 | Four exact backward coordinate sweeps with neutral ties refine the two-stream portfolio |
| [008](../submissions/best_008_246335486.py) | 246,335,486 | +791,295 | Four randomized exact backward sweeps refine the best of three complementary constructors |
| [009](../submissions/best_009_246786935.py) | 246,786,935 | +451,449 | Bit-sliced action evaluation funds eight width64 lookahead restarts and six refinement sweeps |
| [010](../submissions/best_010_246874186.py) | 246,874,186 | +87,251 | Bit-sliced plateau and lookahead search with eight exact backward refinement sweeps |
| [011](../submissions/best_011_247272076.py) | 247,272,076 | +397,890 | Depth-three profitable rescue at terminal two-ply plateaus |
| [012](../submissions/best_012_248036769.py) | 248,036,769 | +764,693 | Bounded neutral and lossy two-ply walks with best-prefix retention and fast exact refinement |
| [013](../submissions/best_013_248753972.py) | 248,753,972 | +717,203 | Sampled adjacent operation-pair replacement with exact completion and bitset refinement |
| [014](../submissions/best_014_249115734.py) | 249,115,734 | +361,762 | Incremental adjacent-pair sweeps followed by sampled exact pair completion |
| [015](../submissions/best_015_249389357.py) | 249,389,357 | +273,623 | Hybrid pair optimization plus exact small-budget search and retained beam candidate |
| [016](../submissions/best_016_249547073.py) | 249,547,073 | +157,716 | Hybrid pair optimization with retained small-budget beam through K24 |
| [017](../submissions/best_017_249880999.py) | 249,880,999 | +333,926 | Guided triple sequence repair combined with retained beam through K24 |
| [018](../submissions/best_018_250064691.py) | 250,064,691 | +183,692 | Color-bound early exits and small-board perturb-refine trials before guided triples |
| [019](../submissions/best_019_250384135.py) | 250,384,135 | +319,444 | Wider depth60 beam for tiny boards combined with small-board perturbation |
| [020](../submissions/best_020_250559222.py) | 250,559,222 | +175,087 | Bounded simulated annealing over operation pairs with best-sequence retention; max-size holdout passed |
| [021](../submissions/best_021_250867386.py) | 250,867,386 | +308,164 | Retained small-board perturbation and deep beam paths followed by annealed pair repair |
| [022](../submissions/best_022_250872488.py) | 250,872,488 | +5,102 | Retain annealed outcomes of both small-board paths with exact incremental state updates |
| [023](../submissions/best_023_250921331.py) | 250,921,331 | +48,843 | Large-board boundary-weighted constructor selection with cached state and refinement geometry |
| [024](../submissions/best_024_250934988.py) | 250,934,988 | +13,657 | Exact bidirectional search for binary 4x4 boards with five-move target reachability |
| [025](../submissions/best_025_250983831.py) | 250,983,831 | +48,843 | Combine exact binary target search with large-board weighted constructor selection |
| [026](../submissions/best_026_251149505.py) | 251,149,505 | +165,674 | Informed endpoint proposals in annealed pair repair; isolated maximum-size runtime passed |
| [027](../submissions/best_027_251280679.py) | 251,280,679 | +131,174 | Informed pair endpoints combined with exact binary search and weighted large-board candidate selection |
| [028](../submissions/best_028_251305191.py) | 251,305,191 | +24,512 | Weighted suffix refinement preserves informed composite score floor; isolated36 maximum-size check passed |
| [029](../submissions/best_029_251345195.py) | 251,345,195 | +40,004 | Annealed exact endpoint replacement across fixed intervening operations; seven wins and no regressions over028 |
| [030](../submissions/best_030_251481350.py) | 251,481,350 | +136,155 | Conditional informed triple annealing on weighted solver;26 wins/no losses over028, isolated max-size runtime passed |
| [031](../submissions/best_031_251606350.py) | 251,606,350 | +125,000 | Exact eight-move small-board finisher using backward wildcard constraints and forward color indexes; two perfect repairs |
| [032](../submissions/best_032_251668850.py) | 251,668,850 | +62,500 | Exact suffix completion after bounded tail removal plus qualified constructor undo;13 tiny holdouts passed including repeated search |
| [033](../submissions/best_033_251678439.py) | 251,678,439 | +9,589 | Two alternating exact forward/backward refinement rounds;five independent single-cell gains with full parent floor |
| [034](../submissions/best_034_251734381.py) | 251,734,381 | +55,942 | Two retained packed late-beam repairs on small boards;four extra matching cells over033 |
| [035](../submissions/best_035_251765631.py) | 251,765,631 | +31,250 | Four retained late beam repairs with qualified exact speed improvements; isolated 36-case maximum 3.391s |
| [036](../submissions/best_036_251771548.py) | 251,771,548 | +5,917 | Retained four-operation commutator append; one additional cell, exact canonical swap restoration, no regressions |
| [037](../submissions/best_037_251801728.py) | 251,801,728 | +30,180 | Retained hotter triple restart plus cleanup; eight improvements and no losses versus035; exact parent preserved on ties |
| [038](../submissions/best_038_251809034.py) | 251,809,034 | +7,306 | Retained width512 depth8 late beam repairs two cells over035;13 independent holdouts passed including depth8 repair |
| [039](../submissions/best_039_251862073.py) | 251,862,073 | +53,039 | Combined exact count-plane speed port, hot triples, commutator, annealed four-window repair and deeper beam; isolated36 max3.336s |
| [040](../submissions/best_040_251963428.py) | 251,963,428 | +101,355 | Compact informed core plus exact inverse cancellation, global operation relocation and sparse six-operation routing; 9548-byte submission |
| [041](../submissions/best_041_252038607.py) | 252,038,607 | +75,179 | Four sparse routing repairs after exact cancellation and global relocation; compact 9539-byte solver |
| [042](../submissions/best_042_252085720.py) | 252,085,720 | +47,113 | Five sparse routing repairs recover additional mismatches within the same bounded permutation search |
| [043](../submissions/best_043_252147480.py) | 252,147,480 | +61,760 | Size-adaptive sparse routing through eight profitable repairs after three relocation rounds |
| [044](../submissions/best_044_252152063.py) | 252,152,063 | +4,583 | Search five low-loss deletion candidates across five global relocation rounds before sparse routing |
| [045](../submissions/best_045_252192457.py) | 252,192,457 | +40,394 | Complete up to twelve profitable sparse routes on smaller boards with bounded larger-board work |
| [046](../submissions/best_046_252388472.py) | 252,388,472 | +196,015 | Retain full prior search portfolio with exact temporal relocation and bit-parallel six-operation permutation routing; plain Python below100000 bytes |
| [047](../submissions/best_047_252571424.py) | 252,571,424 | +182,952 | Expanded global relocation plus twelve size-adaptive sparse repairs using exact parallel anchor scoring |
| [048](../submissions/best_048_252747393.py) | 252,747,393 | +175,969 | Fast exact anchor scoring funds up to thirty profitable sparse routing steps across all board sizes |
| [049](../submissions/best_049_252862932.py) | 252,862,932 | +115,539 | Complement six-operation repairs with twelve-, eighteen-, ten-, and twenty-four-operation cycle powers and revisit shorter generators |
| [050](../submissions/best_050_252894799.py) | 252,894,799 | +31,867 | Retained full-state beam rebuilding of operation blocks with exact backward suffix labels; six stable wins and no losses; max-size holdout passed |
| [051](../submissions/best_051_252909754.py) | 252,909,754 | +14,955 | Retained alternate width-four depth-ten suffix beam with 120000-transition cap; strict canonical gains, maximum-size holdout and exact winning-output reproduction passed |
| [052](../submissions/best_052_252937025.py) | 252,937,025 | +27,271 | Exact contiguous-segment rotation repair after retained suffix beam; exact whole-grid stamp shortcut; all stable gains reproduced and maximum-size holdouts passed |

Complete machine-readable history: [results/history.csv](../results/history.csv).

Final source SHA256: `a3b32accc115fa0dc91143b6bbaaeb25226651d8e8557c70bbcd6f3b1a7a5442`.
