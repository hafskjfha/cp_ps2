# Stamp-plane cache runtime probe: rejected

The already verified bytearray private cluster state remains selected. The cache experiment changes neither the heuristic nor output and provides no meaningful runtime benefit.

`CachedClusterState` shares a dictionary across one search's clones, keyed by immutable stamp bytes. Values are immutable tuples containing only target-match score planes. The current state's grid-derived `old_planes` are added afresh on every call. The cache has8192 entries and deterministic clearing; a zero-entry version supplies the ablation. Only new variant files were written.

Static review verifies all original AST nodes outside `cluster_improve` remain unchanged, and the private `cached_cluster_choices` retains the original random-selection tail exactly.480 randomized state/choice/RNG/clone checks, including forced eviction at limit2, passed. A second review covers limits1,2,8192, immutable cached tuples, fresh grid-plane additions, clone independence, canonical transitions, and reuse of the same stamp cache on a different grid;246 checks passed in0.042s. The exact runtime is recorded in `results/seven_construct_cache_eviction_review.json`.

Isolated standalone measurements all produced identical output bytes:

| Case | Verified parent | Zero-cache ablation | 8192-entry cache |
|---|---:|---:|---:|
| case001 |4.202s|4.311s|4.262s|
| N30 D3 C2 K180 boundary |2.374s|2.385s|2.278s|
| N30 D3 C6 K180 boundary |4.299s|4.277s|4.303s|

Two helper-only repetitions on the C6 boundary averaged0.919s for the verified parent,0.981s for the zero-cache ablation, and0.909s for caching. The cache hit17,685 of23,695 lookups (**74.6%**), used6010 entries, and never cleared. Its roughly1% helper speedup did not improve the critical whole-program cases and fell short of the requested0.15s material improvement. No further paired timing or full qualification is justified.

Evidence: `results/seven_construct_cache_static.json`, `results/seven_construct_cache_probe.json`, and `results/seven_construct_cache_eviction_review.json`. Frozen diagnostic sources: `seven_construct_cached_readable.py` and `seven_construct_uncached_readable.py`. Neither is a selected submission.

