# Submission compaction investigation

The user subsequently corrected the source limit to **100,000 bytes**. The
investigation below records work under the earlier 10,000-byte assumption;
packed containers are no longer necessary. Checkpoint 039 is 107,628 bytes as
originally saved, but AST-unparse with two-space indentation yields 95,435 bytes
while preserving all identifiers and the exact AST. Multiline string content
was excluded from indentation changes. The root task is selecting the final
readable submission format.

## Reusable build tool

`tools/compact_submission.py` uses standard-library AST scope analysis to rename
local variables and owned attributes, strips documentation-only expressions,
and removes unnecessary token spacing. Token serialization is checked by exact
AST equality before and after whitespace compaction. Unsupported or reflective
scope constructs fail closed rather than being transformed speculatively.

Packing uses a literal LZMA source container. Forty-five LZMA1 parameter choices
are compared by actual emitted size; selection is deterministic and unrelated
to benchmark cases. The decompression dictionary is 1 MiB. Both ASCII base85
and a more compact PEP 263 Latin-1 source container are supported.

Example:

```text
python tools/compact_submission.py SOURCE.py OUTPUT.py --encoding latin1 --decoded REVIEW.py
python -m unittest tools.test_compact_submission
```

`decode_literal_wrapper` parses but never executes a submitted wrapper. It
accepts exactly either the base85 literal schema or the Latin-1 literal schema,
checks compressed-stream termination and trailing data, imposes output and
memory limits, and returns the decoded source for the normal static checker.
It does not make arbitrary or nested `exec` acceptable. The root agent owns
readiness/checkpoint integration; this task did not loosen those checks.

Latin-1 files must be uploaded as their original bytes. Copying their displayed
text through a UTF-8 editor or website can change the payload and file size.
ASCII base85 is available for environments requiring UTF-8 text, at a size cost.

## Measured sizes

| Original checkpoint | Original bytes | Dense source bytes | Final Latin-1 packed bytes |
| --- | ---: | ---: | ---: |
| 022 | 47,962 | 21,868 | 7,003 |
| 028 | 68,370 | 30,887 | 9,210 |
| 039 | 107,628 | 46,947 | 12,736 |

Generated comparison files are `solvers/experiments/compact39_core22_latin1.py`,
`compact39_core28_latin1.py`, and `compact39_latin1.py`. The corresponding dense
sources are retained separately for review. These are compaction experiments,
not new score-improvement checkpoints.

| Checkpoint | Packed SHA-256 | Decoded SHA-256 |
| --- | --- | --- |
| 022 | fe7614d168c6ab698e329940ec37e7e639dcda2ca9efd55b95726134411a4cf8 | 010cbb8560881eab13f60091fcfc7574137fa701a463927e43d97ae173a1d703 |
| 028 | 8f0ca1534cd1264b0b125ed3a60101c1b14090713587fde63184c4e1929ebe9c | 2f7ad6dfd931598ca5bbe9d0c84f5f94589161761f3c49bddc3743433d0f3a2d |
| 039 | 211b4f3e536435ec078b0dce6a09e495dfec26fc8c265366c66666cf9972b21d | 20d388eb868d6f7553d8566d04e63871af9ba5f0c36366ec62c1b072ac087f0a |

## Verification

Eight compactor tests pass. They cover nested scopes, comprehension binding,
closures/nonlocal/global, argument defaults, inherited methods and attributes,
keyword arguments, lexical-spacing warnings, refusal of unsupported reflection,
exact wrapper structure, compressed-stream bounds/trailing data, Latin-1 file
execution, and reproducibility with different `PYTHONHASHSEED` values.

For each of checkpoints 022, 028, and 039, cases 000, 002, 004, 008, 016, and
018 produced byte-identical stdout before and after compaction. Every sampled
answer passed the canonical output validator and simulator. Cases include both
stamp sizes, the minimum grid, and an N=30 case. The 022/028 measurements are in
`notes/compact_submission_parity.json`. Observed container overhead was usually
0.02–0.11 seconds; small timing differences also include normal process noise.
The final LZMA parameter tuning leaves the verified decoded hashes unchanged.
No full 320-case benchmark was run for these packaging-only experiments.

## Independent consolidation review

Reviewed `solvers/experiments/route_core028_slim.py` against original checkpoint
028 for the parent task. No semantic difference was found in the shared escape
method, default gain threshold, 5/6-plane aggregation, strict score comparisons,
or rank-based tie selection. Weighted initializer inheritance computes the same
geometry and value/goal masks before weighted counts overwrite the temporary
unweighted values. The routing agent separately tests randomized state and
full-solver equivalence. Recommended removing redundant value/goal mask ORs and
tie-mask reconstruction already supplied by the base initializer, which saves
space and runtime without changing results.
