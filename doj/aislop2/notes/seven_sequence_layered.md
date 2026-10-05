# Shifted patch assignment experiment

The proposed construction alternates two disjoint patch tilings with different offsets. Each layer uses a global Hungarian assignment to move source patches to destinations, decomposes that permutation into stamp cycles, and selects profitable cycles with an operation-budget knapsack. Later iterations optimize one layer against the exact physical prefix and the target wishes propagated backward through the other layer. The shifted tilings allow the second layer to recombine cells from several first-layer patches.

This is a standalone construction experiment, not an integrated submission. It uses fixed configuration rules and no case IDs. A supplied reference sequence is preserved whenever construction fails to improve its canonical final score.

## Scope

The current checkpoint has only 2,079,150 points of relaxed score headroom across all cases with K greater than 100. Restricting those to current matches at least 85% of the color-inventory bound leaves 1,089,636 points. Routing nearly solved, large-K instances therefore cannot alone deliver the requested seven-million-point improvement. This does not establish an impossibility result for the full task.

The broader construction gate K*D^2/N^2 >= 1.25 covers 49 unsolved stable cases with 3,347,627 points of relaxed remaining headroom. At density 1.5 the corresponding scope is 45 cases and 3,126,945 points. These are upper bounds on opportunity, not predicted gains.

## Initial diagnostic

The fixed-frame implementation restores the stamp exactly after every cycle. Three alternating sweeps and two starts were evaluated on the 13 eligible development cases, followed by six passes of existing sequence refinement and two pair-sweep passes. All candidates were validated and scored with the canonical tools.

There were zero wins against checkpoint 055. Total diagnostic time was 3.915 seconds and maximum case time was 1.033 seconds. These times are provisional because another research diagnostic was allowed concurrently. For example, case 001 rose from 490 raw matches to 564 after refinement, compared with 703 for the selected solver. The construction quality is too low to integrate.

An additional 16 fresh random instances passed canonical legality and reference-score preservation checks. Internal assertions verify each selected layer's predicted objective and buffer restoration.

## Free-rotation ablation

The fixed-frame assignment couples all edge rotations around a permutation cycle. That restriction is unnecessary when final stamp contents are unconstrained: the stamp may return rotated. The ablation chooses the best of four rotations independently for every source-destination edge. During cycle execution it tracks the current stamp orientation and adjusts each operation rotation. A completed cycle changes only the chosen board patches and rotates the stamp; stamp colors never remain on the board.

A profitable singleton rotation is represented by two operations. Each layer requires unconstrained stamp wishes, and its exact simulated score must equal the assignment and knapsack prediction. This is valid under the two-layer construction because a suffix made entirely of such cycles also leaves all backward stamp wishes unconstrained.

The ablation is implemented in `solvers/experiments/seven_sequence_layered.py`; the canonical diagnostic is `tools/seven_sequence_layered_probe.py --free-rotations`. Execution waited until the root task's isolated submission-readiness checks finished.

All 40 fresh random canonical checks passed, including legality and reference-score preservation. The same 13 development cases then produced zero wins against checkpoint 055. Total diagnostic time was 6.012 seconds; maximum case time was 1.617 seconds. All 13 outputs were canonical-validator legal.

Independent edge rotations improved raw construction quality: case 001 increased from 490 to 585 matches and case 075 from 499 to 541. Their refined scores were still only 605 and 545, against baseline scores of 703 and 569. Results are saved in `results/seven_sequence_layered_free_dev.json`. The measured result does not justify integration or further tuning within this campaign.

## Limitations

Assignment score and operation cost are not jointly optimized: movement penalties encourage shorter useful permutations, then knapsack drops whole cycles. Alternation can become trapped because each layer must improve the current exact objective. Disjoint tilings leave some borders untouched and restrict how cells can be recombined. Finally, these constructors start from an empty sequence rather than inheriting the strong baseline's physical arrangement, so local sequence refinement must close a large initial quality gap.
