# Constructor campaign after checkpoint055

All diagnostics use the unchanged frozen cases, exact integer score, canonical simulator and strict output validation. No shared solver/checkpoint/history files were changed. Diagnostic timing is provisional because sibling agents also run.

**Latest candidate:** `m2_construct_compact1024_fragment.py` and its self-contained `m2_construct_compact1024.py`. It retains the selected early64 constructor while expanding compact inputs with the packed engine described below. Combined affected-domain diagnostic gain is **380,080** above055. Fresh full standalone qualification remains necessary.

## Selected early constructor replacement

The strongest full-pipeline candidate replaces retained construction with a width64 forward beam that deduplicates grid+stamp states modulo stamp rotation, then retains any improvement from the fast width16 residual-cluster constructor. Existing downstream sequence refinements still run. The redundant later plain forward beam is skipped in this domain.

The domain is determined only by input: N>=10, K>=12, initial matches below70% of the color-inventory bound, and more than4C distinct unrotated target patches. It is disjoint from the existing periodic-target reverse-construction domain. Other inputs follow checkpoint055 unchanged.

| Full pipeline | Dev delta versus055 | Stable delta | Runtime maximum |
|---|---:|---:|---:|
| Early width64 orbit beam | +77,746 | not run | 3.236s dev |
| Early64 plus cluster16 | +85,524 | **+259,551** | **4.165s stable diagnostic** |
| Early96, capped64 for N>=24,K>=120, plus cluster16 | +66,993 | not run | 4.469s dev |
| Two independent width32 orbit beams, choose best, plus cluster16 | +60,689 | not run | 4.710s dev |
| Width64 orbit beam plus three independently refined diverse finalists | +85,524 | not run | 5.176s dev |

The selected stable diagnostic has27wins and3losses. It computes whole replacement-pipeline outputs on every input in the affected domain; it does not retain the old per-case score floor. Its improvement is therefore a net score change. A separate fresh standalone320-case qualification is still required before saving a best checkpoint.

Sources:

- `solvers/experiments/m2_construct_pipeline_fragment.py`: flat4.1KB integration fragment, no local imports.
- `solvers/experiments/m2_construct_pipeline_readable.py`: self-contained readable full candidate, above the source-size limit.
- `solvers/experiments/m2_construct_pipeline.py`:29,789-byte standard-library LZMA wrapper, decompresses to that readable candidate.
- `results/m2_construct_pipeline_stable_w64_m1.json`: selected net stable-domain results with operations.

## Plain beam runtime improvement

`m2_construct_fast_fragment.py` changes the existing plain forward beam's private state to the already-tested `ClusterState`: bytearray board/stamp, mutable score planes, immutable unused counts. It preserves choices and operations.20paired cases all produced identical operation lists and passed canonical validation. Aggregate helper time fell from6.671s to4.838s (27.5%) in an alternating-order diagnostic. This fragment is separate from the selected pipeline candidate and can fund other search outside its replacement domain. See `results/m2_construct_fast_parity.json`.

## Other measured directions

| Hypothesis | Dev retained-parent gain | Outcome |
|---|---:|---|
| Reverse residual clustering, width24 | 4,444 | weak |
| Plain faster width48 forward beam | 35,879 | weaker |
| Width64 forward beam with stamp-rotation equivalence | 71,376 | basis for integration |
| Wider96 beam with4 branches | 57,888 | rejected |
| Score24 sampled outgoing stamp states before selecting6 actions | 45,983 | some complementary wins, limited gain |
| Two-ply optimistic continuation | 24,970 | expensive |
| Reserve of maximum-gain next actions | 7,276 forward;0 reverse | rejected |
| Multiple final beam paths independently refined | 8,272 | rejected |
| Reward squared residual mismatch density over all stamp regions | 34,284 | weaker |
| Keep half incumbent prefix and reconstruct remainder backward | 0 | rejected |
| Exact two-operation macro edges including max through max−3 setup gains and random pickups | 13,081 | rejected |

The standalone width64 orbit constructor scored217,243 retained-parent diagnostic points on all320stable cases, with29wins,82.158s aggregate helper work and2.548s maximum. This is less than the net early-integration gain259,551 because downstream refinement benefits from the new start. These measurements must not be added together.

Results are stored as `results/m2_construct_*.json`; probe source and all measured hypotheses are retained under `solvers/experiments/m2_construct*`.

## Flattened candidate verification

The specialized flat constructor reproduces the research helper's operation lists on8random/boundary configurations covering N3–30, D2/D3, C2–6 and K1–12. The compressed standalone candidate also exactly reproduces diagnostic operations on4 cases, including an unchanged case and cases in both winning/losing replacement outcomes. All outputs passed canonical validation. See `results/m2_construct_pipeline_parity.json`.

Compressed candidate SHA256: `e2e06580b4e57753d4d8061d2827c65e9fd2edba984200ad631881296d76aae9`.

The two32-wide beams lost points relative to the selected64-wide candidate. Refining3additional final beam paths (from the last4layers, within2raw matches of the best, chosen for operation-sequence diversity) reproduced every selected development score exactly while adding roughly6seconds aggregate runtime. Both variants were rejected.

## Follow-up diversity and adaptive search

Three structural beam-diversity policies were compared inside the full early pipeline at width64: a cap on equal rotating grid projections, quotas by current match count, and quotas by the initial operation. Development gains over055 were66,405,58,310,and56,577 respectively, all below the selected85,524. None justified stable measurement.

The compact domain is input-derived: D3,N10–16,K20–80, within the same nonperiodic/low-initial-match constructor domain. It contains6stable cases. A512-wide beam forK<=48 and256-wide beam forK49–80 added57,256 stable points over the selected64 pipeline, with no regressions. Its maximum whole-pipeline diagnostic time was4.087s before the newer runtime kernels.

Increasing to1024/512 added **120,529** over selected64 (another63,273 over512/256). Source/runtime changes were checked to preserve these exact operations:

| Compact1024/512 implementation | Aggregate seconds | Maximum seconds |
|---|---:|---:|
| New refinement runtime kernels, old private beam state |29.096|5.312|
| Plus bounded stamp-rotation canonicalization cache |28.834|5.277|
| Plus bounded incoming-score-plane cache |27.264|4.895|
| Packed six-bit private beam state plus rotation cache |**22.254**|**3.942**|

The packed engine was supplied and independently differentially checked by the sequence agent. It represents every action's gain in a fixed six-bit field, caches per-state scores, and retains the same action ties and RNG consumption. All6 whole-pipeline operation lists are identical across the variants. The selected final integration uses the packed engine only on the compact wider-beam domain; other affected inputs keep the selected64 state representation.

Final compact scores are041:119matches,117:126,201:118,261:172,277:85,and309:87. Their input-independent gate and widths are recorded in `results/m2_construct_pipeline_stable_w64_m1_compact1024_long512_fast_packed.json`. The total constructor contribution is259,551+120,529=**380,080**. This sum composes disjoint modifications to the already-evaluated affected-domain outputs, not independent overlapping search gains.

`m2_construct_compact1024_fragment.py` includes the frozen packed engine and all constructor changes. `m2_construct_compact1024.py` is a34,359-byte standard-library wrapper over the self-contained readable source with the newer refinement runtime kernels. Fresh standalone runs for041,277,and091 exactly reproduced diagnostic operation lists and passed canonical validation, with3.617s,3.182s,and1.778s runtimes. Evidence: `results/m2_construct_compact1024_parity.json`; wrapper SHA256 `4e81c16bf826684c170d3000d8d6b8f1f8ae294632d14b754484bf1fd4039b42`.

A further N17–23 expansion chose power-of-two widths up to512 under an11,000,000 budget for N²*K*width. It lost7,114 development points relative to selected64. Retaining a separate64-wide raw candidate before refinement still lost1,891 and took up to4.919s; differing raw ties can refine differently. This medium-board extension was rejected.
