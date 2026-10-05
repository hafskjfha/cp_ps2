# Independent combined-solver review

Reviewed `solvers/experiments/m2_combined_readable.py` and its packed submission candidate `m2_combined.py`. **No blocking correctness or composition issue found.** This review does not replace the parent's pending full stable score/runtime qualification.

Reviewed packed SHA256: `f75fbfbb57fa2b63670ac07f5b9e23f04606839a26b87f1c7b08be6df637fc44` (33,304 bytes).
Readable SHA256: `4cbc985d71535e923b2b42a3f4382471d90c44c05d5dab4fd7291ac65018baf7`.
The standard-library Base85/LZMA wrapper decodes byte-for-byte to the179,443-byte readable source. AST inspection finds only standard-library imports and the expected stdin/stdout entrypoint; no local helper/data dependency was introduced.

## Composition

- `_cluster_original_million_beam` points to the new bytearray/private-state plain beam. The prior cluster-domain wrapper is retained by `_m2_constructor_previous_beam`; its dynamic lookup intentionally reaches that faster implementation. The new constructor wrapper captures that prior wrapper once, so there is no recursive alias loop.
- `_m2_constructor_previous_retained` captures checkpoint055's backward/retained constructor gate. On an ineligible input the wrapper calls this saved function. The new53-case frozen-suite gate requires N>=10,K>=12, initial agreement below70% of the inventory bound, and more than4C distinct unrotated target patches. It is disjoint from the old structured-target backward-constructor gate.
- The new constructor uses actual physical states and actual operation paths. Canonicalizing only the stamp in the deduplication key is valid because all four relative stamp rotations remain legal; subsequent operations run on the retained representative's actual orientation.
- `_m2_cycle_parent` captures the existing outer solve before defining the cycle-tail wrapper. Global constructor/beam lookups inside the saved pipeline reach the new wrappers as intended. The repair only appends an improving legal path when at least12 operations remain. Each BFS extension checks its path length against the supplied remaining budget.
- Refinement kernel replacements install before `main()` executes. The old initializer remains selected below N12 and the scalar action scan below N16. The only altered preexisting class body is the rank-mask construction. Tie rank, incumbent retention, and zero-gain behavior are preserved.

Outside the new constructor and cycle-repair domains, the intended change is runtime only. Static routing checks and direct differential checks support this; complete320-case stdout parity is not claimed by this review.

## Independent checks on the exact combined bytes

`results/m2_combined_independent_review.json` records:

-26 random configurations crossing N11/12 and N15/16 gates, both stamp sizes, C2/C6, and minimum/maximum N.
-338 complete refinement-state/`best()` comparisons with checkpoint055.
-156 canonical forward grid+stamp transition checks while alternating physical and backward-wish state updates.
-260 scalar-versus-installed `best_action` comparisons, including wildcard wishes, incumbent actions, and both zero-gain modes.
-6 exact operation-sequence comparisons of the new plain beam against055's original plain beam, covering both D and max N; every result was canonically simulated.
-6 fresh canonical cycle-tail checks on N5,6,8,12,18,30. Predicted gains equaled final-grid matches and every path respected K.
-A320-case independent audit of the constructor gate, confirming53 eligible cases.

All checks passed. Earlier isolated-fragment canonical validation additionally covered140 random/generalized-wish cycle cases; the combined review ran fresh checks on the assembled source.

## Measurement interpretation

The forecasted constructor gain259,551 and isolated cycle gain100,223 must not be treated as a verified combined score. The early constructor can alter the path seen by later stages, including spare operation count and which cycles become useful. Only the parent's full run of the exact packed bytes establishes the combined total and5-second suitability.
