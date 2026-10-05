# Independent review: reverse plus residual-cluster integration

Reviewed `solvers/experiments/seven_construct_combined_readable.py`, SHA256
`b43cff8984091c59d0371831acf7ece385db68dcff9ece774e56fd75f47938de`.
No solver source or frozen artifact was edited. Only lightweight inline checks
were run; no full solver benchmark or large holdout was launched during root's
isolated qualification.

**Recommendation: the integration is structurally sound and can proceed to
packing and full qualification. No correctness blocker was found.**

## Source changes and domain exclusivity

AST comparison confirms the complete reverse-integrated parent and its main
function are unchanged. The added fragment contains the cluster helper, domain
predicate/cache, saved original constructors, and two late-bound wrappers.

The early `construct_all` wrapper retains its original constructor result and
asks the cluster helper to improve it. The final `million_beam` wrapper skips
that older final construction only on the cluster domain. Names resolve through
the intended original function aliases; no recursion or shadowing defect was
found.

`cluster_domain` requires N>16,D=3,K>10 and then excludes **exactly** the reverse
constructor's eligibility predicate. Both now count only unrotated target
patches, use the same4C threshold, and use the same initial-score/color-bound
test. This was checked against actual reverse-hook dispatch on120 mixed
configurations including threshold N/K values, random targets, periodic targets,
and initially matching grids. No overlap occurred.

The corrected patch definition matters. An explicit N24,D3,C3,K90 block-periodic
example has12 unrotated patterns but48 rotated patterns. The reverse branch is
eligible at12=4C, and the cluster predicate correctly returns false. Counting
rotations would have incorrectly activated both domains.

## Cluster objective and transition checks

The auxiliary objective counts orthogonally adjacent pairs of mismatching grid
cells. Each physical stamp cell is visited once. Toggling its wrong bit and
updating its degree against the current mask counts every changed edge exactly,
including edges whose two endpoints both change. Boundary masks exclude row
wraparound.

Across24 mixed configurations, the review checked:

- **2,351 transitions** against the canonical simulator.
- Every resulting wrong-cell bitset against full independent reconstruction.
- Every incremental auxiliary count against a complete horizontal/vertical edge
  scan.
- **2,063 sampled candidate gains** against exact match-count differences.
- Parent/sibling isolation of grid, stamp, counts, score planes, wrong mask, and
  total matches after every child update.

Ten small complete helper searches additionally matched the original frozen
edge-set implementation's output exactly. All outputs passed the canonical
validator and preserved the supplied reference score. Inputs remained unchanged,
and reverse-order replay after intervening searches returned identical paths.

## Cache and state safety

The domain cache key snapshots N,D,C,K and the full grid,target,stamp values.
It therefore remains correct when callers reuse lists or mutate their contents.
Explicit mutate/restore checks changed domain results as expected. The cache
holds only one entry and cannot accidentally reuse a different input's decision.

`clone_state` copies all mutable search fields that `State.apply` changes.
`_cluster_wrong` is an integer, so inheriting it through the shallow dictionary
copy is safe; each child then receives its own updated integer. Shared geometry,
target masks, and coverage masks are read-only. The existing refinement caches
remain keyed by their geometry and target contents. Interleaved helper replay
found no contamination.

Deduplication by complete grid+stamp bytes is sound for the auxiliary objective:
both wrong mask and adjacent-error count are determined by that same state and
the immutable target.

## Submission and qualification limits

The readable file is161,396 bytes and therefore exceeds the100,000-byte submitted
source limit. It is a self-contained standard-library program: static review
found only heapq,itertools,math,random,sys imports, stdin input, no external/local
dependencies, and no suspicious filesystem or dynamic-execution calls. The only
static rejection is readable source size. Pack it, verify exact decoding, and
repeat the submission audit on the actual submitted bytes.

`cluster_improve` preserves its supplied early reference floor, but skipping the
old final `million_beam` does **not** establish a floor against the complete old
solver. Total gains and regressions still require the full frozen comparison.
The new search moves work earlier in the pipeline; subsequent refinement can
change runtime. Large random targets exercise the cluster domain, while the
prepared periodic stress inputs exercise the reverse domain. Both need isolated
five-second qualification before promotion.
