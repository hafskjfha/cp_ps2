# Independent FastBack review

Reviewed `solvers/experiments/seven_fastback.py` SHA256
`e077482153119b2683d0008c6893ba1468aeeb06083431e1ba6c94fdcb6f77d7`.
Root-owned source was not edited. All checks below were inline commands; no
dedicated test file was added. Detailed measurements are in
`results/seven_fastback_review.json`.

Root subsequently adopted the bytearray change. Current source SHA256
`74fa67aa4d872903cc64a22882fb7e300cde43312a4d0234a559c0c2844bc146`
passed another288 exact state/plane comparisons against the reviewed original,
including all347,520 gain entries, and288 canonical transitions.

## Result

No correctness defect found. The exact backward gain, incremental planes,
candidate gains, reversal of operations, and canonical final score agree in all
tested configurations.

- 36 configurations, including both dimensions, colors2..6, N=D, N3 and N30.
- 432 reverse states, each with every legal action independently evaluated:
  **253,968 exact action-gain comparisons**.
- 1,728 candidate sets at branches1/4/6/12: legal distinct actions, exact gains,
  decreasing gain order, first gain equal to the exhaustive maximum.
- 432 transitions compared with the canonical simulator. Parent states and
  original objective arrays remained unchanged; child storage was independent.
- 432 complete prefix reversals canonically simulated from the original input;
  resulting target-grid matches equal the maintained backward score.
- 30 end-to-end constructions with K1/2/3/7/16/32/180, width1/2/4/8,
  branch1/4/6, future weight0/3/8. All outputs valid, no initial-score regression,
  and repeated calls returned identical operations.

The exact plane invariant is:

`D² + matches(reverse_board_patch, initial_stamp) - matches(reverse_board_patch, initial_board_patch)`.

The temporary score planes add matches between the reverse stamp and original
board patch. Subtracting D² and the existing reverse-stamp/original-stamp matches
therefore gives the complete swap gain. Five planes suffice because the encoded
value is at most3D²<=27. Sentinel6 contributes no match against real input colors.
Every operation is an involution in the reference stamp orientation, so reversing
the action list is correct without changing rotation values.

## Small performance option

Only in memory, change `engine.first` to use `bytearray` for its board and stamp.
This preserves all arithmetic and makes `board[:]`, concatenation, and the
deduplication key conversion cheaper. Four varied full constructions were run
four times each, alternating the original and modified engines. Every output was
identical. At width16:

| Configuration | Original average | Bytearray average |
|---|---:|---:|
| N30,D3,C6,K180 |0.978s|0.928s|
| N30,D2,C6,K180 |0.532s|0.446s|
| N20,D3,C3,K80 |0.281s|0.269s|
| N15,D3,C6,K120 |0.358s|0.361s|

This is an optional small optimization, not full submission timing qualification.
Machine load was shared, so exact speedups should be remeasured during the final
isolated qualification.

An additional cancellation rewrite of plane updates also preserved all16 full
construction outputs, but timings were noisy and did not demonstrate a clear
benefit. Do not adopt it on these measurements. The `mixed` argument currently
has no effect; this is harmless compatibility, not an active search parameter.

No full320 score claim or contest runtime guarantee is made by this audit.
