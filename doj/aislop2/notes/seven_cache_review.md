# Static review of the private stamp-plane cache

No actionable correctness defect was found in the reviewed implementation.
This was a static-only review: no solver transitions, parity runs, or timing
were executed. The candidate was subsequently rejected for integration because
its owner's timing probe did not show a material improvement; the selected
candidate remains the existing uncached runtime variant.

Reviewed files: `solvers/experiments/seven_construct_cache_state.py`,
`seven_construct_cache_build.py`, and the generated
`seven_construct_cached_readable.py`. The latter's SHA-256 is
`6e3efd529718250132771919b6ecefa37cd66b214c9db68f8c38ceb11de8770d`.

- The cache stores only stamp-versus-target match planes. These depend on the
  reference-oriented stamp, fixed target geometry, and fixed action order.
  `bytes(self.stamp)` is therefore a complete key within this cache's lifetime.
  Every initial `CachedClusterState` creates a fresh dictionary; only its
  descendants share it. Unrelated geometries do not share this dictionary.
- Entries are tuples of Python integers. `_combined_score_planes` copies each
  tuple to a new list before adding the state's current wrong-cell planes.
  No caller can mutate a stored entry through the returned combined planes.
- The clone separately copies grid, stamp, and wrong-cell planes, while sharing
  immutable geometry and the memoization dictionary. Cache mutations can affect
  hit rates across siblings but cannot alter their scores or stored board state.
- At a miss with 8,192 existing entries, the dictionary is cleared before the
  new entry is inserted; it never retains more than 8,192 entries. Cache hits do
  not clear it. Existing tuple references remain valid after a clear. A limit
  of zero disables insertion for the controlled uncached ablation.
- The target-plane addition and subsequent addition of wrong-cell planes match
  the parent's arithmetic. Target counts are at most 9 and combined counts at
  most 18, so the existing five-plane calculation remains sufficient.
- Inherited `State.best` dispatches to the new `best_candidates`. The private
  choice function changes only the source of its combined planes; the builder
  preserves the original candidate selection, random calls, deduplication,
  ordering, and return statements. Cache lookup, insertion, and clearing make
  no random calls and are not used as tie breakers.
- The builder replaces only the three intended names inside `cluster_improve`.
  Existing noncluster choices and the earlier state implementation remain
  available unchanged. The previously reviewed restriction still applies:
  stale `counts` and `stampmask` must not be consumed by inherited gain/escape
  helpers, which this private cluster path does not call.

The static argument supports equivalent behavior for these call sites. It does
not replace full output parity or runtime evidence, and this review makes no
speed-improvement claim.
