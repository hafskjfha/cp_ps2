# Independent review: reverse constructor integration

Reviewed readable source SHA256
`390c3b5dfd7e502074c8679e1959cf3bae1ff4c3aab1eb21f4ffdb188dc1147d`
and packed source SHA256
`b70211712e8844d506849640aa2d1f25e0ab41861d373be35b0ab3bfd9090f54`.
No source or build-tool mutations were made during this review. Checks were
inline commands; no dedicated test file was created.

## Findings

No integration correctness defect found.

- The 27,492-byte packed program decodes **byte-for-byte** to the152,485-byte
  readable program. The submitted bytes satisfy the100,000-byte source limit.
- The original `million_safe_readable.py` prefix and its main function are
  textually unchanged. The inserted block contains `addmask`, `FastBack`,
  `seven_backward_construct`, the saved original retained function, and its hook.
- The AST rewrite removes the helper's module parameter and resolves its
  `m.build`, `m.color_bound`, `m.refine`, and `m.pair_sweep` calls to the original
  solver globals. No unresolved `m` attribute remains.
- Late binding of `solve_retained_iterated` is effective: the existing
  `solve_before_pair_annealing` calls that global at runtime. All later pipeline
  stages therefore process the new constructor result normally.
- Gate conditions correctly require N>=10,K>=12, initial matches strictly below
  88% of the color bound, and at most4C distinct untranslated target patches.
  Exactly88% is excluded; exactly4C patterns is allowed.
- Seven dispatch checks covered N9/N10, K11/K12, near-target, random-target,
  periodic-target, and uniform-target inputs. All used the intended branch and
  the reverse branch received width48.
- Existing `inspect_source` returns valid with no errors or review flags. The
  decoded imports are only `heapq`, `itertools`, `math`, `random`, and `sys`.
  Wrapper imports `base64` and `lzma` are also standard-library modules. The
  decoder is a literal codec wrapper, no local dependencies or file reads are
  required, and the actual program reads stdin and writes the required answer.

## Canonical standalone holdouts

Eight fresh periodic inputs were run sequentially through the actual packed
program using Python `-I -B`. All exited successfully with empty stderr, passed
the output validator, and were canonically simulated. Every result preserved or
improved the initial grid's match count. Seed713591; periodic patterns alternate
diagonal, horizontal, and vertical color periods. Two cases exercise the excluded
N/K boundaries.

| N | D | C | K | Operations | Matches | Seconds |
|---:|---:|---:|---:|---:|---:|---:|
|10|2|2|12|12|80|2.096|
|10|3|6|12|12|53|3.490|
|11|2|4|16|16|75|2.591|
|12|3|3|20|20|109|2.008|
|14|2|5|24|24|116|1.336|
|10|3|2|32|32|100|0.295|
|9|2|3|16|16|65|2.523|
|10|3|6|11|11|47|4.265|

These timings were obtained while other research jobs were active. They are
provisional, not isolated runtime qualification. The longest case is excluded
from the new gate and executes the original constructor path.

## Material limits

The gate deliberately **replaces** the old constructor on eligible inputs; it
does not run both and retain the higher score. Consequently there is no
per-instance runtime053 score floor on those inputs. Frozen benchmark comparison
must determine total gain and any regressions.

Width48 has no explicit time cutoff. Replacing the old constructor saves its cost,
but later stages remain active. Large periodic N30/K180 cases and gate boundaries
need isolated five-second qualification before promotion. The eight small
holdouts establish correctness, not that worst-case bound.

## Prepared large-periodic holdout metadata

No cases were written and no solver runs were started for this set. All12 metadata
entries were checked cheaply: their generated target patch counts pass the gate,
and their initial matches are strictly below88% of the color bound. This includes
the exact4C-pattern gate boundary via the `blocks` family. These inputs are
independent of the frozen benchmark.

Generation order for entry index `i`: initialize `random.Random(seed)`; draw N²
uniform colors for A; for even `i`, draw one stamp color and repeat it D² times,
otherwise draw D² stamp colors; shuffle `list(range(C))` into `palette`. Set
`T[row,col]=palette[f(row,col)%C]` using the specified family:
`diagonal: row+col`; `horizontal: row`; `vertical: col`;
`blocks: row//2+col//2`; `tile: (row%2)*3+col%3`.

| Index | N | D | C | K | Family | Seed |
|---:|---:|---:|---:|---:|---|---:|
|0|20|2|3|90|diagonal|914731|
|1|20|2|6|180|horizontal|915740|
|2|20|3|3|180|tile|916749|
|3|20|3|6|90|vertical|917758|
|4|24|2|3|180|blocks|918767|
|5|24|2|6|90|diagonal|919776|
|6|24|3|3|90|vertical|920785|
|7|24|3|6|180|blocks|921794|
|8|30|2|3|90|horizontal|922803|
|9|30|2|6|180|blocks|923812|
|10|30|3|3|180|diagonal|924821|
|11|30|3|6|180|tile|925830|

The expanded executable stress set is now prepared separately in
`results/seven_periodic_stress_config.json`: all12 combinations of N20/24/30,
D3,C3/6,K90/180, plus D2,N30,K180 with C3 andC6 (14total). The runner
`tools/seven_periodic_stress.py` uses the existing canonical `run_solver`, a
temporary isolated snapshot, sequential execution, and five-second timeouts.
It freezes and verifies every generated input hash. Its `--dry-run` passed for
all14 inputs and confirmed every input enters the gate. No stress solver runs
were performed during preparation; root owns isolated execution after stable.

## Optional disjoint-mask simplification

For a fixed physical position `p` and action, the rotated patch maps `p` to exactly
one stamp cell. Consequently that action belongs to at most one color mask in
`pickup[p]`. For distinct old/new colors, `om & nm == 0`, so `nm & ~om` equals
`nm` and `om & ~nm` equals `om`. All42,378 distinct-color mask pairs across six
mixed configurations passed direct checks; pickup masks also summed exactly to
coverage at every position. This is a proven optional simplification for a future
runtime revision; the frozen candidate was not edited or retimed.
