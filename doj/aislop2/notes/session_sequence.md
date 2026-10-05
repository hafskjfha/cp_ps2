# Session: exact uniform rotation of an operation segment

Parent: immutable `submissions/best_050_252894799.py`, frozen stable320 score252,894,799. This worker owns only the session experiment files and reports.

Hypothesis: adding one rotation offset modulo four to every operation in a contiguous segment changes a coordinated set of actions unavailable to individual rotation refinements. All operations are conjugate by a stamp-cell permutation; the intervening virtual stamp permutations cancel. Therefore the whole segment can be evaluated using a rotated incoming stamp and inverse-rotated outgoing stamp. This is distinct from previous block reorder, relocation and beam reconstruction experiments.

`solvers/experiments/session_sequence_fragment.py` implements one exhaustive best-improvement pass over every interval and each nonzero rotation. It uses `SequenceState` prefix states and exact suffix wishes. A sparse dictionary transports at most D squared changed colors through the original swaps, then accounts for the inverse stamp permutation at every endpoint. Positive candidates are rechecked through the existing independent `SequenceState.delta` before acceptance. It skips cases already at the color-inventory upper bound. K and operation coordinates are unchanged.

Self-contained candidate: `solvers/experiments/session_sequence.py`. It appends the helper after the entire best050 pipeline. Source physically uses LF and is **99,884 bytes**, SHA256 `f37208a35510802aff99c69bff4f7d2e2ffc6a69be339c2926ceafac8bb3773a`. Initial Windows text output was physically102,935bytes despite a99,884-byte universal-newline read; this was corrected before freezing by writing bytes directly. Only parent docstrings/blank lines were removed. AST comparison of101 parent top-level nodes verifies that the sole functional edit is the final solve wrapper; the helper is one added definition.

Inline verification used canonical simulator enumeration, without adding a dedicated test file:40 fixed-seed random instances, both D2/D3, K20, all25,200 segment mutations. The helper result equals the exhaustive best score on each instance and retains the parent score floor. It uses no randomness.

Cached frozen development100 diagnostic (`results/session_sequence_gauge_dev_cached.json`) uses canonical-validated parent outputs from root's `results/session_parent_dev_cache.json`:

- Total score delta **+5,442**, three wins/97ties/no losses.
- case007: +1 matching cell, +1,111 score.
- case043: +2 matching cells, +2,959 score.
- case063: +1 matching cell, +1,372 score.
- Helper aggregate runtime2.119s, maximum0.218s, measured under shared CPU load.
- First20 diagnostic: +1,111, helper max0.229s (`results/session_sequence_gauge_diag.json`).

End-to-end standalone case007 (`results/session_sequence_gauge_endtoend.json`) is valid,589matches/654,444score,180operations,1,498outputbytes. Provisional shared-load runtime4.729s with timeout10; this is not contest runtime qualification. The LF source correction after this check is semantically inert.

This is a promising cached diagnostic, **not a measured stable improvement or saved checkpoint**. Root owns full stable testing, isolated five-second runtime qualification, optional combination with the independent suffix-beam candidate, and checkpoint promotion. CPU-heavy work paused after the requested cached100 diagnostic. A combination may require source size trimming: all parent docstrings total311bytes, blank lines8bytes, and AST-unreferenced `greedy`294bytes; do not exceed100,000physicalbytes.
