# Independent private cluster-state review

**Conclusion: no actionable correctness defect found.** Both the list-backed and
bytearray-backed optimization are approved for the exact private cluster usage
reviewed here, subject to the separate full output-parity and runtime gates.
This review does not certify runtime or submission packaging.

Reviewed source hashes:

| Source | SHA-256 |
| --- | --- |
| `seven_construct_combined_readable.py` | `b43cff8984091c59d0371831acf7ece385db68dcff9ece774e56fd75f47938de` |
| `seven_construct_fast_readable.py` | `7ea3212ba79e2c09f3b4b39b77e26d52533df450d1e3e054c3c33f338997a3be` |
| `seven_construct_fast_bytearray_readable.py` | `db33ee57d94a85e7ddbceb916e1cd7e23b12aeda8fe050b80fc9c5f44326f9d4` |

The sources are under `solvers/experiments/`. Machine-readable independent
evidence is `results/seven_fast_cluster_review.json`. No solver was edited and
no dedicated unit-test file was added. Checks were run inline and took about
one second before a short edge-case follow-up.

## Consumer and lifetime audit

`ClusterState` is instantiated only inside `cluster_improve`, and the optimized
clone is called only on those beam states. The only score consumers in that
path are `million_choices`, `State.best`, and `State.best_candidates`.
They use `stamp`, `grid`, `target_bits`, `old_planes`, `order`, `all_actions`,
`actions`, and `size`; they never read `counts` or `stampmask`.

The inherited `State.gain` and `State.escape` would be unsafe after the optimized
apply because they use the intentionally stale caches. They are not called on
these states. This private-use restriction is part of the approval; the change
must not be generalized by replacing unrelated `State` call sites.

After beam search, `refine` and `pair_sweep` receive the original input values,
geometry, and operation IDs. They create their own state; the private beam
states and stale caches do not escape into those routines. The geometry cache
stores only the shared geometry, never the beam's mutable caches or grid.

## Arithmetic, aliasing, and representations

The optimized swap still iterates the original reference-oriented stamp-cell
to rotated-grid-cell mapping. Its match delta is identical to the parent.
`old_planes` represents the number of wrong cells in each patch: gaining a match
subtracts one through bitwise borrow, and losing a match adds one through carry.
Every intermediate value is in [0,D²], so four planes suffice for D²<=9.
The per-cell coverage masks are sums of disjoint region masks and therefore
equal their bitwise union. Eager precomputation produces the same masks as the
parent's lazy precomputation.

The clone separately copies `grid`, `stamp`, and `old_planes`. `matches` and
`_cluster_wrong` are immutable integers. Shared `counts` is never subsequently
read or changed, while the shared geometry, target, order, target bitsets, and
coverage masks are read-only throughout the private search.

Bytearray conversion preserves all color values because legal colors are 0..5.
Indexing and iteration still yield the same Python integers. Slices create
independent bytearrays; concatenation remains valid because both grid and stamp
use the same representation. `bytes(grid+stamp)` and `tuple(stamp)` produce
identical deduplication keys and diversity signatures for either representation.
No added operation consumes random numbers or changes comparison ordering.

## Independent evidence

- The entire module AST, including top-level bindings and imports, matches the
  parent after removing the two added helper definitions, discarding inert
  top-level string expressions, and reversing the two intended names inside
  `cluster_improve`. This is stronger than matching only same-named functions.
- Sixteen N/D/C configurations cover N=3,4,7,17,30, D=2/3, C=2/6.
- 384 transitions per variant were checked against the canonical simulator for
  grid, reference-oriented stamp, and match count. Score planes and best-action
  results also matched the parent.
- 384 `million_choices` comparisons matched both the chosen actions/gains and
  the exact subsequent random-generator state across all three implementations.
- 768 clone checks verified independent mutable storage and unchanged parents
  after applying an operation to the child. Intentionally unused caches stayed
  unchanged in 768 checks.
- Four complete small cluster searches produced identical operation sequences
  in all three implementations. During these runs, reads of `counts`,
  `stampmask`, `gain`, or `escape` on private states were changed to raise an
  assertion after initialization; no such reads occurred.
- An additional 64 boundary transitions start with fully matching or fully
  mismatching boards, use both stamp sizes and all rotations, and exercise
  error-plane values through 9. Every patch's encoded count was checked directly
  from the canonical grid. Replacing the global geometry cache with another
  target did not alter existing private states.
- Reviewed source hashes were rechecked after all checks.

## Limits

The complete-cluster parity cases intentionally use small widths and horizons
to avoid interfering with isolated timing owned by the other worker. They are
not a replacement for full 320-case output-hash parity and boundary timing.
The readable files exceed the contest source-size limit and are research inputs
to the existing packing workflow; this review does not certify a packed output
or establish its relationship to checkpoint 055's executable bytes.
